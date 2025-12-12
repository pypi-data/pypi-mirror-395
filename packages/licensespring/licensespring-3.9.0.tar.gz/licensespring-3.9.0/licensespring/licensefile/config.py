from __future__ import annotations

from licensespring.api.signature import FSSignatureVerifier, SignatureVerifier
from licensespring.hardware import HardwareIdProvider
from licensespring.licensefile.error import ConfigurationError, ErrorType


class NoneValue:
    """Descriptor that ensures a value is set and not None."""

    def __set_name__(self, owner, name):
        self.name = name

    def __init__(self):
        self._values = {}

    def __get__(self, instance, owner):
        return self._values.get(instance, "Value not set")

    def __set__(self, instance, value):
        if value is None:
            raise ConfigurationError(
                ErrorType.REQUIRED_FIELD_ERROR, f"{self.name} cannot be None"
            )
        self._values[instance] = value


class Configuration:
    """
    A class to configure settings for a license management system.

    This class encapsulates various configuration settings used for managing
    licenses, including authentication keys, encryption settings, hardware ID
    providers, signature verification, and API details.

    Attributes:
        product (str): Name of the product.
        api_key (str): API key for authentication.
        shared_key (str): Shared key for additional security.
        file_key (str): Encryption key for license files. Default is a sample key.
        file_iv (str): Initialization vector for encryption. Default is a sample vector.
        hardware_id_provider (object): Provider class for hardware ID. Default is HardwareIdProvider.
        verify_license_signature (bool): Flag to enable/disable signature verification. Default is True.
        signature_verifier (object): Verifier class for checking signatures. Default is SignatureVerifier.
        api_domain (str): Domain for the API server. Default is "api.licensespring.com".
        api_version (str): Version of the API. Default is "v4".
        filename (str): Name for the license file. Default is "License".
        file_path (str): Path to save the license file. Default is None.
        grace_period_conf (int): Grace period configuration in days. Default is 12.
        is_guard_file_enabled (bool): Enables guard protection for offline licenses if set to True.
    """

    _file_key = NoneValue()
    _file_iv = NoneValue()

    def __init__(
        self,
        product: str,
        api_key: str = None,
        shared_key: str = None,
        file_key: str = None,
        file_iv: str = None,
        hardware_id_provider=HardwareIdProvider,
        verify_license_signature=True,
        signature_verifier=SignatureVerifier,
        api_domain="api.licensespring.com",
        api_protocol="https",
        api_version="v4",
        filename="License",
        file_path=None,
        grace_period_conf=24,
        is_guard_file_enabled=True,
        air_gap_public_key=None,
        client_id=None,
        client_secret=None,
        certificate_chain_path: str = None,
    ) -> None:
        self._product = product

        self._api_key = api_key
        self._shared_key = shared_key

        self._client_id = client_id
        self._client_secret = client_secret
        self.validate_auth()

        self._file_key = file_key
        self._file_iv = file_iv

        self._hardware_id_provider = hardware_id_provider

        self._verify_license_signature = verify_license_signature
        self._signature_verifier = signature_verifier
        self._certificate_chain_path = certificate_chain_path
        self._api_domain = api_domain
        self._api_version = api_version
        self._api_protocol = api_protocol

        self._filename = filename
        self._file_path = file_path
        self.grace_period_conf = grace_period_conf
        self.is_guard_file_enabled = is_guard_file_enabled
        self.air_gap_public_key = air_gap_public_key

    def validate_auth(self):
        if not (
            (self._client_id and self._client_secret)
            or (self._api_key and self._shared_key)
        ):
            raise ConfigurationError(
                ErrorType.AUTHORIZATION_SETUP_ERROR,
                "api_key and shared_key or client_id and client_secret must be provided.",
            )
