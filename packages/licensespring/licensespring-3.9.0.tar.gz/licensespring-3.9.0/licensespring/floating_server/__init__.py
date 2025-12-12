import json
import logging
import threading
import time

import requests
from requests.auth import HTTPBasicAuth

import licensespring
from licensespring.api.error import ClientError
from licensespring.api.signature import FSSignatureVerifier
from licensespring.hardware import HardwareIdProvider


class FloatingAPIClient:
    def __init__(
        self,
        api_protocol: str = "http",
        api_domain: str = "localhost:8080",
        api_version: str = "v4",
        hardware_id_provider: HardwareIdProvider = HardwareIdProvider,
        certificate_chain_path: str = None,
        verify_license_signature=True,
    ):
        self.bearer_token = None
        self.hardware_id_provider = hardware_id_provider()
        self.signature_verifier = FSSignatureVerifier(certificate_chain_path)
        self.api_protocol = api_protocol
        self.api_domain = api_domain
        self.api_version = api_version
        self.api_base = f"{api_protocol}://{api_domain}/api/"
        self.verify_license_signature = verify_license_signature
        self._lock = threading.Lock()
        self.refresh_token_thread = None

    def start_refresh_token_background_task(self):
        """Starts the background thread that runs every 10 minutes."""
        if (
            self.refresh_token_thread is None
            or not self.refresh_token_thread.is_alive()
        ):
            self.refresh_token_thread = threading.Thread(
                target=self._refresh_token_task, daemon=True
            )
            self.refresh_token_thread.start()

    def _refresh_token_task(self):
        while True:
            time.sleep(600)  # 10 minutes
            with self._lock:
                logging.info("refreshing bearer token bcg_task")
                self.refresh_auth()

    def api_url(self, endpoint: str) -> str:
        return f"{self.api_base}{self.api_version}{endpoint}"

    def is_floating_server_v2(self):
        """Determine Floating server"""
        if not hasattr(self, "is_fs_v2"):
            response = requests.request(
                method="get",
                url=f"{self.api_protocol}://{self.api_domain}/api/v5/ping",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )
            try:
                data = response.json()
            except Exception:
                data = {}

            self.is_fs_v2 = True if data.get("message") == "pong" else False

            if self.is_fs_v2:
                self.api_version = "v5"

        return self.is_fs_v2

    def auth(
        self,
        username: str,
        password: str,
    ) -> dict:
        """
        Authenticate

        Args:
            username (str): username
            password (str): password

        Returns:
            dict: response
        """
        data = {"username": username, "password": password}
        if self.is_floating_server_v2():
            response = self.send_request(
                method="post", endpoint="/auth/login", json_data=data
            )

        else:
            response = requests.request(
                method="get",
                url=f"{self.api_protocol}://{self.api_domain}/auth",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                auth=HTTPBasicAuth(username, password),
            )

            if 400 <= response.status_code < 500:
                raise ClientError(response)
            else:
                response.raise_for_status()

        data = response.json()
        self.bearer_token = data.get("token")

        if self.is_floating_server_v2():
            self.start_refresh_token_background_task()

        return data

    def refresh_auth(self):
        """
        Refresh JWT token
        """
        response = self.send_request(method="post", endpoint="/auth/refresh")
        self.bearer_token = response.json().get("token")

    def request_hardware_data(
        self,
        data: dict,
        os_hostname: str = None,
        ip_local: str = None,
        user_info: str = None,
    ) -> dict:
        """
        Request hardware data

        Args:
            data (dict): data
            os_hostname (str, optional): os hostname. Defaults to None.
            ip_local (str, optional): ip local. Defaults to None.
            user_info (str, optional): user info. Defaults to None.

        Returns:
            dict: data
        """
        data["ip_local"] = ip_local
        data["user_info"] = user_info

        data["os_hostname"] = (
            os_hostname
            if os_hostname is not None
            else self.hardware_id_provider.get_hostname()
        )

        return data

    def request_version_data(self, data: dict, app_ver: str = None) -> dict:
        """
        Version data

        Args:
            data (dict): data
            app_ver (str, optional): app version. Defaults to None.

        Returns:
            dict: response
        """
        data["sdk_ver"] = f"PythonSDK {licensespring.version}"

        if app_ver:
            data["app_ver"] = app_ver
        elif licensespring.app_version:
            data["app_ver"] = licensespring.app_version

        return data

    def request_floating_data(
        self, data: dict, product: str, license_id: int = None, user: str = None
    ) -> dict:
        """
        request data for floating server communication

        Args:
            data (dict): data
            product (str): product short code
            license_id (int, optional): license id. Defaults to None.
            user (str, optional): hardware id. Defaults to None.

        Returns:
            dict: response
        """
        data["product"] = product
        data["user"] = user if user else self.hardware_id_provider.get_id()

        if license_id:
            data["license_id"] = license_id

        return data

    def request_floating_data_v2(self, data: dict, username: str = None):
        """
        request general data for floating server v2

        Args:
            data (dict): data
            username (str, optional): hardware id or user identifier. Defaults to None.
        """
        data["username"] = username if username else self.hardware_id_provider.get_id()

        return data

    def request_additional_data(self, data: dict, additional_data: dict) -> dict:
        """
        request additional data
        Args:
            data (dict): data
            additional_data (dict): additional data

        Returns:
            dict: data
        """
        for key, value in additional_data.items():
            if value is not None:
                data[key] = value
        return data

    def request_headers(self, custom_headers: dict = {}) -> dict:
        """
        request headers

        Args:
            custom_headers (dict, optional): custom headers. Defaults to {}.

        Returns:
            dict: headers
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        return {**headers, **custom_headers}

    def send_request(
        self,
        method: str,
        endpoint: str,
        custom_headers: dict = {},
        params: dict = None,
        data: dict = None,
        json_data: json = None,
    ):
        """
        Send request to FS server

        Args:
            method (str): method
            endpoint (str): endpoint
            custom_headers (dict, optional): custom headers. Defaults to {}.
            params (dict, optional): params. Defaults to None.
            data (dict, optional): data. Defaults to None.
            json_data (json, optional): json data. Defaults to None.

        Raises:
            ClientError: Error from FS

        Returns:
            dict: response
        """
        response = requests.request(
            method=method,
            url=self.api_url(endpoint),
            headers=self.request_headers(custom_headers=custom_headers),
            params=params,
            data=data,
            json=json_data,
        )
        if 400 <= response.status_code < 500:
            raise ClientError(response)
        else:
            response.raise_for_status()
        return response

    def register_user(
        self,
        product: str = None,
        user: str = None,
        license_id: int = None,
        os_hostname: str = None,
        ip_local: str = None,
        user_info: str = None,
        email: str = None,
    ) -> dict:
        """
        Register license

        Args:
            product (str): product short code
            user (str): user (default uses hardware id)
            license_id (int, optional): license id. Defaults to None.
            os_hostname (str, optional): hostname. Defaults to None.
            ip_local (str, optional): ip local. Defaults to None.
            user_info (str, optional): user info. Defaults to None.
            email (str, optional): email. Defaults to None.


        Returns:
            dict: response
        """
        data = self.request_version_data(data={})
        data = self.request_hardware_data(
            data=data, os_hostname=os_hostname, ip_local=ip_local, user_info=user_info
        )

        if self.is_floating_server_v2():
            data = self.request_floating_data_v2(data=data, username=user)
            data["email"] = email

            response = self.send_request(
                method="post",
                endpoint=f"/license/{license_id}/user/register",
                json_data=data,
            )

            if self.verify_license_signature:
                self.signature_verifier.verify_license_signature_v2(
                    response.content, response.headers.get("LicenseSignature")
                )

        else:
            data = self.request_floating_data(
                data=data,
                product=product,
                user=user,
                license_id=license_id,
            )

            response = self.send_request(
                method="post", endpoint="/register", json_data=data
            )

        return response.json()

    def unregister_user(
        self, product: str = None, user: str = None, license_id: int = None
    ) -> str:
        """
        unregister license

        Args:
            product (str): product short code
            user (str): user (default uses hardware id)
            license_id (int, optional): license id. Defaults to None.

        Returns:
            str: "user_unregistered"
        """
        data = self.request_version_data(data={})

        if self.is_floating_server_v2():
            data = self.request_floating_data_v2(data=data, username=user)

            response = self.send_request(
                method="post",
                endpoint=f"/license/{license_id}/user/unregister",
                json_data=data,
            )

        else:
            data = self.request_floating_data(
                data=data,
                product=product,
                user=user,
                license_id=license_id,
            )

            response = self.send_request(
                method="post", endpoint="/unregister", json_data=data
            )

        return response.content.decode()

    def unregister_all(self) -> str:
        """
        Unregister all

        Returns:
            str: ""
        """
        response = self.send_request(method="get", endpoint="/unregister/all")

        return response.content.decode()

    def borrow(
        self,
        product: str = None,
        borrowed_until: str = None,
        user: str = None,
        license_id: int = None,
        os_hostname: str = None,
        ip_local: str = None,
        user_info: str = None,
    ) -> dict:
        """
        Borrow license

        Args:
            product (str): product short code
            borrowed_until (str): borrow until (e.g. 2029-05-06T00:00:00Z)
            user (str, optional): user (default uses hardware id)
            license_id (int, optional): license id. Defaults to None.
            os_hostname (str, optional): os hostname. Defaults to None.
            ip_local (str, optional): local ip. Defaults to None.
            user_info (str, optional): user info. Defaults to None.

        Returns:
            dict: response
        """
        data = self.request_version_data(data={})
        data = self.request_hardware_data(
            data=data, os_hostname=os_hostname, ip_local=ip_local, user_info=user_info
        )
        data["borrowed_until"] = borrowed_until

        if self.is_floating_server_v2():
            data = self.request_floating_data_v2(data=data, username=user)

            response = self.send_request(
                method="post",
                endpoint=f"/license/{license_id}/user/borrow",
                json_data=data,
            )

            if self.verify_license_signature:
                self.signature_verifier.verify_license_signature_v2(
                    response.content, response.headers.get("LicenseSignature")
                )

        else:
            data = self.request_floating_data(
                data=data,
                product=product,
                user=user,
                license_id=license_id,
            )

            response = self.send_request(
                method="post", endpoint="/borrow", json_data=data
            )

        return response.json()

    def add_consumption(
        self,
        product: str = None,
        consumptions: int = 1,
        max_overages: int = None,
        allow_overages: bool = None,
        user: str = None,
        license_id: int = None,
    ) -> dict:
        """
        Add license consumptions

        Args:
            product (str): product short code
            consumptions (int, optional): consumptions. Defaults to 1.
            max_overages (int, optional): max overages. Defaults to None.
            allow_overages (bool, optional): allow overages. Defaults to None.
            user (str, optional): user (default uses hardware id)
            license_id (int, optional): license id. Defaults to None.

        Returns:
            dict: response
        """
        data = self.request_version_data(data={})
        data = self.request_additional_data(
            data=data,
            additional_data={
                "consumptions": consumptions,
                "max_overages": max_overages,
                "allow_overages": allow_overages,
            },
        )

        if self.is_floating_server_v2():
            data = self.request_floating_data_v2(data=data, username=user)
            response = self.send_request(
                method="post",
                endpoint=f"/license/{license_id}/consumption/add",
                json_data=data,
            )

            if self.verify_license_signature:
                self.signature_verifier.verify_license_signature_v2(
                    response.content, response.headers.get("LicenseSignature")
                )

        else:
            data = self.request_floating_data(
                data=data,
                product=product,
                user=user,
                license_id=license_id,
            )
            response = self.send_request(
                method="post", endpoint="/add_consumption", json_data=data
            )

        return response.json()

    def add_feature_consumption(
        self,
        product: str = None,
        feature_code: str = None,
        consumptions: int = 1,
        user: str = None,
        license_id: int = None,
    ) -> dict:
        """
        Add feature consumption

        Args:
            product (str): product short code
            feature_code (str): feature code
            user (str, optional): user (default uses hardware id)
            consumptions (int, optional): consumptions. Defaults to 1.
            license_id (int, optional): license id. Defaults to None.

        Returns:
            dict: response
        """
        data = self.request_version_data(data={})
        data = self.request_additional_data(
            data=data,
            additional_data={
                "consumptions": consumptions,
                "feature": feature_code,
            },
        )

        if self.is_floating_server_v2():
            data = self.request_floating_data_v2(data=data, username=user)
            response = self.send_request(
                method="post",
                endpoint=f"/license/{license_id}/consumption/feature/add",
                json_data=data,
            )

            if self.verify_license_signature:
                self.signature_verifier.verify_license_signature_v2(
                    response.content, response.headers.get("LicenseSignature")
                )

        else:
            data = self.request_floating_data(
                data=data,
                product=product,
                user=user,
                license_id=license_id,
            )

            response = self.send_request(
                method="post", endpoint="/add_feature_consumption", json_data=data
            )

        return response.json()

    def feature_register(
        self,
        product: str = None,
        feature_code: str = None,
        user: str = None,
        license_id: int = None,
        borrow_until: str = None,
        os_hostname: str = None,
        ip_local: str = None,
        user_info: str = None,
    ) -> dict:
        """
        Feature register

        Args:
            product (str): product short code
            feature_code (str): feature short code
            user (str, optional): user (default uses hardware id)
            license_id (int, optional): license id. Defaults to None.
            borrowed_until (str): borrow until (e.g. 2029-05-06T00:00:00Z)
            os_hostname (str, optional): os hostname. Defaults to None.
            ip_local (str, optional): ip local. Defaults to None.
            user_info (str, optional): user info. Defaults to None.

        Returns:
            dict: response
        """
        data = self.request_version_data(data={})
        data = self.request_additional_data(
            data=data,
            additional_data={"feature": feature_code, "borrow_until": borrow_until},
        )
        data = self.request_hardware_data(
            data=data, os_hostname=os_hostname, ip_local=ip_local, user_info=user_info
        )

        if self.is_floating_server_v2():
            data = self.request_floating_data_v2(data=data, username=user)

            response = self.send_request(
                method="post",
                endpoint=f"/license/{license_id}/feature/register",
                json_data=data,
            )

            if self.verify_license_signature:
                self.signature_verifier.verify_license_signature_v2(
                    response.content, response.headers.get("LicenseSignature")
                )
        else:
            data = self.request_floating_data(
                data=data,
                product=product,
                user=user,
                license_id=license_id,
            )

            response = self.send_request(
                method="post", endpoint="/featureRegister", json_data=data
            )

        return response.json()

    def feature_release(
        self,
        product: str = None,
        feature_code: str = None,
        user: str = None,
        license_id: int = None,
    ) -> str:
        """
        Feature release

        Args:
            product (str): product short code
            feature_code (str): feature short code
            user (str, optional): user (default uses hardware id)
            license_id (int, optional): license id. Defaults to None.

        Returns:
            str: "feature_released"
        """
        data = self.request_version_data(data={})

        data = self.request_additional_data(
            data=data,
            additional_data={"feature": feature_code},
        )

        if self.is_floating_server_v2():
            data = self.request_floating_data_v2(data=data, username=user)
            response = self.send_request(
                method="post",
                endpoint=f"/license/{license_id}/feature/release",
                json_data=data,
            )

        else:
            data = self.request_floating_data(
                data=data, product=product, user=user, license_id=license_id
            )

            response = self.send_request(
                method="post", endpoint="/featureRelease", json_data=data
            )

        return response.content.decode()

    def fetch_licenses(self, product: str = None):
        if self.is_floating_server_v2():
            response = self.send_request(
                method="get", endpoint=f"/license", params=product
            )
            return response.json()
