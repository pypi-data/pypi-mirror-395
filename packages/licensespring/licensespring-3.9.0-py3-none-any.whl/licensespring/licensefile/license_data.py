from __future__ import annotations

import json
import threading
from datetime import datetime, timedelta, timezone

import licensespring
from licensespring.licensefile.device_variables import VariablesManager
from licensespring.licensefile.error import (
    ConsumptionError,
    ErrorType,
    LicenseSpringTypeError,
)
from licensespring.licensefile.feature_manager import FeatureManager
from licensespring.licensefile.product_details import ProductDetailsManager


class LicenseData:
    """
    A class for handling License file fields, providing functionalities for managing license data.

    Attributes:
        grace_period_conf (int): Defines how many hours can license be in offline mode.
        product (str): Identifier for the software product associated with this license.
        hardware_id (str): Unique hardware ID of the device using the license, used for license binding.
        version (str): Version of the Python SDK, fetched from licensespring.version.
        license_key (str, optional): The key used for license activation. Default is None.
        floating_period (int, optional): Defines the period for a floating license. Default is None.
        last_check (datetime, optional): Timestamp of the last license check. Default is None.
        last_usage (datetime, optional): Timestamp of the last usage of the license. Default is None.

    Methods:
        features_setup(): Sets up local consumption count for consumption-based features.
        local_consumption_setup(): Initializes local consumption count for licenses of type 'consumption'.
        to_json(): Serializes the license data to a JSON string.
        from_json_to_attr(licensefile_dict): Deserializes JSON string or dictionary to license data attributes.
        update_cache(method, response): Updates the license data in memory based on the response from a license operation.

        validity_with_grace_period(): Calculates and returns the expiration date.

        is_grace_period_started(): If grace period started returns True, otherwise False.
        grace_period_end_date(): Calculates end date of grace period.
        update_grace_period_start_date(): Sets grace_period_start_date to UTC.
        reset_grace_period_start_date(): Resets grace period start date.

        update_from_error_code(error_code): Updates the state of the object based on the provided error code.

        is_active_floating_cloud(): Determines whether the license is active floating cloud.

        deactivate(): Deactivates the current license and updates times_activated and license_active.

        update_password(): updates password.

        update_consumption(consumptions:int):Adds local consumptions for consumption-based licenses.
        update_feature_consumption(feature, consumptions=1): Adds a specified number of local consumptions to a feature.

        release_license():Handles operations on licensefile for releasing license.
        register_feature(feature_code): Handles feature check.
        release_feature(feature_code:str): Handles feature release.
        set_boolean(field_name:str,bool:bool): set boolean of field_name.

    """

    datetime_attributes = [
        "last_check",
        "last_usage",
        "floating_period",
        "maintenance_period",
        "start_date",
        "validity_period",
        "borrowed_until",
        "grace_period_start_date",
    ]

    def __init__(self, product, hardwareID, grace_period_conf):
        self.grace_period_conf = grace_period_conf
        self.product = product
        self.hardware_id = hardwareID
        self.version = licensespring.version
        self.feature_manager = FeatureManager()
        self.device_var_manager = VariablesManager()
        self.product_details_manager = ProductDetailsManager()

        self.license_key = None
        self.floating_period = datetime.now(timezone.utc).replace(tzinfo=None)

        self.last_check = None
        self.activation_date = None
        self.last_usage = None
        self.times_activated = 1

        self._lock = threading.Lock()

    def local_consumption_setup(self):
        """
        Initializes the local consumption attribute for licenses of type 'consumption' if it's not already set.
        This method assumes the existence of a license_type attribute to check against 'consumption'.
        """

        if (
            not hasattr(self, "local_consumption")
            and self.license_type == "consumption"
        ):
            self.local_consumption = 0

    def grace_period_setup(self):
        if not hasattr(self, "grace_period_start_date"):
            self.grace_period_start_date = datetime(year=2099, month=1, day=1)

    def to_json(self) -> json:
        """
        Serializes the license data attributes to a JSON string, converting datetime objects to ISO format.

        Returns:
            str: The serialized JSON string of the license data.
        """
        with self._lock:
            data = {}
            for key, value in self.__dict__.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()

                elif key == "feature_manager":
                    data["product_features"] = self.feature_manager.attributes_to_list()

                elif key == "device_var_manager":
                    data["device_variables"] = (
                        self.device_var_manager.attributes_to_list()
                    )

                elif key == "product_details_manager":
                    data["product_details"] = self.product_details_manager.__dict__

                elif key == "_lock":
                    pass

                else:
                    data[key] = value

            return json.dumps(data, ensure_ascii=False)

    def from_json_to_attr(self, licensefile_dict: dict):
        """
        Deserializes a JSON string or dictionary to update the license data attributes, converting ISO format strings back to datetime objects for specific fields.

        Args:
            licensefile_dict (dict): The dictionary containing license data to be deserialized.
        """

        for key, value in licensefile_dict.items():
            if key in LicenseData.datetime_attributes and value != None:
                if value.endswith("Z"):
                    value = value[:-1]
                setattr(self, key, datetime.fromisoformat(value).replace(tzinfo=None))

            elif key == "product_details":
                self.product_details_manager.json_to_attribute(
                    licensefile_dict["product_details"]
                )

            elif key == "product_features":
                self.feature_manager.json_to_attribute(
                    licensefile_dict["product_features"]
                )
            elif key == "variables":
                self.device_var_manager.json_to_attribute(licensefile_dict["variables"])

            else:
                setattr(self, key, value)

    def update_cache(self, method: str, response: dict, feature: str = None):
        """
        Updates licensefile data inside memory.

        Parameters:
        response (dict): Response of license activation or license check.

        Returns: None
        """
        with self._lock:
            self.last_usage = datetime.now(timezone.utc).replace(tzinfo=None)

            if method == "check_license":
                self.last_check = datetime.now(timezone.utc).replace(tzinfo=None)
                self.from_json_to_attr(response)

            elif method == "activate_license":
                self.from_json_to_attr(response)
                self.local_consumption_setup()
                self.grace_period_setup()

                self.license_enabled = True
                self.is_expired = False
                self.license_active = True
                self.is_bundle_activated = False
                self.activation_date = datetime.now(timezone.utc).replace(tzinfo=None)

            elif method == "activate_license_offline":
                response["prevent_vm"] = response["product_details"]["prevent_vm"]
                self.from_json_to_attr(response)
                self.local_consumption_setup()
                self.grace_period_setup()

                self.license_enabled = True
                self.is_expired = False
                self.license_active = True
                self.activation_date = datetime.now(timezone.utc).replace(tzinfo=None)
                

            elif method == "activate_air_gap":
                self.from_json_to_attr(response)
                self.local_consumption_setup()
                self.grace_period_setup()

                self.license_enabled = True
                self.is_expired = False
                self.license_active = True
                self.is_bundle_activated = False
                self.activation_date = datetime.now(timezone.utc).replace(tzinfo=None)
                

            elif method == "activate_bundle_license":
                self.from_json_to_attr(response)
                self.local_consumption_setup()
                self.grace_period_setup()

                self.license_enabled = True
                self.is_expired = False
                self.license_active = True
                self.is_bundle_activated = True
                self.activation_date = datetime.now(timezone.utc).replace(tzinfo=None)

            elif method == "activate_offline_license_bundle":
                response["prevent_vm"] = response["product_details"]["prevent_vm"]
                self.from_json_to_attr(response)
                self.local_consumption_setup()
                self.grace_period_setup()

                self.license_enabled = True
                self.is_expired = False
                self.license_active = True
                self.is_bundle_activated = True
                self.activation_date = datetime.now(timezone.utc).replace(tzinfo=None)

            elif method == "floating_server_register":
                response["floating_in_use_devices"] = response["floating_slots_in_use"]
                # This should get improved on LS side
                self.from_json_to_attr(json.loads(response["license_json"]))
                del response["license_json"]
                self.from_json_to_attr(response)

                self.local_consumption_setup()
                self.grace_period_setup()

                self.license_enabled = True
                self.is_expired = False
                self.license_active = True

            elif method == "floating_server_register_v2":
                self.from_json_to_attr(response)

                self.local_consumption_setup()
                self.grace_period_setup()

                self.license_enabled = True
                self.is_expired = False
                self.license_active = True

            elif method == "update_license_offline":
                self.from_json_to_attr(response)

            elif method == "product_details":
                self.product_details_manager.json_to_attribute(response)

            elif method == "device_variables":
                self.device_var_manager.json_to_attribute(response)

            elif method == "normal":
                self.from_json_to_attr(response)

            elif method == "license_consumption":
                self.from_json_to_attr(response)
                self.local_consumption = 0

            elif method == "feature_consumption":
                feature_obj = getattr(self.feature_manager, feature)
                feature_obj.json_to_attribute(response)
                feature_obj.local_consumption = 0

            elif method == "register_feature":
                feature_obj = getattr(self.feature_manager, feature)
                feature_obj.json_to_attribute(response)

    def get_validity_period(self):
        with self._lock:
            return self.validity_period

    def get_validity_with_grace_period(self) -> datetime | None:
        """
        Calculates and returns the expiration date and time of an object with an optional grace period extension.
        """

        with self._lock:
            if hasattr(self, "grace_period") and self.validity_period != None:
                if self.grace_period > 0:
                    return self.validity_period + timedelta(hours=self.grace_period)

            return self.validity_period

    def is_grace_period_started(self) -> bool:
        return self.grace_period_start_date != datetime(year=2099, month=1, day=1)

    def grace_period_end_date(self) -> datetime:
        return self.grace_period_start_date + timedelta(hours=self.grace_period_conf)

    def update_grace_period_start_date(self) -> None:
        with self._lock:
            if not self.is_grace_period_started():
                self.grace_period_start_date = datetime.now(timezone.utc).replace(
                    tzinfo=None
                )

    def reset_grace_period_start_date(self) -> None:
        with self._lock:
            if self.is_grace_period_started():
                self.grace_period_start_date = datetime(year=2099, month=1, day=1)

    def update_from_error_code(self, error_code: str):
        """
        Updates the state of the object based on the provided error code.

        Args:
            error_code (str): A string representing the error code which dictates how the object's state should be updated. The method recognizes three specific error codes:
                - "LICENSE_NOT_ACTIVE": Indicates the license is not currently active. Sets `self.license_active` to False.
                - "LICENSE_NOT_ENABLED": Indicates the license is not enabled. Sets `self.license_enabled` to False.
                - "LICENSE_EXPIRED": Indicates the license has expired. Sets `self.is_expired` to True.

        The method converts `error_code` to uppercase to ensure case-insensitive comparison.
        """

        with self._lock:
            if error_code.upper() == "LICENSE_NOT_ACTIVE":
                self.license_active = False

            elif error_code.upper() == "LICENSE_NOT_ENABLED":
                self.license_enabled = False

            elif error_code.upper() == "LICENSE_EXPIRED":
                self.is_expired = True

    def is_active_floating_cloud(self):
        """
        Determines whether the license is active floating cloud

        Returns:
            bool: True if the floating cloud is active, False otherwise.
        """
        with self._lock:
            if self.is_floating_cloud:
                if self.floating_period > datetime.now(timezone.utc).replace(
                    tzinfo=None
                ):
                    return True

            return False

    def deactivate(self):
        """
        Deactivates the current license and updates times_activated and license_active.

        1. Decrements the `times_activated` counter if it is greater than 0. This counter tracks the number of times the license has been activated. The decrement operation signifies one less active instance of the license.

        2. If `times_activated` is already at 0, it leaves it unchanged. This prevents the counter from going negative, which would be semantically incorrect.

        3. Sets `self.license_active` to False, indicating that the license is no longer active.

        This method is typically called when the license needs to be deactivated.

        """

        with self._lock:
            if self.times_activated > 0:
                self.times_activated -= 1

            else:
                self.times_activated = 0

            self.license_active = False

    def update_consumption(self, consumptions: int):
        """
        Adds local consumptions for consumption-based licenses.

        Args:
            consumptions (int): The number of consumptions to add locally.

        Returns:
            dict: The updated license cache reflecting the new consumption count.

        Raises:
            LicenseTypeError: If the license is not of type 'consumption'.
            ConsumptionError: If adding the consumptions would exceed the allowed maximum.
            ConsumptionError: If adding the negative consumptions are not allowed.
        """

        with self._lock:
            if self.license_type != "consumption":
                raise LicenseSpringTypeError(
                    ErrorType.WRONG_LICENSE_TYPE,
                    f" WRONG License Type: {self.license_type}",
                )

            elif (
                getattr(self, "allow_negative_consumptions", True) == False
                and consumptions < 0
            ):
                raise ConsumptionError(
                    error_type=ErrorType.NEGATIVE_CONSUMPTION_NOT_ALLOWED,
                    message="Negative consumptions not allowed",
                )

            elif self.allow_unlimited_consumptions:
                self.local_consumption += consumptions

            elif (
                self.max_consumptions + self.max_overages
                < self.local_consumption + consumptions + self.total_consumptions
            ):
                raise ConsumptionError(
                    ErrorType.NOT_ENOUGH_LICENSE_CONSUMPTIONS,
                    "Not enough conusmptions left!",
                )

            else:
                self.local_consumption += consumptions

    def reset_local_consumption(self):
        with self._lock:
            self.local_consumption = 0

    def is_controlled_by_floating_server(self):
        with self._lock:
            return self.is_floating

    def is_floating_license(self):
        return self.is_floating or self.is_floating_cloud

    def update_feature_consumption(self, feature, consumptions=1):
        """
        Adds a specified number of consumptions to a local feature, updating its consumption count.
        """

        with self._lock:
            self.feature_manager.add_local_consumption(feature, consumptions)

    def update_floating_period(self, end_date: datetime = None) -> None:
        """
        Updates floating end time if needed

        Args:
            end_date (datetime): end date of floating
        """

        with self._lock:
            if self.is_floating_license():
                if isinstance(end_date, datetime):
                    floating_end = end_date

                else:
                    floating_end = timedelta(
                        minutes=self.floating_timeout
                    ) + datetime.now(timezone.utc).replace(tzinfo=None)

                self.floating_period = floating_end

    def release_license(self):
        """
        Handles operations on licensefile for releasing license

        1. Sets `self.is_borrowed` to False, indicating the license is no longer borrowed.
        2. Resets `self.borrowed_until` to None, clearing the timestamp until which the license was borrowed.
        3. Decrements `self.floating_in_use_devices` by 1, reducing the count of devices currently using a floating license by one.
        """

        with self._lock:
            self.is_borrowed = False
            self.borrowed_until = None
            self.floating_period = datetime.now(timezone.utc).replace(tzinfo=None)
            if self.floating_in_use_devices > 0:
                self.floating_in_use_devices -= 1

    def register_feature(self, feature_code: str):
        """
        Handles feature check
        """

        with self._lock:
            self.feature_manager.register_feature(feature_code)

    def get_bundle_response(self, response: dict):
        bundle_response = {}
        for license_response in response:
            bundle_response[license_response["product_details"]["short_code"]] = (
                license_response
            )

        return bundle_response

    def release_feature(self, feature_code: str):
        """
        Handles feature release
        """

        with self._lock:
            self.feature_manager.release_feature(feature_code)

    def set_boolean(self, field_name: str, bool: bool):
        """
        Changes/Sets LicenseData field to boolean value

        Args:
            field_name (str): field name
            bool (bool): True/False
        """

        with self._lock:
            setattr(self, field_name, bool)

    def get_feature_object(self, feature: str):
        with self._lock:
            return getattr(self.feature_manager, feature, None)

    def get_feature_object_field(self, feature_object: object, field: str):
        with self._lock:
            return getattr(feature_object, field)

    def get_company_data(self):
        with self._lock:
            return getattr(self, "company", None)

    def get_feature_dict(self, feature_code):
        with self._lock:
            return self.feature_manager.get_feature_dict(feature_code)

    def get_variable(self, variable_name: str):
        with self._lock:
            return self.device_var_manager.get_device_variable(variable_name)

    def set_variables(self, variables: dict):
        with self._lock:
            self.device_var_manager.set_variables(variables)

    def get_variables(self):
        with self._lock:
            return self.device_var_manager.attributes_to_list()

    def get_device_variables_for_send(self) -> dict:
        with self._lock:
            return self.device_var_manager.get_device_variable_for_send()

    def get_custom_fields(self):
        with self._lock:
            return self.custom_fields

    def get_customer(self) -> dict:
        with self._lock:
            return self.customer

    def get_product_details(self):
        return self.product_details_manager.__dict__

    def get_is_floating(self):
        with self._lock:
            return getattr(self, "is_floating")

    def get_floating_in_use_devices(self):
        with self._lock:
            return getattr(self, "floating_in_use_devices", None)

    def get_max_floating_users(self):
        with self._lock:
            return getattr(self, "floating_users")

    def get_is_borrowed(self):
        with self._lock:
            return self.is_borrowed

    def get_borrowed_until(self):
        with self._lock:
            return getattr(self, "borrowed_until", None)

    def get_floating_timeout(self):
        with self._lock:
            return getattr(self, "floating_timeout", None)

    def get_floating_period(self):
        with self._lock:
            return self.floating_period

    def get_max_transfers(self):
        with self._lock:
            return self.max_transfers

    def get_transfer_count(self):
        with self._lock:
            return self.transfer_count

    def get_id(self):
        with self._lock:
            return self.id

    def get_start_date(self):
        with self._lock:
            return self.start_date

    def get_maintenance_period(self):
        with self._lock:
            return self.maintenance_period

    def get_last_check(self):
        with self._lock:
            return self.last_check

    def get_last_usage(self):
        with self._lock:
            return self.last_usage

    def get_max_activations(self):
        with self._lock:
            return self.max_activations

    def get_allow_unlimited_activations(self):
        with self._lock:
            return self.allow_unlimited_activations

    def get_is_trial(self):
        with self._lock:
            return self.is_trial

    def get_allow_grace_period(self):
        with self._lock:
            return self.allow_grace_period

    def get_grace_period_conf(self):
        with self._lock:
            return self.grace_period_conf

    def get_grace_period(self):
        with self._lock:
            return self.grace_period

    def get_is_expired(self):
        with self._lock:
            return self.is_expired

    def get_license_active(self):
        with self._lock:
            return self.license_active

    def get_license_enabled(self):
        with self._lock:
            return self.license_enabled

    def get_license_type(self):
        with self._lock:
            return self.license_type

    def get_prevent_vm(self):
        with self._lock:
            return self.prevent_vm

    def get_metadata(self):
        with self._lock:
            return self.metadata

    def get_local_consumptions(self) -> int:
        with self._lock:
            return getattr(self, "local_consumption", None)

    def get_max_consumptions(self) -> int:
        with self._lock:
            return getattr(self, "max_consumptions", None)

    def get_total_consumptions(self) -> int:
        with self._lock:
            return getattr(self, "total_consumptions", None)

    def get_max_overages(self) -> int:
        with self._lock:
            return getattr(self, "max_overages", None)

    def get_consumption_reset(self) -> bool:
        with self._lock:
            return getattr(self, "reset_consumption", None)

    def get_allow_unlimited_consumptions(self) -> bool:
        with self._lock:
            return getattr(self, "allow_unlimited_consumptions", None)

    def get_consumption_period(self) -> str:
        with self._lock:
            return getattr(self, "consumption_period", None)

    def get_allow_overages(self) -> bool:
        with self._lock:
            return getattr(self, "allow_overages", None)

    def get_is_air_gapped(self) -> bool:
        with self._lock:
            return getattr(self, "is_air_gapped", False)

    def get_license_key(self):
        with self._lock:
            return getattr(self, "license_key")

    def get_policy_id(self) -> str:
        with self._lock:
            return getattr(self, "policy_id", None)

    def get_license_user(self) -> dict:
        with self._lock:
            return getattr(self, "user", None)

    def get_order_store_id(self):
        with self._lock:
            return getattr(self, "order_store_id", None)

    def get_version(self):
        with self._lock:
            return getattr(self, "version", None)
    
    def get_activation_date(self):
        with self._lock:
            return getattr(self,"activation_date",None)
