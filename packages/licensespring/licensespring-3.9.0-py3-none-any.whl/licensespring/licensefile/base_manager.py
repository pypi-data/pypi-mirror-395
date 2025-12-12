from licensespring.licensefile import License
from licensespring.licensefile.config import Configuration
from licensespring.licensefile.data_storage import DataStorage
from licensespring.licensefile.error import LicenseFileCorruption
from licensespring.licensefile.service import APIService


class BaseManager:
    def __init__(self, conf: Configuration):
        self._conf = conf
        self.licensefile_handler = DataStorage(conf)
        self.api_client = APIService(conf=conf)

    def load_license(self) -> License:
        """
        Loads licensefile and sets attributes for LicenseData instance
        Returns:
        License: An instance of the License class reflecting the loaded license.
        """
        self.licensefile_handler.load_licensefile()

        return License(self._conf._product, self.api_client, self.licensefile_handler)

    def current_config(self) -> dict:
        """
        Get current configuration

        Returns:
            dict: configuration
        """
        return self._conf.__dict__

    def reconfigure(self, conf: Configuration) -> None:
        """
        Reconfigure

        Args:
            conf (Configuration): Configuration
        """
        self._conf = conf
        self.licensefile_handler = DataStorage(conf)
        self.api_client = APIService(conf=conf)

    def is_license_file_corrupted(self) -> bool:
        """
        Check if licensefile is corrupted

        Returns:
            bool: True if licensefile is corrupted otherwise False
        """
        try:
            self.licensefile_handler.load_licensefile()
            return False
        except LicenseFileCorruption:
            return True

    def clear_local_storage(self):
        """
        Clear all data from current product
        """
        self.licensefile_handler.clear_storage()

    def data_location(self) -> str:
        """
        Get licensefile location

        Returns:
            str: licensefile location
        """

        return self.licensefile_handler.license_path

    def set_data_location(self, path: str):
        """
        Set data location

        Args:
            path (str): new data location path
        """
        self.licensefile_handler._license_path = path

    def license_file_name(self) -> str:
        """
        Get licensefile name

        Returns:
            str: licensefile name
        """

        return self.licensefile_handler._filename

    def set_license_file_name(self, name: str):
        """
        Set licensefile name

        Args:
            name (str): license file name
        """

        self.licensefile_handler._filename = name

    def get_product_details(
        self, include_latest_version=False, include_custom_fields=False, env: str = None
    ) -> dict:
        """
        Get product details

        Args:
            include_latest_version (bool, optional): include_latest_version. Defaults to False.
            include_custom_fields (bool, optional): include_custom_fields. Defaults to False.
            env (str, optional): env. Defaults to None.

        Returns:
            dict: product details
        """
        return self.api_client.product_details(
            product=self._conf._product,
            include_latest_version=include_latest_version,
            include_custom_fields=include_custom_fields,
            env=None,
        )
