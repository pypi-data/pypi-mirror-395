from __future__ import annotations

import logging
from datetime import datetime
from typing import Callable

from requests.exceptions import RequestException

from licensespring.api.error import ClientError
from licensespring.licensefile.data_storage import DataStorage
from licensespring.licensefile.error import (
    ClockTamperedException,
    ConfigurationMismatch,
    ErrorType,
    LicenseActivationException,
    LicenseStateException,
    TimeoutExpiredException,
    VMIsNotAllowedException,
)
from licensespring.licensefile.helpers import DateTimeHelper
from licensespring.licensefile.offline_activation_guard import OfflineActivation
from licensespring.licensefile.service import APIService
from licensespring.watchdog import FeatureWatchdog, LicenseWatchdog


class License:
    """
    Represents and manages license operations including activation, deactivation,
    and consumption tracking for a software product.

    Methods:
        __init__(self, product, api_client, licensefile_handler): Initializes the license object with a product, API client, and licensefile handler.

        All Licenses:
            Getters:
                get_device_variables(self, get_from_be: bool = True): Retrieve device varaibles from server or from licensefile

                Licensefile (Offline):
                    start_date(self): Get the license start date
                    maintenance_period(self): Get the license maintenance period
                    is_maintence_period_expired(self): Check if maintence period has expired
                    maintenance_days_remaining(self): Remaining maintenance days

                    last_check(self): Get when was last license check
                    license_type(self): Get license type
                    max_activations(self): Get max activations
                    days_since_last_check(self): Number of days since last check
                    days_remaining(self): How many days remain until validity expires
                    max_transfers(self): Number of max transfers
                    is_device_transfer_allowed(self): If device transfer is allowed return True otherwise False
                    is_device_transfer_limited(self): Return True if there is limited for device transfer otherwise False
                    transfer_count(self): transfer count
                    customer_information(self): retrieve customer information
                    allow_unlimited_activations(self): If unlimited activations are allowed return True otherwise False
                    id(self): Get license id
                    license_enabled(self): If license enabled returns True otherwise False
                    license_active(self): If license is active returns True otherwise False
                    is_valid(self): Checks if license is enabled, active and non-expired then return True otherwise False (License not valid)
                    prevent_vm(self): if license prevents virtual machines return True otherwise False
                    is_trial(self): if license is trial return True otherwise False
                    check_license_status(self): Verifies the current status of the license, raising exceptions if the license is not enabled, not active, or expired.
                    local_check(self): Performs a local check of the license against product code, hardware ID, and VM restrictions.
                    is_grace_period(self, e: Exception): Determines if the current license state is within a grace period
                    get_grace_period(self): Get grace period value is hours.
                    custom_fields(self): Get list of custom fields
                    get_custom_field(self,field_name:str): Get custom fields value
                    get_product_details(self): Retrieve product details from licensefile
                    get_device_variable(self, variable_name: str): Retrieve device variable.
                Online:
                    check(self, include_expired_features=False, req_overages=-1): Performs an online check to sync license data with the backend.
                    product_details(self, include_latest_version: bool = False, include_custom_fields: bool = False): Retrieve product details from server.
            Post:

                Licensefile:
                    update_offline(self, path: str, reset_consumption: bool): Update License through refresh file.
                    set_device_variables(self, variables: dict, save: bool = True): Save device variables to licensefile.
                Online:
                    deactivate(self, delete_license=False): Deactivates the license and optionally deletes the local license file.
                    change_password(self, password: str, new_password: str): Change users password.
                    deactivate_offline(self, offline_path: str): Deactive offline license.
                    send_device_variables(self): Send device variables to LS server

        Time Limited:
            Getters:
                is_validity_period_expired(self): Determines whether the license's validity period has expired, based on the enabled state and validity period.
                validity_period(self): Get the license validity period
                is_expired(self): if validity period of license has expired returns True otherwise False

        Subscription:
            Getters:
                validity_with_grace_period(self): Get the validity period with grace period
                allow_grace_subscription_period(self): if grace period is allowed within subscription return True otherwise False
                is_subscription_grace_period_started(self): is grace period within subscription active
                subscription_grace_period(self): How many hours can subscription be in grace period

        Floating Licenses:
            Getters:
                is_floating_expired(self): Checks if a floating license has expired. Placeholder method that currently always returns False.
                expiry_date(self): Get expiry date of floating license
                is_borrowed(self): Check if license is borrowed
                borrow_until(self): get borrow end date
            Post:
                setup_license_watch_dog(self,callback,timeout):Initializes and starts the license watchdog with the specified callback and timeout.
                stop_license_watch_dog(self): Stops the license watchdog if it is currently running.
                floating_borrow(self,borrow_until:str): Attempts to borrow a floating license until the specified date.
                floating_release(self,throw_e:bool): Releases a borrowed floating license and updates the license status accordingly.

        Consumption Licenses:
            Getters:
                local_consumptions(self) : Get local consumptions
                max_consumptions(self): Get max consumptions
                total_consumptions(self): Get total consumptions
                max_overages(self): Get max overages
                allow_unlimited_consumptions(self): True if unlimited consumptions are allowed otherwise False
                consumption_reset(self): True if there is consumptions reset otherwise False
                allow_overages(self): True if overages are allowed otherwise False
                consumption_period(self): Consumption period
            Post:
                add_local_consumption(self, consumptions=1): Adds local consumption records for consumption-based licenses,
                sync_consumption(self, req_overages=-1): Syncs local consumption data with the server, adjusting for overages if specified.

        License Features:
            Getters:
                get_feature_data(self,feature_code:str): Get license feature fields dictionary.
            Post:
                Licensefile(offline):
                    add_local_feature_consumption(self, feature: str, consumptions=1): Add feature local consumption
                Online:
                    check_feature(self, feature: str, add_to_watchdog=False): Sync feature with LicenseSpring server or register floating feature
                    release_feature(self, feature: str): Release floating feature
                    sync_feature_consumption(self, feature): Sync consumption with the server
                    setup_feature_watch_dog(self,callback: Callable, timeout: int,deamon: bool =False): Setup feature watchdog for floating features
                    stop_feature_watch_dog(self): stop feature watchdog

    Attributes:
        product (str): The software product this license is associated with.
        api_client: An instance responsible for communicating with the licensing API.
        licensefile_handler: Handles local license file operations such as reading and writing.
    """

    def __init__(
        self, product: str, api_client: APIService, licensefile_handler: DataStorage
    ) -> None:
        self.product = product
        self.api_client = api_client
        self.licensefile_handler = licensefile_handler
        self.watch_dog = None
        self.feature_watch_dog = None

    def order_store_id(self) -> str:
        """
        Get order store id

        Returns:
            str: order_store_id
        """
        return self.licensefile_handler._cache.get_order_store_id()

    # air gapped
    def is_air_gapped(self) -> bool:
        """
        Check if license is air gapped

        Returns:
            bool: If license is air gapped return True, otherwise False.
        """
        return self.licensefile_handler._cache.get_is_air_gapped()

    def policy_id(self) -> str:
        """
        Policy id

        Returns:
            str: policy id
        """
        return self.licensefile_handler._cache.get_policy_id()

    def is_floating_expired(self) -> bool:
        """
        Checks if floating license has expired

        Returns:
            bool: True if license has expired, otherwise False.
        """

        if self.licensefile_handler._cache.is_floating_license():
            return DateTimeHelper.has_time_started(self.expiry_date())
        return False

    def is_validity_period_expired(self) -> bool:
        """
        Determines whether the license's validity period has expired.

        Returns:
            bool: True if the validity period has expired or the license is disabled, False otherwise.
        """

        if self.is_expired():
            return True

        if isinstance(self.validity_with_grace_period(), datetime):
            if DateTimeHelper.has_time_started(self.validity_with_grace_period()):
                self.licensefile_handler._cache.set_boolean("is_expired", True)
                return True

        return False

    def validity_period(self) -> datetime:
        """
        Get validity period

        Returns:
            datetime: Validity period
        """
        return self.licensefile_handler._cache.get_validity_period()

    def validity_with_grace_period(self) -> datetime:
        """
        Get validity period

        Returns:
            datetime: Validity period
        """
        return self.licensefile_handler._cache.get_validity_with_grace_period()

    def license_user(self) -> dict:
        return self.licensefile_handler._cache.get_license_user()

    def key(self) -> str:
        return self.licensefile_handler._cache.get_license_key()

    def is_grace_period_started(self):
        return self.licensefile_handler._cache.is_grace_period_started()

    def grace_period_hours_remaining(self):
        return DateTimeHelper.hours_remain(
            self.licensefile_handler._cache.grace_period_end_date()
        )

    def maintenance_days_remaining(self):
        return DateTimeHelper.days_remain(self.maintenance_period())

    def days_remaining(self) -> int:
        return DateTimeHelper.days_remain(self.validity_with_grace_period())

    def customer_information(self) -> dict:
        return self.licensefile_handler._cache.get_customer()

    def id(self):
        return self.licensefile_handler._cache.get_id()

    def max_transfers(self) -> int:
        return self.licensefile_handler._cache.get_max_transfers()

    def transfer_count(self) -> int:
        return self.licensefile_handler._cache.get_transfer_count()

    def is_device_transfer_allowed(self) -> bool:
        return self.max_transfers() != -1

    def is_device_transfer_limited(self) -> bool:
        return self.max_transfers() != 0

    def days_since_last_check(self) -> int:
        return DateTimeHelper.days_since(self.last_check())

    def start_date(self) -> datetime:
        return self.licensefile_handler._cache.get_start_date()

    def maintenance_period(self) -> datetime:
        return self.licensefile_handler._cache.get_maintenance_period()

    def is_maintence_period_expired(self):
        return DateTimeHelper.has_time_started(self.maintenance_period())

    def last_check(self) -> datetime:
        return self.licensefile_handler._cache.get_last_check()

    def last_usage(self) -> datetime:
        return self.licensefile_handler._cache.get_last_usage()

    def license_type(self) -> str:
        return self.licensefile_handler._cache.get_license_type()

    def max_activations(self) -> int:
        return self.licensefile_handler._cache.get_max_activations()

    def metadata(self) -> dict:
        return self.licensefile_handler._cache.get_metadata()

    def allow_unlimited_activations(self) -> bool:
        return self.licensefile_handler._cache.get_allow_unlimited_activations()

    def allow_grace_subscription_period(self) -> bool:
        return self.licensefile_handler._cache.get_allow_grace_period()

    def is_subscription_grace_period_started(self) -> bool:
        if self.subscription_grace_period() == 0:
            return False

        return DateTimeHelper.has_time_started(self.validity_period())

    def get_grace_period(self) -> int:
        return self.licensefile_handler._cache.get_grace_period_conf()

    def subscription_grace_period(self) -> int:
        return self.licensefile_handler._cache.get_grace_period()

    def is_expired(self) -> bool:
        return self.licensefile_handler._cache.get_is_expired()

    def license_enabled(self) -> bool:
        return self.licensefile_handler._cache.get_license_enabled()

    def license_active(self) -> bool:
        return self.licensefile_handler._cache.get_license_active()

    def is_valid(self) -> bool:
        return (
            self.license_enabled() and self.license_active() and not self.is_expired()
        )

    def prevent_vm(self) -> bool:
        return self.licensefile_handler._cache.get_prevent_vm()

    def is_trial(self) -> bool:
        return self.licensefile_handler._cache.get_is_trial()

    # floating
    def floating_timeout(self) -> bool:
        return self.licensefile_handler._cache.get_floating_timeout()

    def is_floating(self) -> bool:
        return self.licensefile_handler._cache.is_floating_license()

    def floating_client_id(self) -> str:
        return self.api_client.hardware_id_provider.get_id()

    def is_controlled_by_floating_server(self) -> bool:
        return self.licensefile_handler._cache.is_controlled_by_floating_server()

    def expiry_date(self) -> datetime:
        return self.licensefile_handler._cache.get_floating_period()

    def borrow_until(self) -> datetime:
        return self.licensefile_handler._cache.get_borrowed_until()

    def is_borrowed(self) -> bool:
        return self.licensefile_handler._cache.get_is_borrowed()

    def floating_in_use_devices(self) -> int:
        return self.licensefile_handler._cache.get_floating_in_use_devices()

    def floating_end_date(self) -> datetime:
        return self.licensefile_handler._cache.get_floating_period()

    def max_floating_users(self) -> int:
        return self.licensefile_handler._cache.get_max_floating_users()

    # consumption

    def local_consumptions(self) -> int:
        return self.licensefile_handler._cache.get_local_consumptions()

    def max_consumptions(self) -> int:
        return self.licensefile_handler._cache.get_max_consumptions()

    def total_consumptions(self) -> int:
        return self.licensefile_handler._cache.get_total_consumptions()

    def max_overages(self) -> int:
        return self.licensefile_handler._cache.get_max_overages()

    def allow_unlimited_consumptions(self) -> bool:
        return self.licensefile_handler._cache.get_allow_unlimited_consumptions()

    def consumption_reset(self) -> bool:
        return self.licensefile_handler._cache.get_consumption_reset()

    def allow_overages(self) -> bool:
        return self.licensefile_handler._cache.get_allow_overages()

    def consumption_period(self) -> str:
        return self.licensefile_handler._cache.get_consumption_period()

    # feature getters

    def get_feature_data(self, feature_code: str) -> dict:
        """
        Get feature dictionary

        Args:
            feature_code (str): feature code

        Returns:
            dict: feature dictionary
        """
        return self.licensefile_handler._cache.get_feature_dict(feature_code)

    def features(self):
        """
        Get features
        """
        return self.licensefile_handler._cache.feature_manager.return_features_list()

    def check_license_status(self) -> None:
        """
        Verifies the current status of the license, including its enablement, activation, and expiration.

        Raises:
            LicenseStateException: If the license is not enabled, not active, or expired.
        """

        if not self.license_enabled():
            raise LicenseStateException(
                ErrorType.LICENSE_NOT_ENABLED, "The license disabled"
            )

        if not self.license_active():
            raise LicenseStateException(
                ErrorType.LICENSE_NOT_ACTIVE, "The license is not active."
            )

        if self.is_validity_period_expired():
            raise LicenseStateException(
                ErrorType.LICENSE_EXPIRED, "The license is expired."
            )

    def check(self, include_expired_features=False, env: str = None) -> dict | None:
        """
        Performs an online license check, syncing the license data with the backend.
        This includes syncing consumptions for consumption-based licenses.

        Args:
            include_expired_features (bool, optional): If True, includes expired license features in the check. Defaults to False.
            env (str, optional): optional param takes "win", "win32", "win64", "mac", "linux", "linux32" or "linux64"

        Returns:
            dict: The response from the license check operation.

        Raises:
            Exceptions: Various exceptions can be raised depending on the API client's implementation and the response from the licensing server.
        """

        try:
            # Add logic for floating server
            logging.info("Online check started")

            if self.is_controlled_by_floating_server():
                logging.info("License is controlled by floating server!")
                response = self.api_client.floating_client.register_user(
                    product=self.licensefile_handler._cache.product,
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                )
                if self.api_client.floating_client.is_floating_server_v2():
                    self.licensefile_handler._cache.update_cache(
                        "floating_server_register_v2", response
                    )

                else:
                    self.licensefile_handler._cache.update_cache(
                        "floating_server_register", response
                    )
                self.licensefile_handler._cache.update_floating_period()

            else:
                response = self.api_client.check_license(
                    product=self.licensefile_handler._cache.product,
                    bundle_code=getattr(
                        self.licensefile_handler._cache, "bundle_code", None
                    ),
                    hardware_id=None,
                    license_key=getattr(
                        self.licensefile_handler._cache, "license_key", None
                    ),
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                    username=getattr(self.licensefile_handler._cache, "username", None),
                    include_expired_features=include_expired_features,
                    env=env,
                )

                logging.info("Request sent to server")

                self.licensefile_handler._cache.update_cache("check_license", response)
                self.licensefile_handler._cache.update_floating_period(
                    self.licensefile_handler._cache.borrowed_until
                )

                logging.info("Updated licensefile with response")

                for (
                    feature
                ) in (
                    self.licensefile_handler._cache.feature_manager.return_features_list()
                ):
                    self.sync_feature_consumption(feature)

                if self.licensefile_handler._cache.license_type == "consumption":
                    self.sync_consumption(req_overages=-1)

                    logging.info("license consumption synced")

                self.licensefile_handler._cache.reset_grace_period_start_date()

                logging.info("Online check successful")

                return response

        except ClientError as ex:
            self.licensefile_handler._cache.update_from_error_code(ex.code)

            logging.info(ex)
            raise ex

        except RequestException as ex:
            if (
                not self.licensefile_handler._cache.is_floating_license()
                or self.licensefile_handler._cache.is_active_floating_cloud()
            ) and self.is_grace_period(ex):
                return None

            raise RequestException("Grace period not allowed/passed")

        except Exception as ex:
            logging.info(ex)
            raise ex

        finally:
            self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)
            self.check_license_status()

    def get_deactivation_code(self, initialization_code: str) -> str:
        """
        Get deactivation code for air gap licenses

        Args:
            initialization_code (str): initialization_code

        Returns:
            str: deactivation code
        """
        return self.api_client.get_air_gap_activation_code(
            initialization_code, self.key()
        )

    def deactivate_air_gap(self, confirmation_code: str) -> None:
        """
        Deactivate air gap license and clear storage

        Args:
            confirmation_code (str): confirmation_code

        Raises:
            LicenseActivationException: VerificationError
        """
        if not self.api_client.verify_confirmation_code(
            confirmation_code=confirmation_code,
            license_key=self.key(),
            policy_id=str(self.policy_id()),
        ):
            raise LicenseActivationException(
                error_type=ErrorType.AIR_GAP_ACTIVATION_ERROR,
                message="VerificationError",
            )

        self.licensefile_handler._cache.deactivate()
        self.licensefile_handler.clear_storage()

    def deactivate(self, delete_license=False) -> None:
        """
        Deactivates the license and optionally deletes the local license file.

        Args:
            delete_license (bool, optional): If True, deletes the local license file upon deactivation.
                Defaults to False.
        """

        if not self.license_active():
            if delete_license:
                self.licensefile_handler.delete_licensefile()
            return None

        if self.is_controlled_by_floating_server():
            self.licensefile_handler._cache.release_license()
            return self.api_client.floating_client.unregister_user(
                product=self.licensefile_handler._cache.product,
                license_id=getattr(self.licensefile_handler._cache, "id", None),
            )

        self.api_client.deactivate_license(
            product=self.licensefile_handler._cache.product,
            bundle_code=getattr(self.licensefile_handler._cache, "bundle_code", None),
            hardware_id=None,
            license_key=getattr(self.licensefile_handler._cache, "license_key", None),
            license_id=getattr(self.licensefile_handler._cache, "id", None),
            username=getattr(self.licensefile_handler._cache, "username", None),
        )

        if delete_license:
            self.licensefile_handler.delete_licensefile()
            return None

        self.licensefile_handler._cache.deactivate()
        self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

    def local_check(self) -> None:
        """
        Performs a local check of the license, ensuring product code, hardware ID, VM (virtual machine), and other conditions are met.

        Raises:
            Various exceptions for different failure conditions.
        """
        try:
            if self.licensefile_handler._cache.product != self.product:
                raise ConfigurationMismatch(
                    ErrorType.PRODUCT_MISMATCH,
                    "License product code does not correspond to configuration product code",
                )

            if (
                self.licensefile_handler._cache.hardware_id
                != self.api_client.hardware_id_provider.get_id()
            ):
                raise ConfigurationMismatch(
                    ErrorType.HARDWARE_ID_MISMATCH,
                    "License hardware id does not correspond to configuration hardware id",
                )

            self.check_license_status()

            if self.api_client.hardware_id_provider.get_is_vm() != self.prevent_vm():
                raise VMIsNotAllowedException(
                    ErrorType.VM_NOT_ALLOWED, "Virtual machine not allowed."
                )

            if self.is_floating_expired():
                raise TimeoutExpiredException(
                    ErrorType.FLOATING_TIMEOUT, "Floating license timeout has expired."
                )

            if DateTimeHelper.has_time_expired(self.last_usage()):
                raise ClockTamperedException(
                    ErrorType.CLOCK_TAMPERED, "Detected cheating with local date time."
                )

        except LicenseStateException as e:
            self.licensefile_handler._cache.update_from_error_code(e.error_type.name)

            raise e

    def change_password(self, password: str, new_password: str) -> str:
        """
        Changes the password for user-based license.
        This method first checks the current license status to ensure it is active and not expired.
        It then attempts to change the password with the licensing server.

        Params:
            password (str): Old password of license user
            new_password (str): New password of license user

        Returns:
            str: password was changed.
        """

        self.check_license_status()

        response = self.api_client.change_password(
            username=getattr(self.licensefile_handler._cache, "username", None),
            password=password,
            new_password=new_password,
        )

        return response

    def add_local_consumption(self, consumptions=1) -> None:
        """
        Add local license consumptions

        Args:
            consumptions (int, optional): Add consumptions. Defaults to 1.
        """

        self.licensefile_handler._cache.update_consumption(consumptions)

    def add_local_feature_consumption(self, feature: str, consumptions=1) -> None:
        """
        Add local feature consumptions

        Args:
            feature (str): feature code
            consumptions (int, optional): Number consumptions. Defaults to 1.
        """

        self.licensefile_handler._cache.update_feature_consumption(
            feature, consumptions
        )

    def sync_feature_consumption(self, feature) -> bool:
        """
        Syncs the local consumption data with the server for consumption-based licenses.

        Args:
            feature (str): feature code.

        Returns:
            bool: True if the consumption data was successfully synchronized; False otherwise.

        """

        if not hasattr(self.licensefile_handler._cache.feature_manager, feature):
            return False

        feature_obj = getattr(self.licensefile_handler._cache.feature_manager, feature)

        if not hasattr(feature_obj, "local_consumption"):
            return False

        if (
            self.licensefile_handler._cache.get_feature_object_field(
                feature_obj, "local_consumption"
            )
            == 0
        ):
            return False

        try:
            if self.is_controlled_by_floating_server():
                response = self.api_client.floating_client.add_feature_consumption(
                    product=self.licensefile_handler._cache.product,
                    feature_code=feature,
                    consumptions=self.licensefile_handler._cache.get_feature_object_field(
                        feature_obj, "local_consumption"
                    ),
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                )

            else:
                response = self.api_client.add_feature_consumption(
                    product=self.licensefile_handler._cache.product,
                    bundle_code=getattr(
                        self.licensefile_handler._cache, "bundle_code", None
                    ),
                    hardware_id=None,
                    license_key=getattr(
                        self.licensefile_handler._cache, "license_key", None
                    ),
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                    username=getattr(self.licensefile_handler._cache, "username", None),
                    feature=feature,
                    consumptions=self.licensefile_handler._cache.get_feature_object_field(
                        feature_obj, "local_consumption"
                    ),
                )

        except ClientError as ex:
            logging.info(ex)
            raise ex

        except RequestException as ex:
            if self.is_grace_period(ex):
                self.licensefile_handler.save_licensefile(
                    self.licensefile_handler._cache
                )
                self.check_license_status()

                return False

            raise RequestException("Grace period not allowed/passed")

        except Exception as ex:
            logging.info(ex)
            raise ex

        else:
            self.licensefile_handler._cache.update_cache(
                "feature_consumption", response, feature
            )

            self.licensefile_handler._cache.reset_grace_period_start_date()

            self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

            return True

    def sync_consumption(self, req_overages=-1) -> bool:
        """
        Syncs the local consumption data with the server for consumption-based licenses.

        Args:
            req_overages (int, optional): Specifies the behavior for requesting consumption overages.
                Defaults to -1, which means no overage request is made. A value of 0 disables overages,
                and a positive value requests permission for overages up to the specified value.

        Returns:
            bool: True if the consumption data was successfully synchronized; False otherwise.

        Side Effects:
            Resets local consumption count after successful synchronization.
        """

        if not hasattr(self.licensefile_handler._cache, "local_consumption"):
            return False

        if self.local_consumptions() == 0 and req_overages < 0:
            return False

        try:
            if req_overages == 0:
                max_overages = req_overages
                allow_overages = False

            elif req_overages > 0:
                max_overages = req_overages
                allow_overages = True

            else:
                max_overages = None
                allow_overages = None

            if self.is_controlled_by_floating_server():
                response = self.api_client.floating_client.add_consumption(
                    product=self.licensefile_handler._cache.product,
                    consumptions=self.local_consumptions(),
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                    max_overages=max_overages,
                    allow_overages=allow_overages,
                )

            else:
                response = self.api_client.add_consumption(
                    product=self.licensefile_handler._cache.product,
                    bundle_code=getattr(
                        self.licensefile_handler._cache, "bundle_code", None
                    ),
                    license_key=getattr(
                        self.licensefile_handler._cache, "license_key", None
                    ),
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                    username=getattr(self.licensefile_handler._cache, "username", None),
                    consumptions=self.local_consumptions(),
                    max_overages=max_overages,
                    allow_overages=allow_overages,
                )

        except ClientError as ex:
            logging.info(ex)
            raise ex

        except RequestException as ex:
            if self.is_grace_period(ex):
                self.licensefile_handler.save_licensefile(
                    self.licensefile_handler._cache
                )
                self.check_license_status()

                return False

            raise RequestException("Grace period not allowed/passed")

        except Exception as ex:
            logging.info(ex)
            raise ex

        else:
            self.licensefile_handler._cache.update_cache(
                "license_consumption", response
            )
            self.licensefile_handler._cache.reset_grace_period_start_date()
            self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

            return True

    def is_grace_period(self, ex: Exception) -> bool:
        """
        Determines if the license is currently within its grace period following a specific exception.
        The grace period logic is activated only if the license cache has a 'grace_period' attribute set,
        and the passed exception is of type 'RequestException', typically indicating a communication
        error with the licensing server.

        Returns:
            bool: True if the license is within its grace period, False otherwise.

        Side Effects:
            - If the license is within its grace period and a 'RequestException' occurs, this method
            updates the grace period start date in the license cache to the current time.
        """

        if not hasattr(self.licensefile_handler._cache, "grace_period_conf"):
            return False

        elif self.licensefile_handler._cache.grace_period_conf > 0 and isinstance(
            ex, RequestException
        ):
            self.licensefile_handler._cache.update_grace_period_start_date()

            return DateTimeHelper.has_time_expired(
                self.licensefile_handler._cache.grace_period_end_date()
            )

        return False

    def setup_license_watch_dog(
        self,
        callback: Callable,
        timeout: int,
        run_immediately: bool = True,
        deamon: bool = False,
    ) -> None:
        """
        Initializes and starts the license watchdog with the specified callback and timeout.

        Args:
            callback: A callable to be executed by the watchdog in response to specific events or conditions.
            timeout: The period in minutes after which the watchdog should perform its checks.
            deamon: run thread as deamon
            run_immediately: run license check immediately, if False wait for timeout first.

        Side Effects:
            - Instantiates the LicenseWatchdog class and stores the instance.
            - Starts the watchdog thread.
        """

        self.watch_dog = LicenseWatchdog(self, callback, timeout)
        self.watch_dog.run(run_immediately=run_immediately, deamon=deamon)

    def stop_license_watch_dog(self) -> None:
        """
        Stops the license watchdog if it is currently running.

        Side Effects:
            - Stops the watchdog thread, if it exists.
        """

        if self.watch_dog:
            self.watch_dog.stop()

    def setup_feature_watch_dog(
        self, callback: Callable, timeout: int, deamon: bool = False
    ):
        """
        Initializes and starts the feature watchdog with the specified callback and timeout.

        Args:
            callback (Callable): A callable to be executed by the watchdog in response to specific events or conditions.
            timeout (int): The period in minutes after which the watchdog should perform its checks.
            deamon (bool, optional): Run thread as deamon. Defaults to False.
        """
        logging.info("Setting up feature watchdog")
        self.feature_watch_dog = FeatureWatchdog(self, callback, timeout)

        for (
            feature
        ) in self.licensefile_handler._cache.feature_manager.attributes_to_list():
            self.feature_watch_dog.add_feature(feature["code"])

        self.feature_watch_dog.run(deamon=deamon)

    def stop_feature_watch_dog(self):
        """
        Stops the license watchdog if it is currently running.

        Side Effects:
            - Stops the watchdog thread, if it exists.
        """
        if self.feature_watch_dog != None:
            self.feature_watch_dog.stop()

    def floating_borrow(self, borrow_until: str, password: str = None) -> None:
        """
        Attempts to borrow a floating license until the specified date.

        Args:
            borrow_until: A string representing the date until which the license should be borrowed.

        Returns:
            None

        Side Effects:
            - Checks if the license is floating or floating cloud type and attempts to borrow it.
            - Updates the license cache and stops the license watchdog if borrowing is successful.
        """

        if not self.licensefile_handler._cache.is_floating_license():
            return None

        if self.licensefile_handler._cache.is_controlled_by_floating_server():
            response = self.api_client.floating_client.borrow(
                product=self.licensefile_handler._cache.product,
                borrowed_until=borrow_until,
                license_id=getattr(self.licensefile_handler._cache, "id", None),
            )

        else:
            response = self.api_client.floating_borrow(
                product=self.licensefile_handler._cache.product,
                bundle_code=getattr(
                    self.licensefile_handler._cache, "bundle_code", None
                ),
                hardware_id=None,
                license_key=getattr(
                    self.licensefile_handler._cache, "license_key", None
                ),
                license_id=getattr(self.licensefile_handler._cache, "id", None),
                username=getattr(self.licensefile_handler._cache, "username", None),
                password=password,
                borrowed_until=borrow_until,
            )

        self.licensefile_handler._cache.set_boolean("is_borrowed", True)
        self.stop_license_watch_dog()
        self.licensefile_handler._cache.update_cache("normal", response)
        self.licensefile_handler._cache.update_floating_period(
            self.licensefile_handler._cache.borrowed_until
        )
        self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

    def floating_release(self, throw_e: bool = False):
        """
        Releases a borrowed floating license and updates the license status accordingly.

        Args:
            throw_e: A boolean indicating whether to raise an exception on failure.

        Returns:
            None

        Side Effects:
            - Attempts to release the floating license and update the license cache.
            - Logs and potentially raises an exception if an error occurs during release.
        """

        if not self.licensefile_handler._cache.is_floating_license():
            return None

        try:
            self.check_license_status()

            if self.is_controlled_by_floating_server():
                self.api_client.floating_client.unregister_user(
                    product=self.licensefile_handler._cache.product,
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                )

            else:
                self.api_client.floating_release(
                    product=self.licensefile_handler._cache.product,
                    bundle_code=getattr(
                        self.licensefile_handler._cache, "bundle_code", None
                    ),
                    hardware_id=None,
                    license_key=getattr(
                        self.licensefile_handler._cache, "license_key", None
                    ),
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                    username=getattr(self.licensefile_handler._cache, "username", None),
                )

            self.licensefile_handler._cache.release_license()
            self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

        except Exception as ex:
            if throw_e:
                logging.info(ex)
                raise ex

    def check_feature(self, feature: str, add_to_watchdog=False) -> None:
        """
        Checks for a specific license feature and updates the license cache accordingly.

        Args:
            feature: feature code.
            add_to_watchdog: A boolean indicating whether to add the feature check to a watchdog routine.

        Returns:
            None
        """
        try:
            if self.is_controlled_by_floating_server():
                # we can expend this currently there is discrepancy between api and FS api
                # if user can send borrow_until on feature check on FS it should work same of API
                response = self.api_client.floating_client.feature_register(
                    product=self.licensefile_handler._cache.product,
                    feature_code=feature,
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                )

            else:
                response = self.api_client.check_license_feature(
                    product=self.licensefile_handler._cache.product,
                    feature=feature,
                    bundle_code=getattr(
                        self.licensefile_handler._cache, "bundle_code", None
                    ),
                    hardware_id=None,
                    license_key=getattr(
                        self.licensefile_handler._cache, "license_key", None
                    ),
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                    username=getattr(self.licensefile_handler._cache, "username", None),
                )

            self.licensefile_handler._cache.register_feature(feature)
            self.licensefile_handler._cache.update_cache(
                "register_feature", response, feature
            )

            if self.feature_watch_dog != None and add_to_watchdog:
                self.feature_watch_dog.add_feature(feature)

            self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

        except Exception as ex:
            logging.info(ex)
            raise ex

    def release_feature(self, feature: str):
        """
        Releases a borrowed license feature and updates the license cache accordingly.

        Args:
            feature: The feature code.

        Returns:
            None
        """
        try:
            if self.is_controlled_by_floating_server():
                self.api_client.floating_client.feature_release(
                    product=self.licensefile_handler._cache.product,
                    feature_code=feature,
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                )

                if self.api_client.floating_client.is_floating_server_v2():
                    self.licensefile_handler._cache.release_feature(feature)

            else:
                self.api_client.floating_feature_release(
                    product=self.licensefile_handler._cache.product,
                    feature=feature,
                    bundle_code=getattr(
                        self.licensefile_handler._cache, "bundle_code", None
                    ),
                    hardware_id=None,
                    license_key=getattr(
                        self.licensefile_handler._cache, "license_key", None
                    ),
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                    username=getattr(self.licensefile_handler._cache, "username", None),
                )

                self.licensefile_handler._cache.release_feature(feature)

            if self.feature_watch_dog != None:
                self.feature_watch_dog.remove_feature(feature)

            self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

        except Exception as ex:
            logging.info(ex)
            raise ex

    def update_offline(self, path: str, reset_consumption: bool) -> bool:
        """
        Updates license via refresh file

        Args:
            path (str): path of the refresh file
            reset_consumption (bool): True resets consumption otherwise False

        Raises:
            ConfigurationMismatch: The update file does not belong to this device
            ConfigurationMismatch: The update file does not belong to this product

        Returns:
            bool: True if license was successfully updated otherwise False
        """

        data = self.licensefile_handler.load_offline_license(path)
        decoded_data = self.api_client.check_offline_load(data)

        if decoded_data["hardware_id"] != self.licensefile_handler._cache.hardware_id:
            raise ConfigurationMismatch(
                ErrorType.HARDWARE_ID_MISMATCH,
                " The update file does not belong to this device. ",
            )

        if (
            decoded_data["product_details"]["short_code"]
            != self.licensefile_handler._cache.product
        ):
            raise ConfigurationMismatch(
                ErrorType.PRODUCT_MISMATCH,
                " The update file does not belong to this product.",
            )

        if (
            reset_consumption == True
            and self.licensefile_handler._cache.license_type == "consumption"
        ):
            self.licensefile_handler._cache.reset_local_consumption()

        self.licensefile_handler._cache.update_cache(
            "update_license_offline", decoded_data
        )
        self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

        return True

    def deactivate_offline(self, offline_path: str) -> str:
        """
        Generates .req file for the offline deactivation

        Args:
            offline_path (str): path of the .req file

        Returns:
            str: path of the deactivation file
        """

        self.licensefile_handler._cache.deactivate()
        data = self.api_client.deactivate_offline_dump(
            product=self.licensefile_handler._cache.product,
            bundle_code=getattr(self.licensefile_handler._cache, "bundle_code", None),
            hardware_id=None,
            license_key=getattr(self.licensefile_handler._cache, "license_key", None),
            license_id=getattr(self.licensefile_handler._cache, "id", None),
            username=getattr(self.licensefile_handler._cache, "username", None),
        )
        offline_data = OfflineActivation()
        offline_data.set_is_activation(False)
        offline_data.set_data(data)

        return self.licensefile_handler.create_request_file(offline_data, offline_path)

    def product_details(
        self,
        include_latest_version: bool = False,
        include_custom_fields: bool = False,
        env: str = None,
    ) -> dict:
        """
        Update product details from LicenseSpring server

        Args:
            include_latest_version (bool, optional): Lateset version information. Defaults to False.
            include_custom_fields (bool, optional): custom fields information. Defaults to False.
            env (str, optional): optional param takes "win", "win32", "win64", "mac", "linux", "linux32" or "linux64"

        Returns:
            dict: response
        """
        response = self.api_client.product_details(
            self.licensefile_handler._cache.product,
            include_latest_version,
            include_custom_fields,
            env,
        )

        self.licensefile_handler._cache.update_cache("product_details", response)
        self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

        return response

    def get_product_details(self) -> dict:
        """
        Retrieve product details from licensefile

        Returns:
            dict: Product details
        """
        return self.licensefile_handler._cache.get_product_details()

    def set_device_variables(self, variables: dict, save: bool = True):
        """
        Set device variables locally

        Args:
            variables (dict): variables dict
            save (bool, optional): Save cache to licensefile. Defaults to True.
        """
        self.licensefile_handler._cache.set_variables(variables)
        if save:
            self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

    def send_device_variables(self) -> bool:
        """
        Send device variables to LicenseSpring server. Handles GracePeriod

        Raises:
            ex: RequestException (Grace period not allowed)

        Returns:
            bool: True if new variables are sent to LicenseSpring server otherwise, False
        """
        try:
            new_varaibles = (
                self.licensefile_handler._cache.get_device_variables_for_send()
            )

            if len(new_varaibles) == 0:
                return False

            self.api_client.track_device_variables(
                product=self.licensefile_handler._cache.product,
                bundle_code=getattr(
                    self.licensefile_handler._cache, "bundle_code", None
                ),
                hardware_id=None,
                license_key=getattr(
                    self.licensefile_handler._cache, "license_key", None
                ),
                license_id=getattr(self.licensefile_handler._cache, "id", None),
                username=getattr(self.licensefile_handler._cache, "username", None),
                variables=new_varaibles,
            )

            return True

        except RequestException as ex:
            if self.is_grace_period(ex):
                return False

            logging.info(ex)
            raise ex

    def get_device_variable(self, variable_name: str) -> dict:
        """
        Get device variable if exists

        Args:
            variable_name (str): variable name

        Returns:
            dict: variable dictionary
        """
        return self.licensefile_handler._cache.get_variable(variable_name)

    def get_device_variables(self, get_from_be: bool = True) -> list:
        """
        Get device variables from server or locally

        Args:
            get_from_be (bool, optional): If True collects data from LicenseSpring server. Defaults to True.

        Raises:
            ex: RequestException (Grace period not allowed)

        Returns:
            list: List of device variables
        """
        if get_from_be:
            try:
                response = self.api_client.get_device_variables(
                    product=self.licensefile_handler._cache.product,
                    bundle_code=getattr(
                        self.licensefile_handler._cache, "bundle_code", None
                    ),
                    hardware_id=None,
                    license_key=getattr(
                        self.licensefile_handler._cache, "license_key", None
                    ),
                    license_id=getattr(self.licensefile_handler._cache, "id", None),
                    username=getattr(self.licensefile_handler._cache, "username", None),
                )

            except RequestException as ex:
                if not self.is_grace_period():
                    logging.info(ex)
                    raise ex

            self.licensefile_handler._cache.update_cache("device_variables", response)
            self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

        return self.licensefile_handler._cache.get_variables()

    def custom_fields(self) -> list:
        """
        Get custom fields

        Returns:
            list: list of custom fields -> [{name, data_type, value},..]
        """
        return self.licensefile_handler._cache.get_custom_fields()

    def version(self) -> str:
        """
        Return current version

        Returns:
            str: version
        """
        return self.licensefile_handler._cache.get_version()

    def company(self) -> dict:
        """
        Return company data

        Returns:
            dict: company
        """
        return self.licensefile_handler._cache.get_company_data()
    
    def activation_date(self) -> datetime:
        """
        Date when license was activated

        Returns:
            datetime: license activation date
        """
        return self.licensefile_handler._cache.get_activation_date()
