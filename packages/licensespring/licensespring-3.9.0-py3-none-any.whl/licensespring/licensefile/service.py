import logging
from base64 import b64decode, b64encode
from datetime import datetime, timezone

from Crypto.Hash import SHA1, SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Util.number import bytes_to_long, long_to_bytes

from licensespring.api import APIClient
from licensespring.floating_server import FloatingAPIClient
from licensespring.licensefile.config import Configuration
from licensespring.licensefile.error import ErrorType, LicenseActivationException
from licensespring.licensefile.offline_activation_guard import (
    OfflineActivation,
    OfflineActivationGuard,
)


class APIService(APIClient):
    def __init__(self, conf: Configuration) -> None:
        super().__init__(
            api_key=conf._api_key,
            shared_key=conf._shared_key,
            hardware_id_provider=conf._hardware_id_provider,
            verify_license_signature=conf._verify_license_signature,
            signature_verifier=conf._signature_verifier,
            api_domain=conf._api_domain,
            api_version=conf._api_version,
            api_protocol=conf._api_protocol,
            client_id=conf._client_id,
            client_secret=conf._client_secret,
        )

        self._conf = conf
        self.floating_client = FloatingAPIClient(
            api_protocol=conf._api_protocol,
            api_domain=conf._api_domain,
            api_version=conf._api_version,
            verify_license_signature=conf._verify_license_signature,
            certificate_chain_path=conf._certificate_chain_path,
        )

    def create_activation_guard(self, id: str) -> OfflineActivationGuard:
        """
        Creates OfflineActivationGuard object

        Args:
            id (str): response_id

        Returns:
            OfflineActivationGuard
        """

        offline_guard = OfflineActivationGuard()
        offline_guard.set_id(id=id)
        offline_guard.set_device_id(self.hardware_id_provider.get_id())
        offline_guard.set_date_created()

        return offline_guard

    def check_guard(self, offline_data: OfflineActivation, id: str):
        """
        Checks the validity of the .lic file

        Args:
            offline_data (OfflineActivation): OfflineActivation object

        Raises:
            LicenseActivationException: Activation data is not valid
            LicenseActivationException: Response file ID mismatch
            LicenseActivationException: License does not belong to this device
        """

        if offline_data._guard._date_created > datetime.now(timezone.utc).replace(
            tzinfo=None
        ):
            raise LicenseActivationException(
                ErrorType.OFFLINE_ACTIVATION_ERROR,
                "Activation data is not valid, please restart activation process.",
            )

        elif offline_data._guard._id != id:
            raise LicenseActivationException(
                ErrorType.OFFLINE_ACTIVATION_ERROR,
                "Response file ID mismatch, please restart activation process.",
            )

        elif offline_data._guard._device_id != self._conf._hardware_id_provider.get_id(
            self
        ):
            raise LicenseActivationException(
                ErrorType.OFFLINE_ACTIVATION_ERROR,
                "License does not belong to this device.",
            )

    def get_air_gap_activation_code(
        self, initialization_code: str, license_key: str
    ) -> str:
        """
        Get air gap activation code

        Args:
            initialization_code (str): initialization code
            license_key (str): license key

        Returns:
            str: activation code
        """
        hardware_id = self.hardware_id_provider.get_id()
        message = (hardware_id + license_key).encode("utf-8")
        decoded_key = b64decode(initialization_code)

        private_key = ECC.construct(curve="P-256", d=bytes_to_long(decoded_key))

        digest = SHA1.new(message)

        signer = DSS.new(private_key, "deterministic-rfc6979")
        signature = signer.sign(digest)

        r, s = int.from_bytes(
            signature[: len(signature) // 2], byteorder="big"
        ), int.from_bytes(signature[len(signature) // 2 :], byteorder="big")

        degree = private_key.pointQ.size_in_bits()
        bn_len = (degree + 7) // 8
        r_bytes = long_to_bytes(r, bn_len)
        s_bytes = long_to_bytes(s, bn_len)

        raw_buf = r_bytes + s_bytes

        return b64encode(raw_buf).decode("utf-8")

    def verify_confirmation_code(
        self, confirmation_code: str, license_key: str, policy_id: str
    ) -> bool:
        """
        Verify confirmation code

        Args:
            confirmation_code (str): confirmation code
            license_key (str): license key
            policy_id (str): policy id

        Returns:
            bool: True if verification was successful, otherwise False.
        """
        hardware_id = self.hardware_id_provider.get_id()
        message = (hardware_id + license_key + policy_id).encode("utf-8")
        decoded_key = b64decode(self._conf.air_gap_public_key)

        hex_key = decoded_key.hex()
        gx = int(hex_key[:64], 16)
        gy = int(hex_key[64:], 16)

        public_key = ECC.construct(curve="P-256", point_x=gx, point_y=gy)
        decoded_signature = b64decode(confirmation_code)

        signature = DSS.new(public_key, "fips-186-3")
        digest = SHA256.new(message)

        try:
            signature.verify(digest, decoded_signature)
            return True
        except (ValueError, TypeError):
            logging.info("Failed to verify EC Signature")
            return False

    def activate_air_gapped_licenses(
        self, data: OfflineActivation, license_key: str, policy_id: str
    ) -> dict:
        """
        Activate air gapped license

        Args:
            data (OfflineActivation): Offline activation data
            license_key (str): license key
            policy_id (str): policy id

        Raises:
            LicenseActivationException: Policy ID mismatch

        Returns:
            dict: response
        """
        response = data.decode_offline_activation()
        logging.info("Offline file activation id:", response["id"])

        if str(response["id"]) != policy_id:
            raise LicenseActivationException(
                ErrorType.AIR_GAP_ACTIVATION_ERROR,
                "Policy file ID mismatch, please use another file.",
            )

        if data._use_guard:
            logging.info("Checking activation guard")
            self.check_guard(data, id=license_key)
            logging.info("Activation guard check passed")

        response["license_key"] = license_key
        response["license_type"] = response["default_license_type"]
        response["policy_id"] = response["id"]

        del response["default_license_type"]
        # Next line insures that product is not overwritten with product_id
        del response["product"]

        return response

    def activate_license_offline(self, data: OfflineActivation) -> dict:
        """
        Decodes the data and checks the guard file

        Args:
            data (OfflineActivation): offline activation data

        Returns:
            dict: response
        """
        response = data.decode_offline_activation()

        logging.info("Offline file activation id:", response["request_id"])

        if data._use_guard:
            logging.info("Checking activation guard")
            self.check_guard(data, response["request_id"])
            logging.info("Activation guard check passed")

        return response

    def activate_bundle_offline(self, data: OfflineActivation) -> dict:
        """
        Decodes the data and checks the guard file

        Args:
            data (OfflineActivation): offline activation data

        Returns:
            dict: response
        """
        response = data.decode_offline_activation()

        product_short_code = (
            response.get("licenses", [{}])[0]
            .get("product_details", {})
            .get("short_code")
        )

        if product_short_code != self._conf._product:
            raise LicenseActivationException(
                ErrorType.PRODUCT_MISMATCH,
                "Response file product is not same as within the configuration.",
            )

        if response.get("bundle_signature_v2") is None:
            raise LicenseActivationException(
                ErrorType.SIGNATURE_MISSING_ERROR,
                "Response file is missing the bundle signature",
            )

        logging.info(
            "Offline file activation id:", response["licenses"][0]["request_id"]
        )

        if data._use_guard:
            logging.info("Checking activation guard")
            self.check_guard(data, response["licenses"][0]["request_id"])
            logging.info("Activation guard check passed")

        return response["licenses"]
