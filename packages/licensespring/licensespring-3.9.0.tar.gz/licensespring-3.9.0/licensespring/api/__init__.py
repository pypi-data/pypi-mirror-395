import base64
import json
from collections import OrderedDict
from datetime import datetime, timedelta, timezone

import requests

import licensespring
from licensespring.api.authorization import (
    authorization_headers_oauth,
    autorization_headers,
    date_header_value,
    offline_signature,
    offline_signature_v2,
)
from licensespring.api.error import ClientError, InvalidClientCredentials
from licensespring.api.signature import SignatureVerifier
from licensespring.hardware import HardwareIdProvider


class APIClient:
    def __init__(
        self,
        api_key=None,
        shared_key=None,
        hardware_id_provider=HardwareIdProvider,
        verify_license_signature=True,
        signature_verifier=SignatureVerifier,
        api_protocol="https",
        api_domain="api.licensespring.com",
        api_version="v4",
        client_id=None,
        client_secret=None,
    ):
        self.api_key = api_key
        self.shared_key = shared_key

        self.client_id = client_id
        self.client_secret = client_secret
        self.validate_auth()

        self.hardware_id_provider = hardware_id_provider()

        self.verify_license_signature = verify_license_signature
        self.signature_verifier = signature_verifier()

        self.api_protocol = api_protocol
        self.api_domain = api_domain
        self.api_version = api_version
        self.api_base = f"{api_protocol}://{api_domain}/api/{api_version}"

        self.token = None
        self.token_validity = datetime.now(timezone.utc)

    @property
    def is_oauth(self):
        return True if self.client_id and self.client_secret else False

    def validate_auth(self):
        if not (
            (self.client_id and self.client_secret)
            or (self.api_key and self.shared_key)
        ):
            raise Exception(
                "Either (client_id and client_secret) or (api_key and shared_key) must be provided."
            )

    def api_url(self, endpoint):
        return f"{self.api_base}{endpoint}"

    def update_bearer_token(self):
        url = f"{self.api_base}/oauth_url?login_type=client_credentials"
        keyk_url = requests.get(url).json()["url"]

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.post(
            keyk_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
        )

        if 400 <= response.status_code < 500:
            error_code = response.json().get("error")

            if error_code in ["invalid_client", "unauthorized_client"]:
                raise InvalidClientCredentials(response)
        else:
            response.raise_for_status()

        self.token_validity = datetime.now(timezone.utc) + timedelta(
            seconds=response.json()["expires_in"] - 5
        )
        self.token = response.json()["access_token"]

    def get_bearer_token(self):
        if self.token == None or self.token_validity < datetime.now(timezone.utc):
            self.update_bearer_token()

        return self.token

    def request_headers(self, custom_headers={}):
        if self.is_oauth:
            token = self.get_bearer_token()
            authorization_headers = authorization_headers_oauth(token)
        else:
            authorization_headers = autorization_headers(self.api_key, self.shared_key)

        headers = {"Content-Type": "application/json"}
        return {**headers, **authorization_headers, **custom_headers}

    def request_generic_data(
        self,
        data,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        password=None,
    ):
        data["product"] = product
        if bundle_code:
            data["bundle_code"] = bundle_code

        data["hardware_id"] = (
            hardware_id if hardware_id else self.hardware_id_provider.get_id()
        )

        if license_key:
            data["license_key"] = license_key
        if license_id:
            data["license_id"] = license_id
        if username:
            data["username"] = username
        if password:
            data["password"] = password

        return data

    def request_sso_data(
        self, data, customer_account_code=None, id_token=None, code=None
    ):
        if customer_account_code:
            data["customer_account_code"] = customer_account_code
            if code:
                data["code"] = code
            elif id_token:
                data["id_token"] = id_token

        return data

    def request_additional_data(self, data, additional_data):
        for key, value in additional_data.items():
            if value is not None:
                data[key] = value
        return data

    def request_hardware_data(
        self,
        data,
        os_ver=None,
        hostname=None,
        ip=None,
        mac_address=None,
    ):
        data["os_ver"] = (
            os_ver if os_ver is not None else self.hardware_id_provider.get_os_ver()
        )
        data["hostname"] = (
            hostname
            if hostname is not None
            else self.hardware_id_provider.get_hostname()
        )
        data["ip"] = ip if ip is not None else self.hardware_id_provider.get_ip()
        data["mac_address"] = (
            mac_address
            if mac_address is not None
            else self.hardware_id_provider.get_mac_address()
        )

        return data

    def request_vm_data(self, data, is_vm=None, vm_info=None):
        data["is_vm"] = (
            is_vm if is_vm is not None else self.hardware_id_provider.get_is_vm()
        )
        data["vm_info"] = (
            vm_info if vm_info is not None else self.hardware_id_provider.get_vm_info()
        )

        return data

    def request_version_data(self, data, app_ver=None):
        data["sdk_ver"] = f"PythonSDK {licensespring.version}"

        if app_ver:
            data["app_ver"] = app_ver
        elif licensespring.app_version:
            data["app_ver"] = licensespring.app_version

        return data

    def send_request(
        self,
        method,
        endpoint,
        custom_headers={},
        params=None,
        data=None,
        json_data=None,
    ):
        response = requests.request(
            method=method,
            url=self.api_url(endpoint),
            headers=self.request_headers(custom_headers=custom_headers),
            params=params,
            data=data,
            json=json_data,
        )

        if 400 <= response.status_code < 500:
            if response.json()["code"] in [
                "oauth_token_expired",
                "oauth_token_malformed",
            ]:
                self.update_bearer_token()
                return self.send_request(
                    method=method,
                    endpoint=endpoint,
                    custom_headers=custom_headers,
                    params=params,
                    data=data,
                    json_data=json_data,
                )
            else:
                raise ClientError(response)
        else:
            response.raise_for_status()

        return response

    def activate_license(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        password=None,
        customer_account_code=None,
        id_token=None,
        code=None,
        app_ver=None,
        os_ver=None,
        hostname=None,
        ip=None,
        is_vm=None,
        vm_info=None,
        mac_address=None,
        variables=None,
    ):
        data = self.request_generic_data(
            {},
            product,
            bundle_code,
            hardware_id,
            license_key,
            license_id,
            username,
            password,
        )
        data = self.request_sso_data(
            data,
            customer_account_code=customer_account_code,
            id_token=id_token,
            code=code,
        )
        data = self.request_hardware_data(
            data=data,
            os_ver=os_ver,
            hostname=hostname,
            ip=ip,
            mac_address=mac_address,
        )
        data = self.request_vm_data(data, is_vm=is_vm, vm_info=vm_info)
        data = self.request_version_data(data, app_ver=app_ver)
        data = self.request_additional_data(
            data=data,
            additional_data={
                "variables": variables,
            },
        )

        response = self.send_request(
            method="post",
            endpoint="/activate_license",
            json_data=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def activate_bundle(
        self,
        product,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        password=None,
        customer_account_code=None,
        id_token=None,
        code=None,
        app_ver=None,
        os_ver=None,
        hostname=None,
        ip=None,
        is_vm=None,
        vm_info=None,
        mac_address=None,
        variables=None,
    ):

        data = self.request_generic_data(
            {},
            product,
            None,
            hardware_id,
            license_key,
            license_id,
            username,
            password,
        )
        data = self.request_sso_data(
            data,
            customer_account_code=customer_account_code,
            id_token=id_token,
            code=code,
        )
        data = self.request_hardware_data(
            data=data,
            os_ver=os_ver,
            hostname=hostname,
            ip=ip,
            mac_address=mac_address,
        )
        data = self.request_vm_data(data, is_vm=is_vm, vm_info=vm_info)
        data = self.request_version_data(data, app_ver=app_ver)
        data = self.request_additional_data(
            data=data,
            additional_data={
                "variables": variables,
            },
        )

        response = self.send_request(
            method="post",
            endpoint="/activate_bundle",
            json_data=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def deactivate_bundle(
        self,
        product,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
    ):
        data = self.request_generic_data(
            {}, product, None, hardware_id, license_key, license_id, username
        )

        response = self.send_request(
            method="post",
            endpoint="/deactivate_bundle",
            json_data=data,
        )
        return response.content.decode()

    def check_bundle(
        self,
        product,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        include_expired_features=None,
        env=None,
    ):

        data = self.request_generic_data(
            {},
            product,
            None,
            hardware_id,
            license_key,
            license_id,
            username,
            None,
        )

        data = self.request_additional_data(
            data=data,
            additional_data={
                "include_expired_features": (
                    "true" if include_expired_features else "false"
                ),
                "env": env,
            },
        )

        response = self.send_request(
            method="get",
            endpoint="/check_bundle",
            params=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def deactivate_license(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
    ):
        data = self.request_generic_data(
            {}, product, bundle_code, hardware_id, license_key, license_id, username
        )

        response = self.send_request(
            method="post",
            endpoint="/deactivate_license",
            json_data=data,
        )
        return response.content.decode()

    def check_license(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        include_expired_features=None,
        env=None,
    ):
        data = self.request_generic_data(
            {},
            product,
            bundle_code,
            hardware_id,
            license_key,
            license_id,
            username,
            None,
        )

        data = self.request_additional_data(
            data=data,
            additional_data={
                "include_expired_features": (
                    "true" if include_expired_features else "false"
                ),
                "env": env,
            },
        )

        response = self.send_request(
            method="get",
            endpoint="/check_license",
            params=data,
        )
        response_json = response.json()

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response_json

    def activate_offline_dump(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        password=None,
        app_ver=None,
        os_ver=None,
        hostname=None,
        ip=None,
        is_vm=None,
        vm_info=None,
        mac_address=None,
        variables=None,
    ):
        data = {"request": "activation"}
        data = self.request_generic_data(
            data,
            product,
            bundle_code,
            hardware_id,
            license_key,
            license_id,
            username,
            password,
        )
        data = self.request_hardware_data(
            data=data,
            os_ver=os_ver,
            hostname=hostname,
            ip=ip,
            mac_address=mac_address,
        )
        data = self.request_vm_data(data, is_vm=is_vm, vm_info=vm_info)
        data = self.request_version_data(data, app_ver=app_ver)
        data = self.request_additional_data(
            data=data,
            additional_data={
                "variables": variables,
            },
        )
        data["date"] = date_header_value()

        data["request_id"] = self.hardware_id_provider.get_request_id()
        data["schema_version"] = 2

        if self.is_oauth:
            data["signature"] = offline_signature(
                self.client_id,
                self.client_secret,
                data["hardware_id"],
                license_key,
                username,
            )
            data["client_id"] = self.client_id
            new_signature = offline_signature_v2(
                key=self.client_id, data=json.dumps(data)
            )
        else:
            data["signature"] = offline_signature(
                self.api_key,
                self.shared_key,
                data["hardware_id"],
                license_key,
                username,
            )
            data["api_key"] = self.api_key
            new_signature = offline_signature_v2(
                key=self.shared_key, data=json.dumps(data)
            )

        data = {"request": data, "signature": new_signature}

        return base64.b64encode(json.dumps(data).encode()).decode()

    def activate_offline_load(self, data):
        decoded_data = base64.b64decode(data).decode()
        response_json = json.loads(decoded_data)

        if self.verify_license_signature:
            response_json_sig_v2_check_data = json.loads(
                decoded_data, object_pairs_hook=OrderedDict
            )
            response_json_sig_v2_check_data.pop("license_signature")
            license_signature_v2 = response_json_sig_v2_check_data.pop(
                "license_signature_v2"
            )
            response_json_sig_v2_check_string = json.dumps(
                response_json_sig_v2_check_data,
                separators=(",", ":"),
                ensure_ascii=False,
            )
            self.signature_verifier.verify_license_signature_v2(
                response_json_sig_v2_check_string.encode(), license_signature_v2
            )

        return response_json

    def check_offline_load(self, data):
        decoded_data = base64.b64decode(data).decode()
        response_json = json.loads(decoded_data)

        if self.verify_license_signature:
            response_json_sig_v2_check_data = json.loads(
                decoded_data, object_pairs_hook=OrderedDict
            )
            license_signature_v2 = response_json_sig_v2_check_data.pop(
                "license_signature_v2"
            )
            response_json_sig_v2_check_string = json.dumps(
                response_json_sig_v2_check_data,
                separators=(",", ":"),
                ensure_ascii=False,
            )
            self.signature_verifier.verify_license_signature_v2(
                response_json_sig_v2_check_string.encode(), license_signature_v2
            )

        return response_json

    def activate_offline(self, data):
        response = self.send_request(
            method="post",
            endpoint="/activate_offline",
            custom_headers={"Content-type": "text/plain"},
            data=data,
        )
        response_json = response.json()

        if self.verify_license_signature:
            response_json_sig_v2_check_data = response.json(
                object_pairs_hook=OrderedDict
            )
            response_json_sig_v2_check_data.pop("license_signature")
            license_signature_v2 = response_json_sig_v2_check_data.pop(
                "license_signature_v2"
            )
            response_json_sig_v2_check_string = json.dumps(
                response_json_sig_v2_check_data,
                separators=(",", ":"),
                ensure_ascii=False,
            )
            self.signature_verifier.verify_license_signature_v2(
                response_json_sig_v2_check_string.encode(), license_signature_v2
            )

        return response_json

    def deactivate_offline_dump(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        app_ver=None,
        os_ver=None,
        hostname=None,
        ip=None,
        mac_address=None,
        consumptions=None,
        product_features=None,
    ):
        data = {"request": "deactivation"}
        data = self.request_generic_data(
            data, product, bundle_code, hardware_id, license_key, license_id, username
        )
        data = self.request_hardware_data(
            data=data,
            os_ver=os_ver,
            hostname=hostname,
            ip=ip,
            mac_address=mac_address,
        )
        data = self.request_version_data(data, app_ver=app_ver)

        data = self.request_additional_data(
            data=data,
            additional_data={
                "consumptions": consumptions,
                "product_features": product_features,
            },
        )

        data["date"] = date_header_value()
        data["request_id"] = self.hardware_id_provider.get_request_id()

        data["schema_version"] = 2

        if self.is_oauth:
            data["signature"] = offline_signature(
                self.client_id,
                self.client_secret,
                data["hardware_id"],
                license_key,
                username,
            )
            data["client_id"] = self.client_id
            new_signature = offline_signature_v2(
                key=self.client_id, data=json.dumps(data, ensure_ascii=False)
            )
        else:
            data["signature"] = offline_signature(
                self.api_key,
                self.shared_key,
                data["hardware_id"],
                license_key,
                username,
            )
            data["api_key"] = self.api_key
            new_signature = offline_signature_v2(
                key=self.shared_key, data=json.dumps(data, ensure_ascii=False)
            )

        data = {"request": data, "signature": new_signature}

        return base64.b64encode(json.dumps(data, ensure_ascii=False).encode()).decode()

    def deactivate_offline(self, data):
        response = self.send_request(
            method="post",
            endpoint="/deactivate_offline",
            custom_headers={"Content-type": "text/plain"},
            data=data,
        )

        return response.content.decode()

    def add_consumption(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        consumptions=None,
        max_overages=None,
        allow_overages=None,
    ):
        data = self.request_generic_data(
            {}, product, bundle_code, hardware_id, license_key, license_id, username
        )
        data = self.request_additional_data(
            data=data,
            additional_data={
                "consumptions": consumptions,
                "max_overages": max_overages,
                "allow_overages": allow_overages,
            },
        )

        response = self.send_request(
            method="post",
            endpoint="/add_consumption",
            json_data=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def add_feature_consumption(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        feature=None,
        consumptions=None,
    ):
        data = self.request_generic_data(
            {}, product, bundle_code, hardware_id, license_key, license_id, username
        )
        data["feature"] = feature
        data = self.request_additional_data(
            data=data,
            additional_data={
                "consumptions": consumptions,
            },
        )

        response = self.send_request(
            method="post",
            endpoint="/add_feature_consumption",
            json_data=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def trial_key(
        self,
        product,
        hardware_id=None,
        email=None,
        license_policy=None,
        first_name=None,
        last_name=None,
        phone=None,
        address=None,
        postcode=None,
        state=None,
        country=None,
        city=None,
        reference=None,
    ):
        data = self.request_generic_data({}, product, hardware_id=hardware_id)
        data = self.request_additional_data(
            data=data,
            additional_data={
                "email": email,
                "license_policy": license_policy,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "address": address,
                "postcode": postcode,
                "state": state,
                "country": country,
                "city": city,
                "reference": reference,
            },
        )

        response = self.send_request(
            method="get",
            endpoint="/trial_key",
            params=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def product_details(
        self,
        product,
        include_latest_version=False,
        include_custom_fields=False,
        env=None,
    ):
        data = {"product": product}
        data = self.request_additional_data(
            data=data,
            additional_data={
                "include_latest_version": "true" if include_latest_version else "false",
                "include_custom_fields": "true" if include_custom_fields else "false",
                "env": env,
            },
        )

        response = self.send_request(
            method="get",
            endpoint="/product_details",
            params=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def track_device_variables(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        variables=None,
    ):
        data = self.request_generic_data(
            {},
            product,
            bundle_code,
            hardware_id,
            license_key,
            license_id,
            username,
            None,
        )
        data["variables"] = variables

        response = self.send_request(
            method="post",
            endpoint="/track_device_variables",
            json_data=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def floating_release(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
    ):
        data = self.request_generic_data(
            {},
            product,
            bundle_code,
            hardware_id,
            license_key,
            license_id,
            username,
            None,
        )

        response = self.send_request(
            method="post",
            endpoint="/floating/release",
            json_data=data,
        )

        return response.content.decode()

    def floating_borrow(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        password=None,
        borrowed_until=None,
    ):
        data = self.request_generic_data(
            {},
            product,
            bundle_code,
            hardware_id,
            license_key,
            license_id,
            username,
            password,
        )
        data["borrowed_until"] = borrowed_until

        response = self.send_request(
            method="post",
            endpoint="/floating/borrow",
            json_data=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def change_password(self, username, password, new_password):
        data = {
            "username": username,
            "password": password,
            "new_password": new_password,
        }

        response = self.send_request(
            method="post",
            endpoint="/change_password",
            json_data=data,
        )

        return response.content.decode()

    def versions(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        env=None,
        channel=None,
    ):
        data = self.request_generic_data(
            {},
            product,
            bundle_code,
            hardware_id,
            license_key,
            license_id,
            username,
        )
        data = self.request_additional_data(
            data=data,
            additional_data={"env": env, "channel": channel},
        )

        response = self.send_request(
            method="get",
            endpoint="/versions",
            params=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def installation_file(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
        env=None,
        version=None,
        channel=None,
    ):
        data = self.request_generic_data(
            {},
            product,
            bundle_code,
            hardware_id,
            license_key,
            license_id,
            username,
        )
        data = self.request_additional_data(
            data=data,
            additional_data={"env": env, "version": version, "channel": channel},
        )

        response = self.send_request(
            method="get",
            endpoint="/installation_file",
            params=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def customer_license_users(self, product, customer):
        data = {
            "product": product,
            "customer": customer,
        }

        response = self.send_request(
            method="get",
            endpoint="/customer_license_users",
            params=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def user_licenses(self, product, username, password):
        data = {"product": product, "username": username, "password": password}

        response = self.send_request(
            method="get", endpoint="/user_licenses", params=data
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def sso_url(self, product, customer_account_code, response_type="token"):
        data = {
            "product": product,
            "customer_account_code": customer_account_code,
            "response_type": response_type,
        }

        response = self.send_request(
            method="get",
            endpoint="/sso_url",
            params=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def get_device_variables(
        self,
        product,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
    ):
        data = self.request_generic_data(
            {},
            product,
            bundle_code,
            hardware_id,
            license_key,
            license_id,
            username,
            None,
        )

        response = self.send_request(
            method="get",
            endpoint="/get_device_variables",
            params=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def check_license_feature(
        self,
        product,
        feature,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
    ):
        data = self.request_generic_data(
            {},
            product,
            bundle_code,
            hardware_id,
            license_key,
            license_id,
            username,
            None,
        )
        data = self.request_additional_data(
            data=data,
            additional_data={
                "feature": feature,
            },
        )
        response = self.send_request(
            method="get",
            endpoint="/check_license_feature",
            params=data,
        )

        if self.verify_license_signature:
            self.signature_verifier.verify_license_signature_v2(
                response.content, response.headers.get("LicenseSignature")
            )

        return response.json()

    def floating_feature_release(
        self,
        product,
        feature,
        bundle_code=None,
        hardware_id=None,
        license_key=None,
        license_id=None,
        username=None,
    ):
        data = self.request_generic_data(
            {},
            product,
            bundle_code,
            hardware_id,
            license_key,
            license_id,
            username,
            None,
        )
        data = self.request_additional_data(
            data=data,
            additional_data={
                "feature": feature,
            },
        )

        response = self.send_request(
            method="post",
            endpoint="/floating/feature_release",
            json_data=data,
        )

        return response.content.decode()
