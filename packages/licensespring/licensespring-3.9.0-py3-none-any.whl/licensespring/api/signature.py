import base64
import logging

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from OpenSSL import crypto


class SignatureVerifier:
    PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
    MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAwEt7ZQWSzeBYNBwyi3KW
    +XU/6I+ju90R5ZpTvSE4VWL8KSgVJ6bWKIhaKTL2hbUpIQQgS5ZKfa4SEEMdIm5k
    xe0u2F64JFAVQunx/1O/UXsD7ADVt93Q/hxA9Npa16tKepZoyhi79sxpaxyy/WTd
    sZKuTLApX7bWX6/XPhaPjNyiWeeK2Naka44B+F+PwN/ey3rZUra3pBltShwy2dmK
    IxJVmprf5ttMYBB+ouqPin3VgDw5Jq1FZwpLBiOe+ogR+sHu7QYWwLq6AgC4e3Jq
    gryEvqfJr/XkvOnAdcAIZm6tK6DdnLWCy6Onrk7t0VQK5nnGF1CKE+jcAByWopcI
    VCwfYrs1UCSY1YibKXNJoyvEhgLyCC+KAgXKf8omcg1Q18XKu5XSrvrCzXLnRnaF
    NpFDjcg5AJJab78hX7qGPC+e8PjuBYwh2vtx5mFj7/c+T59JM/vXwwvW9DsnDztD
    WEDFhzGanU71NgwrZbRoNSyTW0UjbZsyJVSIX6233Ng0y5L9mDe8p8P+u1B0sXAA
    ozEKL/yG4Qu5r4LIw4iv6JVPT1xbWlH4Vc4KaN3toaf4+G0EkFy6ncvBncWifLAR
    SoWpQ5YsygDdQNVYdmMsoQ76UTuNxo3eZ0sQJjbQVBqlkcXrAdtUCpuojPRsl/Xs
    9zVOJrzZPG0I98E5quNbRkMCAwEAAQ==
    -----END PUBLIC KEY-----"""

    def __init__(self):
        rsa_public_key = RSA.importKey(self.PUBLIC_KEY)
        self.verifier = PKCS115_SigScheme(rsa_public_key)

    def verify_signature(self, message, signature):
        hash = SHA256.new(message)
        self.verifier.verify(hash, signature)

    def verify_license_signature(
        self, hardware_id, auth_value, validity_period, signature_b64
    ):
        message = f'{hardware_id}#{auth_value}#{validity_period if validity_period else ""}'.lower().encode()
        signature = base64.b64decode(signature_b64)
        self.verify_signature(message, signature)

    def verify_license_signature_v2(self, message, signature_b64):
        signature = base64.b64decode(signature_b64)
        self.verify_signature(message, signature)


class FSSignatureVerifier(SignatureVerifier):

    def __init__(self, chain_path: str = None):
        if chain_path:
            self.leaf, self.intermediate, self.root = self.load_certs(chain_path)
            self.verify_chain(self.leaf, self.intermediate, self.root)

            self.verifier = self.load_verifier(self.leaf)

    def load_certs(self, chain_path: str) -> None:
        with open(chain_path, "rb") as file:
            pem_data = file.read()

        certs = []
        logging.info("Loading certificates ...")
        for cert in pem_data.split(b"-----END CERTIFICATE-----"):
            if b"-----BEGIN CERTIFICATE-----" in cert:
                cert += b"-----END CERTIFICATE-----\n"
                certs.append(crypto.load_certificate(crypto.FILETYPE_PEM, cert))

        return certs

    def verify_chain(self, leaf, intermediate, root):
        logging.info("Chain verification")
        store = crypto.X509Store()

        store.add_cert(root)
        store.add_cert(intermediate)

        store_ctx = crypto.X509StoreContext(store, leaf)
        store_ctx.verify_certificate()
        logging.info("Certificate chain is valid!")

    def load_verifier(self, leaf_cert):
        return PKCS115_SigScheme(
            RSA.importKey(
                crypto.dump_publickey(
                    crypto.FILETYPE_PEM, leaf_cert.get_pubkey()
                ).decode()
            )
        )
