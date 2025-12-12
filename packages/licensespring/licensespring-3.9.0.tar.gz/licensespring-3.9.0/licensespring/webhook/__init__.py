import json

from licensespring.webhook.signature import WebhookSignature


class Webhook:
    DEFAULT_TOLERANCE = 300  # 5 minutes

    @staticmethod
    def get_event(payload, sig_header, secret, tolerance=DEFAULT_TOLERANCE):
        WebhookSignature.verify_header(payload, sig_header, secret, tolerance)
        return json.loads(payload)
