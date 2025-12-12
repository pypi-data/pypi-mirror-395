class SignatureVerificationError(Exception):
    def __init__(self, message, sig_header, payload):
        self.message = message
        self.sig_header = sig_header
        self.payload = payload

    def __str__(self):
        return self.message

    def __repr__(self):
        return str(self)
