from __future__ import annotations

import json
import os

from licensespring.licensefile.config import Configuration
from licensespring.licensefile.default_crypto import DefaultCryptoProvider
from licensespring.licensefile.error import (
    ErrorType,
    LicenseDeleted,
    LicenseFileCorruption,
)
from licensespring.licensefile.license_data import LicenseData
from licensespring.licensefile.offline_activation_guard import (
    OfflineActivation,
    OfflineActivationGuard,
)


class DataStorage(DefaultCryptoProvider):
    """
    Extends DefaultCryptoProvider to handle license file cache operations, including saving to and loading from a .key file.

    Attributes:
        _conf (Configuration): Configuration object containing settings and parameters.
        _cache (LicenseData): Instance of LicenseData for managing license attributes in memory.
        _filename (str): The name of the file used for storing the license information.
        _license_path (str): The file path where the license file is stored.

    Methods:
        cache: Returns the current license data stored in memory.
        license_path: Returns the file path for the license file.
        save_licensefile(): Encrypts and saves the license data to a file.
        load_licensefile(): Loads and decrypts the license data from a file.
        set_path(product_code, custom_path): Sets the file path for the license file based on the operating system.
        delete_licensefile(): Deletes the license file and clears the license data in memory.
        create_activation_guard(id): Creates OfflineActivationGuard object.
        create_request_file(req_data,offline_path): Creates .req file for license activation or deactivation.
        save_guard_file(guard): Saves guard file locally.
        remove_offline_activation_data(activation_file): Removes guard and activation file.
        load_guard_file(): Loads locally saved guard file.
        check_guard(offline_data): Checks the validity of the .lic file.
        load_offline_response(file_path): Loads offline response file.
    """

    def __init__(self, conf: Configuration):
        self._conf = conf
        super().__init__(self._conf._file_key, self._conf._file_iv)

        self._cache = LicenseData(
            product=self._conf._product,
            hardwareID=self._conf._hardware_id_provider.get_id(self),
            grace_period_conf=self._conf.grace_period_conf,
        )

        self._filename = self._conf._filename
        self._license_path = self.set_path(self._conf._product, self._conf._file_path)

    @property
    def cache(self):
        return self._cache.to_json()

    @property
    def license_path(self):
        return self._license_path

    def save_licensefile(self, data_obj: LicenseData):
        """
        Creates path for licensefile
        Saves encrypted string of licensefile JSON
        """
        if not getattr(data_obj, "is_bundle_activated", False):
            json_string_encrypted = self.encrypt(data_obj.to_json())

        else:
            bundle_data = self.get_licensefile_dict(ignore_file_not_found=True)
            product_short_code = data_obj.get_product_details()["short_code"]
            bundle_data[product_short_code] = data_obj.to_json()
            json_string_encrypted = self.encrypt(
                json.dumps(bundle_data, ensure_ascii=False)
            )

        with self._cache._lock:
            if not os.path.exists(self.license_path):
                os.makedirs(self.license_path)

            with open(
                os.path.join(self.license_path, self._filename + ".key"), "w"
            ) as file:
                file.write(json_string_encrypted)

    def create_request_file(
        self, req_data: OfflineActivation, offline_path: str
    ) -> str:
        """
        Creates .req file for license activation or deactivation

        Args:
            req_data (OfflineActivation): OfflineActivation object
            offline_path (str): sets a path for .req file

        Returns:
            str: path of a .req file
        """

        if not os.path.exists(offline_path):
            os.makedirs(offline_path)

        filename = (
            "activate_offline.req"
            if req_data._is_activation
            else "deactivate_offline.req"
        )

        with open(os.path.join(offline_path, filename), mode="w") as f:
            print(req_data._data, file=f)

        if req_data._is_activation:
            self.save_guard_file(req_data._guard)

        return os.path.join(offline_path, filename)

    def save_guard_file(self, guard: OfflineActivationGuard) -> None:
        """
        Saves guard file locally

        Args:
            guard (OfflineActivationGuard): OfflineActivationGuard object
        """

        if self._conf.is_guard_file_enabled:
            if not os.path.exists(self.license_path):
                os.makedirs(self.license_path)
            self.remove_offline_activation_data()
            with open(
                os.path.join(self.license_path, "OfflineActivation.guard"), "w"
            ) as file:
                file.write(self.encrypt(guard.to_json()))

    def remove_offline_activation_data(self, activation_file: str = None):
        """
        Removes guard and activation file.

        Args:
            activation_file (str, optional): Path of the activation file. Defaults to None.
        """

        file_path_guard = os.path.join(self.license_path, "OfflineActivation.guard")

        if os.path.exists(file_path_guard):
            os.remove(file_path_guard)

        if activation_file != None:
            if os.path.exists(activation_file):
                os.remove(activation_file)

    def load_guard_file(self) -> dict:
        """
        Loads locally saved guard file

        Returns:
            dict: guard file
        """

        with open(
            os.path.join(self.license_path, "OfflineActivation.guard"), "r"
        ) as file:
            json_string_encrypted = file.read()

        return json.loads(self.decrypt(json_string_encrypted))

    def load_offline_license(self, path: str) -> dict:
        with open(path, "r") as file:
            data = file.read()

        return data

    def load_offline_response(self, file_path: str) -> OfflineActivation:
        """
        Loads offline response file

        Args:
            file_path (str): file path

        Returns:
            str: string data
        """
        offline_data = OfflineActivation()
        offline_data.set_is_activation(True)

        with open(file_path, "r") as file:
            data = file.read()

        offline_data.set_data(data)
        offline_data.set_use_guard(self._conf.is_guard_file_enabled)

        if self._conf.is_guard_file_enabled:
            guard_dict = self.load_guard_file()
            offline_data.create_guard_file(OfflineActivationGuard.from_json(guard_dict))

        return offline_data

    def get_licensefile_dict(self, ignore_file_not_found=False):
        licensefile_path = os.path.join(self.license_path, self._filename + ".key")

        try:
            with open(licensefile_path, "r") as file:
                json_string_encrypted = file.read()

            return json.loads(self.decrypt(json_string_encrypted))

        except (UnicodeDecodeError, ValueError):
            raise LicenseFileCorruption(
                ErrorType.CORRUPTED_LICENSEFILE, "Licensefile corrupted"
            )

        except FileNotFoundError:
            if ignore_file_not_found:
                return {}
            raise LicenseDeleted(ErrorType.NO_LICENSEFILE, "Licensefile doesn't exist")

    def load_licensefile(self, ignore_file_not_found=False) -> dict:
        """
        Loads and decrypts licensefile

        Returns:
            dict: licensefile
        """
        licensefile_dict = self.get_licensefile_dict(ignore_file_not_found)

        self._cache.from_json_to_attr(licensefile_dict)

        self._cache.grace_period_conf = self._conf.grace_period_conf

        return licensefile_dict

    def set_path(self, product_code: str, custom_path=None) -> str:
        """
        Set path for licensefile

        Parameters:
            product_code (str): short product code of LicenseSpring product
            custom_path(str,optional): custom path of licensefile

        Returns:
            str: Path of licensefile
        """

        if custom_path is not None:
            return custom_path

        if os.name == "nt":  # Windows
            base_path = os.path.join(
                os.environ.get("SystemDrive"),
                os.sep,
                "Users",
                os.environ.get("USERNAME"),
            )
            return os.path.join(
                base_path, "AppData", "Local", "LicenseSpring", product_code
            )

        elif os.name == "posix":  # Linux and macOS
            if "HOME" in os.environ:
                base_path = os.environ["HOME"]
                return os.path.join(
                    base_path, ".LicenseSpring", "LicenseSpring", product_code
                )

            else:  # macOS and other POSIX systems
                base_path = os.path.expanduser("~")
                return os.path.join(
                    base_path,
                    "Library",
                    "Application Support",
                    "LicenseSpring",
                    product_code,
                )

        else:
            raise Exception("Unsupported operating system")

    def delete_licensefile(self):
        """
        Permanently deletes licensefile and clears cache

        Returns: None
        """

        self.remove_offline_activation_data()

        if os.path.exists(os.path.join(self.license_path)):
            os.remove(os.path.join(self.license_path, self._filename + ".key"))

        self._cache = LicenseData(
            product=self._conf._product,
            hardwareID=self._conf._hardware_id_provider.get_id(self),
            grace_period_conf=self._conf.grace_period_conf,
        )

    def clear_storage(self) -> None:
        """
        Clear storage
        1. Delete licensefile
        2. Delete guardfile
        If folder is empty delete folder
        """
        self.delete_licensefile()
        self.remove_offline_activation_data()

        if os.path.exists(self._license_path) and os.path.isdir(self._license_path):
            if not os.listdir(self._license_path):
                os.rmdir(self._license_path)
