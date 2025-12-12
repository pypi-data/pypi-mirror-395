from __future__ import annotations

from datetime import datetime, timedelta, timezone

from licensespring.licensefile.error import (
    ConsumptionError,
    ErrorType,
    ItemNotFoundError,
    LicenseSpringTypeError,
)


class Feature:
    def __init__(self) -> None:
        self.floating_end_date = datetime.now(timezone.utc).replace(tzinfo=None)
        self.floating_start_date = datetime(year=2099, month=1, day=1)

        """
        Attributes:
            Feature fields: id,feature_type,expiry_date ...


        Methods:
            json_to_attribute(feature: dict): Converts JSON data into attributes for the Feature object
        """

    def json_to_attribute(self, feature: dict):
        """
        Converts JSON data into attributes for the Feature object. Special handling is applied to date fields
        to ensure they are parsed correctly from ISO format. If the feature is of type 'consumption' and doesn't
        already have a 'local_consumption' attribute, it initializes this attribute with 0.

        Args:
            feature (dict): A dictionary containing feature information, including any potential date fields and
            other attributes like 'feature_type' and 'local_consumption'.
        """
        for key, value in feature.items():

            if (
                key in ["expiry_date", "floating_end_date", "floating_start_date"]
                and value
            ):
                if value.endswith("Z"):
                    value = value[:-1]
                setattr(self, key, datetime.fromisoformat(value).replace(tzinfo=None))

            else:
                setattr(self, key, value)

        if self.feature_type == "consumption" and not hasattr(
            self, "local_consumption"
        ):
            self.local_consumption = 0

    def floating_end_datetime(self):
        if not hasattr(self, "floating_end_date"):
            setattr(
                self,
                "floating_end_date",
                datetime.now(timezone.utc).replace(tzinfo=None),
            )
        return self.floating_end_date

    def is_online_floating(self):
        return self.is_floating_cloud

    def is_offline_floating(self):
        return self.is_floating

    def floating_is_expired(self):
        if self.expiry_date == None or not hasattr(self, "expiry_date"):
            return False

        return datetime.now(timezone.utc).replace(tzinfo=None) > self.expiry_date


class FeatureManager:
    def __init__(self) -> None:
        """
        Initializes a new FeatureManager object that will hold and manage multiple Feature objects.

        Attributes:
            Feature objects

        Methods:
            return_features_list(): Returns lists of features
            remove_features(): Removes features that are not present in the latest feature response
            json_to_attribute(): JSON to attributes
            attributes_to_list(): Attributes to list
            add_local_consumption(feature_code, consumptions=1): Adds a specified number of consumptions to a feature
            register_feature(feature_code): Registers a feature fields as being in use.
            release_feature(self,feature_code): Releases a previously registered feature.

        """
        pass

    def return_features_list(self) -> list:
        return [key for key, feat in self.__dict__.items()]

    def remove_features(self, feature_response) -> None:
        """
        Removes features from the manager that are not present in the latest feature response.

        Args:
            feature_response (iterable): An iterable of dictionaries, each containing a 'code' key
            representing the feature code.

        """
        existing_features = set(self.return_features_list())

        new_features = set([feature["code"] for feature in feature_response])

        remove_features = existing_features - new_features

        for feature in remove_features:
            delattr(self, feature)

    def json_to_attribute(self, feature_response: dict):
        self.remove_features(feature_response)

        for feature in feature_response:
            if not hasattr(self, feature["code"]):
                setattr(self, feature["code"], Feature())

            feature_obj = getattr(self, feature["code"])

            feature_obj.json_to_attribute(feature)

    def attributes_to_list(self) -> list:
        feature_list = []

        for _, feat in self.__dict__.items():
            data = {}

            for key, value in feat.__dict__.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()

                else:
                    data[key] = value

            feature_list.append(data)

        return feature_list

    def add_local_consumption(self, feature_code, consumptions=1) -> None:
        """
        Adds a specified number of local consumptions to a  feature, updating its consumption count.

        This method identifies a feature by its code and increments its local consumption by a given number. It performs several checks to validate the operation:
        1. It verifies the existence of the feature object. If the feature does not exist, it raises an `ItemNotFoundError`.
        2. It checks if the feature's type is set to "consumption". If not, a `LicenseSpringTypeError` is raised to indicate the feature is not of the consumption type.
        3. It determines whether the feature allows unlimited consumptions. If so, it directly increments the local consumption count.
        4. For limited consumption features, it checks if adding the specified consumptions would exceed the feature's maximum allowed consumptions and overages. If this limit would be exceeded, it raises a `ConsumptionError`.

        Args:
            feature_code (str): The code identifying the feature to which consumptions are to be added.
            consumptions (int, optional): The number of consumptions to add. Defaults to 1.

        Raises:
            ItemNotFoundError: If the feature specified by `feature_code` does not exist.
            LicenseSpringTypeError: If the identified feature is not of the "consumption" type.
            ConsumptionError: If adding the specified number of consumptions would exceed the feature's consumption limits.

        This method updates the `local_consumption` attribute of the specified feature object, reflecting the addition of the specified number of consumptions.
        """

        feature_obj = getattr(self, feature_code, None)

        if feature_obj == None:
            raise ItemNotFoundError(
                ErrorType.UNSUPPORTED_PRODUCT_FEATURE, "Features do not exists"
            )

        if feature_obj.feature_type != "consumption":
            raise LicenseSpringTypeError(
                ErrorType.WRONG_FEATURE_TYPE, "Feature not consumption type"
            )

        elif (
            getattr(feature_obj, "allow_negative_consumptions", True) == False
            and consumptions < 0
        ):
            raise ConsumptionError(
                error_type=ErrorType.NEGATIVE_CONSUMPTION_NOT_ALLOWED,
                message="Negative consumptions not allowed",
            )

        elif feature_obj.allow_unlimited_consumptions:
            feature_obj.local_consumption += consumptions

        elif (
            feature_obj.max_consumption + feature_obj.max_overages
            < consumptions
            + feature_obj.total_consumptions
            + feature_obj.local_consumption
        ):
            raise ConsumptionError(
                ErrorType.NOT_ENOUGH_FEATURE_CONSUMPTIONS, "Not enough consumptions"
            )

        else:
            feature_obj.local_consumption += consumptions

    def register_feature(self, feature_code):
        """
        Registers a feature fields as being in use.

        Args:
            feature_code (str): The code of the feature to register as in use.
        """
        feature_obj = getattr(self, feature_code, None)

        if feature_obj.is_floating_cloud or feature_obj.is_floating:
            feature_obj.floating_start_date = datetime.now(timezone.utc).replace(
                tzinfo=None
            )
            feature_obj.floating_end_date = feature_obj.floating_start_date + timedelta(
                minutes=feature_obj.floating_timeout
            )

    def release_feature(self, feature_code: str):
        """
        Releases a previously registered feature.

        Args:
            feature_code (str): The code of the feature to release.
        """

        feature_obj = getattr(self, feature_code, None)

        if feature_obj.is_floating_cloud or feature_obj.is_floating:
            feature_obj.floating_start_date = datetime(year=2099, month=1, day=1)
            feature_obj.floating_end_date = datetime.now(timezone.utc).replace(
                tzinfo=None
            )
            if feature_obj.floating_in_use_devices > 0:
                feature_obj.floating_in_use_devices -= 1

    def get_feature_dict(self, feature_code: str) -> dict:
        """
        Get feature data inside dictionary

        Args:
            feature_code (str): feature short code

        Returns:
            dict: feature data
        """

        feature_obj = getattr(self, feature_code, None)

        if feature_obj:
            return feature_obj.__dict__
