import logging
import os
from typing import Dict, List

import requests

from licensespring.licensefile import License
from licensespring.licensefile.base_manager import BaseManager
from licensespring.licensefile.config import Configuration
from licensespring.licensefile.customer import Customer
from licensespring.licensefile.error import ErrorType, LicenseActivationException
from licensespring.licensefile.offline_activation_guard import OfflineActivation


class LicenseID:
    """
    Represents a mechanism for license identification and activation.

    The LicenseID class provides a structured way to handle both key-based and user-based
    license activations. It encapsulates the necessary details for each activation method,
    allowing for clear and concise license management within applications.

    Attributes:
        key (str, optional): The license key for key-based activation. Defaults to None.
        username (str, optional): The username (typically an email) for user-based activation. Defaults to None.
        password (str, optional): The password associated with the username for user-based activation. Defaults to None.

    Methods:
        from_key: Class method to create a LicenseID instance for key-based activation.
        from_user: Class method to create a LicenseID instance for user-based activation.
    """

    def __init__(self) -> None:
        self.key = None
        self.username = None
        self.password = None

    @classmethod
    def from_key(cls, key):
        """
        Creates an instance of LicenseID for a key-based license.

        Parameters:
            key (str): license key

        Returns:
            LicenseID
        """
        licenseID = cls()
        licenseID.key = key
        return licenseID

    @classmethod
    def from_user(cls, username, password=None):
        """
        Creates an instance of LicenseID for a user-based license.

        Parameters:
            username (str): email of an user
            password (str): password

        Returns:
            LicenseID
        """
        licenseID = cls()
        licenseID.username = username
        licenseID.password = password
        return licenseID


class LicenseManager(BaseManager):
    """
    LicenseManager is used for license activation

    Attributes:
        api_client (APIClient): An instance of the APIClient responsible for API communication.
        _product (str): LicenseSpring product.
        licensefile_handler (DataStorage): A data storage handler for managing
            license file operations.

    Parameters:
        conf (Configuration): A configuration object containing necessary parameters
            such as API keys, hardware ID provider, and other settings required
            for license activation and verification.
    """

    def __init__(
        self,
        conf: Configuration,
    ) -> None:
        super().__init__(conf)

    def activate_license(
        self,
        license_id: LicenseID,
        bundle_code: str = None,
        hardware_id: str = None,
        unique_license_id: int = None,
        customer_account_code: str = None,
        id_token: str = None,
        code: str = None,
        app_ver: str = None,
        os_ver: str = None,
        hostname: str = None,
        ip: str = None,
        is_vm: bool = None,
        vm_info: str = None,
        mac_address: str = None,
    ) -> License:
        """
        Activates a license with the license server and updates local license data accordingly.

        This method supports a variety of parameters to accommodate different licensing scenarios,
        including key-based activation, user-based activation

        Args:
            license_id (LicenseID): An instance containing the license key or user credentials.
            bundle_code (str, optional): specify unique bundle_code of a bundle
            hardware_id (str, optional): A unique identifier for the hardware.
            unique_license_id (int, optional): A unique identifier for the license.
            customer_account_code (str, optional): An account code for the customer.
            id_token (str, optional): Token for identity verification.
            code (str, optional): An additional code for license verification.
            app_ver (str, optional): The version of the application requesting activation.
            os_ver (str, optional): The operating system version of the host.
            hostname (str, optional): The hostname of the device requesting activation.
            ip (str, optional): The IP address of the device.
            is_vm (bool, optional): Indicates whether the application is running on a virtual machine.
            vm_info (str, optional): Information about the virtual machine, if applicable.
            mac_address (str, optional): The MAC address of the device.

        Returns:
            License: An instance of the License class reflecting the activated license.
        """

        response = self.api_client.activate_license(
            product=self._conf._product,
            bundle_code=bundle_code,
            hardware_id=hardware_id,
            license_key=license_id.key,
            license_id=unique_license_id,
            username=license_id.username,
            password=license_id.password,
            customer_account_code=customer_account_code,
            id_token=id_token,
            code=code,
            app_ver=app_ver,
            os_ver=os_ver,
            hostname=hostname,
            ip=ip,
            is_vm=is_vm,
            vm_info=vm_info,
            mac_address=mac_address,
        )

        response["username"] = license_id.username
        response["bundle_code"] = bundle_code
        self.licensefile_handler._cache.update_cache("activate_license", response)
        self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

        return License(
            self._conf._product,
            api_client=self.api_client,
            licensefile_handler=self.licensefile_handler,
        )

    def is_online(self, throw_e=True) -> bool:
        """
        Check if system is online.

        Args:
            throw_e (bool, optional): When True exception will be raised, otherwise False. Defaults to True.

        Raises:
            ex: Request Exception

        Returns:
            bool: True if system is online otherwise False.
        """
        try:
            response = requests.get(
                f"{self.api_client.api_protocol}://{self.api_client.api_domain}"
            )

            if response.status_code == 200:
                return True

        except Exception as ex:
            if throw_e:
                raise ex

        return False

    def create_offline_activation_file(
        self,
        license_id: LicenseID,
        req_path: str,
        bundle_code: str = None,
        hardware_id: str = None,
        unique_license_id: int = None,
        app_ver: str = None,
        os_ver: str = None,
        hostname: str = None,
        ip: str = None,
        is_vm: bool = None,
        vm_info: str = None,
        mac_address: str = None,
        device_variables: dict = None,
    ) -> str:
        """
        Creates .req file for activation

        Args:
            license_id (LicenseID): An instance containing the license key or user credentials.
            req_path (str): Specify place where to create .req file
            bundle_code (str, optional): specify unique bundle_code of a bundle.
            hardware_id (str, optional): A unique identifier for the hardware.
            app_ver (str, optional): The version of the application requesting activation.
            os_ver (str, optional): The operating system version of the host.
            hostname (str, optional): The hostname of the device requesting activation.
            ip (str, optional):  The IP address of the device.
            is_vm (bool, optional): Indicates whether the application is running on a virtual machine.
            vm_info (str, optional): Information about the virtual machine.
            mac_address (str, optional): The MAC address of the device.
            device_variables (dict, optional): device varaibles.

        Returns:
            str: path of the .req file
        """

        data = self.api_client.activate_offline_dump(
            product=self._conf._product,
            bundle_code=bundle_code,
            hardware_id=hardware_id,
            license_key=license_id.key,
            license_id=unique_license_id,
            username=license_id.username,
            password=license_id.password,
            app_ver=app_ver,
            os_ver=os_ver,
            hostname=hostname,
            ip=ip,
            is_vm=is_vm,
            vm_info=vm_info,
            mac_address=mac_address,
            variables=device_variables,
        )

        offline_data = OfflineActivation()
        offline_data.set_data(data)
        offline_data.set_is_activation(True)
        offline_data.create_guard_file(
            self.api_client.create_activation_guard(
                offline_data.decode_offline_activation()["request"]["request_id"]
            )
        )

        return self.licensefile_handler.create_request_file(
            req_data=offline_data, offline_path=req_path
        )

    def activate_license_offline(self, ls_activation_path: str) -> License:
        """
        Activates a .lic

        Args:
            ls_activation_path (str): path to activation file

        Raises:
            LicenseActivationException: Activation data is not valid
            LicenseActivationException: Response file ID mismatch
            LicenseActivationException: License does not belong to this device

        Returns:
            License: License object
        """

        data = self.licensefile_handler.load_offline_response(ls_activation_path)

        if len(data._data) == 0:
            return

        response = self.api_client.activate_license_offline(data=data)
        self.licensefile_handler._cache.update_cache(
            "activate_license_offline", response
        )
        license = License(
            self._conf._product,
            api_client=self.api_client,
            licensefile_handler=self.licensefile_handler,
        )
        license.licensefile_handler.save_licensefile(self.licensefile_handler._cache)
        self.licensefile_handler.remove_offline_activation_data(ls_activation_path)
        logging.info("Offline activation succeeded")

        return license

    def get_air_gap_activation_code(
        self, initialization_code: str, license_key: str
    ) -> str:
        """
        Get activation code

        Args:
            initialization_code (str): initialization code
            license_key (str): license key

        Returns:
            str: activation code
        """
        res = self.api_client.get_air_gap_activation_code(
            initialization_code=initialization_code, license_key=license_key
        )
        guard = self.api_client.create_activation_guard(license_key)
        self.licensefile_handler.save_guard_file(guard)

        return res

    def activate_air_gap_license(
        self, confirmation_code: str, policy_path: str, license_key: str, policy_id: str
    ) -> License:
        """
        Activate air gap license

        Args:
            confirmation_code (str): confirmation code
            policy_path (str): policy path (file or folder)
            license_key (str): license_key
            policy_id (str): policy id

        Raises:
            LicenseActivationException: Signature verification fail

        Returns:
            License: License
        """
        if not self.api_client.verify_confirmation_code(
            confirmation_code=confirmation_code,
            license_key=license_key,
            policy_id=policy_id,
        ):
            raise LicenseActivationException(
                error_type=ErrorType.AIR_GAP_ACTIVATION_ERROR,
                message="VerificationError",
            )

        if os.path.exists(policy_path) and os.path.isfile(policy_path):
            data = self.licensefile_handler.load_offline_response(policy_path)

            if len(data._data) == 0:
                return

            response = self.api_client.activate_air_gapped_licenses(
                data=data, license_key=license_key, policy_id=policy_id
            )

        else:
            for file in [f for f in os.listdir(policy_path) if f.endswith(".lic")]:
                logging.info("Policy file path: ", file)
                data = self.licensefile_handler.load_offline_response(
                    os.path.join(policy_path, file)
                )

                if not len(data._data) == 0:
                    try:
                        response = self.api_client.activate_air_gapped_licenses(
                            data=data, license_key=license_key, policy_id=policy_id
                        )

                        if response:
                            break

                    except LicenseActivationException:
                        pass

        if response:
            self.licensefile_handler._cache.update_cache("activate_air_gap", response)
            license = License(
                self._conf._product,
                api_client=self.api_client,
                licensefile_handler=self.licensefile_handler,
            )

            license.licensefile_handler.save_licensefile(
                self.licensefile_handler._cache
            )

            return license

    def get_trial_license(
        self, customer: Customer, license_policy: str = None
    ) -> LicenseID:
        """
        Creates LiceseID for trial licenses

        Args:
            customer (Customer): Customer object
            license_policy (str, optional): license policy code. Defaults to None.

        Returns:
            LicenseID
        """

        response = self.api_client.trial_key(
            self._conf._product,
            hardware_id=None,
            email=customer.email,
            license_policy=license_policy,
            first_name=customer.first_name,
            last_name=customer.last_name,
            phone=customer.phone,
            address=customer.address,
            postcode=customer.postcode,
            state=customer.state,
            country=customer.country,
            city=customer.city,
            reference=customer.reference,
        )

        if "license" in response:
            return LicenseID.from_key(response["license"])

        else:
            return LicenseID.from_user(
                response["license_user"], response["initial_password"]
            )

    def get_version_list(
        self,
        license_id: LicenseID,
        channel: str = None,
        unique_license_id: int = None,
        env: str = None,
    ) -> List[Dict]:
        """
        Get versions

        Args:
            license_id (LicenseID): An instance containing the license key or user credentials.
            unique_license_id (int, optional): A unique identifier for the license.
            env (str,optional): Version of environment
            channel (str, optional): channel of the version

        Returns:
            dict: response
        """
        return self.api_client.versions(
            product=self._conf._product,
            hardware_id=None,
            license_key=license_id.key,
            license_id=unique_license_id,
            username=license_id.username,
            env=env,
            channel=channel,
        )

    def get_installation_file(
        self,
        license_id: LicenseID,
        unique_license_id: int = None,
        env: str = None,
        version: str = None,
        channel: str = None,
    ) -> dict:
        """
        Get installation file

        Args:
            license_id (LicenseID): An instance containing the license key or user credentials
            channel (str, optional): channel of the version
            unique_license_id (int, optional): A unique identifier for the license.
            env (str, optional): Version of environment
            version (str, optional): Versions

        Returns:
            dict: installation file
        """

        return self.api_client.installation_file(
            product=self._conf._product,
            hardware_id=None,
            license_key=license_id.key,
            license_id=unique_license_id,
            username=license_id.username,
            env=env,
            version=version,
            channel=channel,
        )

    def get_customer_license_users(self, customer: Customer) -> dict:
        """
        Get customer license users

        Args:
            customer (Customer): customer

        Returns:
            dict: response
        """

        return self.api_client.customer_license_users(
            self._conf._product, customer=customer.email
        )

    def get_user_licenses(self, license_id: LicenseID) -> list:
        """
        Get User licenses

        Args:
            license_id (LicenseID): license_id

        Returns:
            list: User licenses
        """

        return self.api_client.user_licenses(
            product=self._conf._product,
            username=license_id.username,
            password=license_id.password,
        )

    def get_sso_url(self, account_code: str, use_auth_code: bool = True) -> str:
        """
        Get SSO url

        Args:
            account_code (str): account code
            use_auth_code (bool, optional): Use code for response_type. Defaults to True.
        """
        response_type = "code" if use_auth_code else "token"
        return self.api_client.sso_url(
            product=self._conf._product,
            customer_account_code=account_code,
            response_type=response_type,
        )
