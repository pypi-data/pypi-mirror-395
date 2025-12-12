from base64 import b32decode, b32encode, urlsafe_b64decode, urlsafe_b64encode
from os import environ

from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.serialization import (Encoding,
                                                          PublicFormat,
                                                          load_der_private_key,
                                                          load_der_public_key)


class E2EE:
    def __init__(self, public_key: bytes = None, public_salt: bytes = None) -> None:
        if not public_key and not public_salt:
            self.server = True
            self.signing_private_key = self.load_certificate(environ["PRIVATE_KEY"])
        else:
            self.server = False
            self.signing_public_key = self.load_certificate(environ["PUBLIC_KEY"])
            self.load_peer_public_key(public_key, public_salt, exchange=False)

        self.shared_private_key = None
        self.shared_private_salt = None
        self.private_salt = ec.generate_private_key(ec.SECP521R1())
        self._public_salt = self.private_salt.public_key()
        self.private_key = ec.generate_private_key(ec.SECP521R1())
        self._public_key = self.private_key.public_key()

        if public_key and public_salt:
            self.__exchange_keys(self.peer_public_key, self.peer_public_salt)
            self.__setup_symmetric_encryption()

    def load_certificate(self, path):
        with open(path, "rb") as key_file:
            raw_bytes = key_file.read()
        if self.server:
            certificate = load_der_private_key(raw_bytes, password=None)
        else:
            certificate = load_der_public_key(raw_bytes)
        return certificate

    def sign_key(self, key):
        return self.signing_private_key.sign(key, ec.ECDSA(hashes.SHA224()))

    def verify_key(self, key, sig):
        raw_key = b32decode(key.encode("utf-8"))
        raw_sig = b32decode(sig.encode("utf-8"))
        try:
            self.signing_public_key.verify(raw_sig, raw_key, ec.ECDSA(hashes.SHA224()))
            return ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP521R1(), raw_key)
        except InvalidSignature:
            raise InvalidSignature("The signature of the received key is invalid")

    @property
    def public_salt(self):
        return self.__export_public_key(self._public_salt)

    @property
    def public_key(self):
        return self.__export_public_key(self._public_key)

    def __export_public_key(self, key):
        exported_key = key.public_bytes(
            encoding=Encoding.X962, format=PublicFormat.UncompressedPoint
        )
        encoded_key = b32encode(exported_key)
        if self.server:
            signature = b32encode(self.sign_key(exported_key))
            return encoded_key.decode("utf-8"), signature.decode("utf-8")
        else:
            return encoded_key.decode("utf-8")

    def __exchange_keys(self, public_key, public_salt):
        self.shared_private_key = self.private_key.exchange(ec.ECDH(), public_key)
        self.shared_private_salt = self.private_salt.exchange(ec.ECDH(), public_salt)

    def __setup_symmetric_encryption(self):
        self.derived_secret_key = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=self.shared_private_salt,
            iterations=100000,
            length=32,
        ).derive(self.shared_private_key)
        self.fernet = Fernet(urlsafe_b64encode(self.derived_secret_key))

    def load_peer_public_key(
        self, public_key: bytes, public_salt: bytes, exchange: bool = True
    ):
        if self.server:
            raw_key = b32decode(public_key.encode("utf-8"))
            raw_salt = b32decode(public_salt.encode("utf-8"))
            self.peer_public_key = ec.EllipticCurvePublicKey.from_encoded_point(
                ec.SECP521R1(), raw_key
            )
            self.peer_public_salt = ec.EllipticCurvePublicKey.from_encoded_point(
                ec.SECP521R1(), raw_salt
            )
        else:
            self.peer_public_key = self.verify_key(*public_key)
            self.peer_public_salt = self.verify_key(*public_salt)
        if exchange and self.peer_public_key and self.peer_public_salt:
            self.__exchange_keys(self.peer_public_key, self.peer_public_salt)
            self.__setup_symmetric_encryption()

    def encrypt(self, message: str):
        unencoded_secret_message = self.fernet.encrypt(message.encode("utf-8"))
        return urlsafe_b64encode(unencoded_secret_message).decode("utf-8")

    def decrypt(self, encoded_encrypted_message: str):
        encrypted_message = urlsafe_b64decode(encoded_encrypted_message)
        return self.fernet.decrypt(encrypted_message).decode("utf-8")
