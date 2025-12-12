import copy
import json
import logging

from licensespring.licensefile import License
from licensespring.licensefile.base_manager import BaseManager
from licensespring.licensefile.config import Configuration
from licensespring.licensefile.data_storage import DataStorage
from licensespring.licensefile.license_manager import LicenseID
from licensespring.licensefile.offline_activation_guard import OfflineActivation


class BundleManager(BaseManager):
    def __init__(self, conf: Configuration):
        super().__init__(conf)
        self.cache_licenses = None

    def get_current_bundle(self) -> dict[str, License]:
        """
        Retrieve a dictionary of bundled licenses.

        Returns:
            dict: A dictionary where the keys are product short codes and the values are License objects.
        """
        if not self.cache_licenses:
            self.cache_licenses = self.load_bundles()
        return self.cache_licenses

    def load_bundles(self) -> dict[str, License]:
        """
        Load bundles from a file

        Returns:
            dict: A dictionary where the keys are product short codes and the values are License objects.
        """
        cache_licenses = {}

        bundle_response = self.licensefile_handler.get_licensefile_dict()

        for product_code, license_data in bundle_response.items():
            license_conf = copy.deepcopy(self._conf)
            license_conf._product = product_code
            license_storage = DataStorage(conf=license_conf)
            license_storage._cache.update_cache("normal", json.loads(license_data))
            cache_licenses[product_code] = License(
                product=product_code,
                api_client=self.api_client,
                licensefile_handler=license_storage,
            )

        return cache_licenses

    def activate_bundle(
        self,
        license_id: LicenseID,
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
        variables: dict = None,
    ) -> dict[str, License]:
        """
        Activate bundle and update the licensefile

        Args:
            license_id (LicenseID): An instance containing the license key or user credentials.
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
            dict[str, License]: A dictionary where the keys are product short codes and the values are License objects.
        """

        response = self.api_client.activate_bundle(
            product=self._conf._product,
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
            variables=variables,
        )
        bundles_response = self.licensefile_handler._cache.get_bundle_response(response)

        response_licenses = {}

        for product_code, license_response in bundles_response.items():
            license_storage = DataStorage(self._conf)
            license_storage._cache.product = product_code
            license_storage._cache.update_cache(
                "activate_bundle_license", license_response
            )
            response_licenses[product_code] = License(
                product=product_code,
                api_client=self.api_client,
                licensefile_handler=license_storage,
            )
            license_obj = response_licenses[product_code]
            self.licensefile_handler.save_licensefile(
                license_obj.licensefile_handler._cache
            )

        self.cache_licenses = response_licenses

        return self.cache_licenses

    def create_offline_activation_file(
        self,
        license_id: LicenseID,
        req_path: str,
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
            bundle_code=None,
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

    def activate_bundle_offline(self, ls_activation_path: str) -> dict[str, License]:
        """
        Activate offline bundle licenses

        Args:
            ls_activation_path (str): path to a .lic file

        Returns:
            dict[str, License]: dictionary of licenses in a bundle
        """

        data = self.licensefile_handler.load_offline_response(ls_activation_path)

        if len(data._data) == 0:
            return

        response = self.api_client.activate_bundle_offline(data=data)
        bundles_response = self.licensefile_handler._cache.get_bundle_response(response)

        response_licenses = {}

        for product_code, license_response in bundles_response.items():
            license_storage = DataStorage(self._conf)
            license_storage._cache.product = product_code
            license_storage._cache.update_cache(
                "activate_offline_license_bundle", license_response
            )
            response_licenses[product_code] = License(
                product=product_code,
                api_client=self.api_client,
                licensefile_handler=license_storage,
            )
            license_obj = response_licenses[product_code]
            self.licensefile_handler.save_licensefile(
                license_obj.licensefile_handler._cache
            )

        self.cache_licenses = response_licenses

        return self.cache_licenses

    def deactivate_bundle_offline(
        self, license_id: LicenseID, offline_path: str, unique_license_id: int = None
    ) -> str:
        """
        Generates .req file for the offline deactivation

        Args:
            license_id (LicenseID): license_id
            offline_path (str): path of the .req file
            unique_license_id (int): unique license id

        Returns:
            str: path of the deactivation file
        """

        for license_obj in self.get_current_bundle().values():
            license_obj.licensefile_handler._cache.deactivate()
            self.licensefile_handler.save_licensefile(
                license_obj.licensefile_handler._cache
            )

        data = self.api_client.deactivate_offline_dump(
            product=self.licensefile_handler._cache.product,
            bundle_code=None,
            hardware_id=None,
            license_key=license_id.key,
            license_id=unique_license_id,
            username=license_id.username,
        )
        offline_data = OfflineActivation()
        offline_data.set_is_activation(False)
        offline_data.set_data(data)

        return self.licensefile_handler.create_request_file(offline_data, offline_path)

    def check_bundle(
        self,
        license_id: LicenseID,
        hardware_id: str = None,
        unique_license_id: int = None,
        include_expired_features: bool = False,
        env: str = None,
    ) -> dict[str, License]:
        """
        Check bundle and update the licensefile

        Args:
            license_id (LicenseID): license_id
            hardware_id (str, optional): A unique identifier for the hardware. Defaults to None.
            unique_license_id (int, optional): A unique identifier for the license. Defaults to None.
            include_expired_features (bool, optional): If True, includes expired license features in the check. Defaults to False.
            env (str, optional): optional param takes "win", "win32", "win64", "mac", "linux", "linux32" or "linux64". Defaults to None.

        Returns:
            dict[str, License]: A dictionary where the keys are product short codes and the values are License objects.
        """

        response = self.api_client.check_bundle(
            product=self._conf._product,
            hardware_id=hardware_id,
            license_key=license_id.key,
            license_id=unique_license_id,
            username=license_id.username,
            include_expired_features=include_expired_features,
            env=env,
        )

        cache_licenses = self.get_current_bundle()

        bundles_response = self.licensefile_handler._cache.get_bundle_response(response)

        for product_code, license_obj in cache_licenses.items():
            license_obj.licensefile_handler._cache.update_cache(
                "check_license", bundles_response[product_code]
            )
            self.licensefile_handler.save_licensefile(
                license_obj.licensefile_handler._cache
            )

        logging.info("Online bundle check completed successfully")
        return cache_licenses

    def deactivate_bundle(
        self,
        license_id: LicenseID,
        hardware_id: str = None,
        unique_license_id: int = None,
        remove_local_data: bool = False,
    ) -> None:
        """
        Deactivate bundle

        Args:
            license_id (LicenseID): license_id
            hardware_id (str, optional): hardware id. Defaults to None.
            unique_license_id (int, optional): A unique identifier for the license. Defaults to None.
            remove_local_data (bool, optional): remove licensefile from storage. Defaults to False.
        """

        self.api_client.deactivate_bundle(
            product=self._conf._product,
            hardware_id=hardware_id,
            license_key=license_id.key,
            license_id=unique_license_id,
            username=license_id.username,
        )

        if remove_local_data:
            self.licensefile_handler.delete_licensefile()
            self.cache_licenses = None
            return

        for license_obj in self.get_current_bundle().values():
            license_obj.licensefile_handler._cache.deactivate()
            self.licensefile_handler.save_licensefile(
                license_obj.licensefile_handler._cache
            )
