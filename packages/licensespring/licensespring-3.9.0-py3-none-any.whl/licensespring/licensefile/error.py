from __future__ import annotations

from enum import Enum, auto


class ErrorType(Enum):
    """Licensefile error"""

    NO_LICENSEFILE = auto()
    CORRUPTED_LICENSEFILE = auto()

    """License status error"""

    LICENSE_NOT_ENABLED = auto()
    LICENSE_NOT_ACTIVE = auto()
    LICENSE_EXPIRED = auto()

    WRONG_LICENSE_TYPE = auto()
    WRONG_FEATURE_TYPE = auto()

    PRODUCT_MISMATCH = auto()
    HARDWARE_ID_MISMATCH = auto()

    VM_NOT_ALLOWED = auto()

    FLOATING_TIMEOUT = auto()

    CLOCK_TAMPERED = auto()

    NOT_ENOUGH_LICENSE_CONSUMPTIONS = auto()
    NOT_ENOUGH_FEATURE_CONSUMPTIONS = auto()
    NEGATIVE_CONSUMPTION_NOT_ALLOWED = auto()

    UNSUPPORTED_PRODUCT_FEATURE = auto()

    """activation"""

    OFFLINE_ACTIVATION_ERROR = auto()
    AIR_GAP_ACTIVATION_ERROR = auto()

    """Watchdogs"""

    LICENSE_WATCHDOG_ERROR = auto()
    FEATURE_WATCHDOG_ERROR = auto()

    """Configuration"""

    AUTHORIZATION_SETUP_ERROR = auto()
    REQUIRED_FIELD_ERROR = auto()

    """Signature missing"""

    SIGNATURE_MISSING_ERROR = auto()


class LicenseSpringException(Exception):
    """Base exception class for all LicenseSpring-related errors."""

    def __init__(self, error_type: ErrorType, message):
        self.error_type = error_type
        self.message = message

    def __repr__(self):
        return "{}(error_name={},error_value={}, message={})".format(
            self.__class__.__name__,
            self.error_type.name,
            self.error_type.value,
            self.message,
        )

    def __str__(self) -> str:
        return f"{self.error_type} ({self.error_type.value}): {self.message}"


class LicenseActivationException(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)


class LicenseDeleted(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)


class LicenseStateException(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)


class LicenseSpringTypeError(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)


class ConfigurationMismatch(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)


class VMIsNotAllowedException(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)


class TimeoutExpiredException(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)


class ClockTamperedException(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)


class ConsumptionError(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)


class ItemNotFoundError(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)


class WatchdogException(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)


class LicenseFileCorruption(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)


class ConfigurationError(LicenseSpringException):
    def __init__(self, error_type: ErrorType, message):
        super().__init__(error_type, message)
