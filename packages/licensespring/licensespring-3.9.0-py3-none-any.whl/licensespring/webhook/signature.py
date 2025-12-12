import hmac
import time
from hashlib import sha256

from licensespring.webhook.error import SignatureVerificationError
from licensespring.webhook.utils import secure_compare


class WebhookSignature:
    EXPECTED_SCHEME = "v1"

    @staticmethod
    def compute_signature(payload, secret):
        mac = hmac.new(
            secret.encode("utf-8"),
            msg=payload.encode("utf-8"),
            digestmod=sha256,
        )
        return mac.hexdigest()

    @staticmethod
    def get_timestamp_and_signatures(header, scheme):
        list_items = [i.split("=", 2) for i in header.split(",")]
        timestamp = int([i[1] for i in list_items if i[0] == "t"][0])
        signatures = [i[1] for i in list_items if i[0] == scheme]
        return timestamp, signatures

    @classmethod
    def verify_header(cls, payload, header, secret, tolerance=None):
        try:
            timestamp, signatures = cls.get_timestamp_and_signatures(
                header, cls.EXPECTED_SCHEME
            )
        except Exception:
            raise SignatureVerificationError(
                "Unable to extract timestamp and signatures from header",
                header,
                payload,
            )

        if not signatures:
            raise SignatureVerificationError(
                f"No signatures found with expected scheme {cls.EXPECTED_SCHEME}",
                header,
                payload,
            )

        signed_payload = "%d.%s" % (timestamp, payload)
        expected_sig = cls.compute_signature(signed_payload, secret)
        if not any(secure_compare(expected_sig, s) for s in signatures):
            raise SignatureVerificationError(
                "No signatures found matching the expected signature for payload",
                header,
                payload,
            )

        if tolerance and timestamp < time.time() - tolerance:
            raise SignatureVerificationError(
                f"Timestamp outside the tolerance zone ({timestamp})",
                header,
                payload,
            )

        return True
