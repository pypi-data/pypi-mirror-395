from base64 import standard_b64decode, standard_b64encode

try:
    from nacl.secret import SecretBox

    HAS_NACL = True
except ImportError:
    HAS_NACL = False
    SecretBox = None  # type: ignore

from pymacaroons2.field_encryptors.base_field_encryptor import BaseFieldEncryptor
from pymacaroons2.utils import convert_to_bytes, convert_to_string, truncate_or_pad


def _check_nacl_available():
    if not HAS_NACL:
        raise ImportError(
            "SecretBoxEncryptor requires 'pynacl' package. "
            "Install it with: pip install pymacaroons2[encryption]"
        )


class SecretBoxEncryptor(BaseFieldEncryptor):

    def __init__(self, signifier=None, nonce=None):
        _check_nacl_available()
        super(SecretBoxEncryptor, self).__init__(signifier=signifier or "sbe::")
        self.nonce = nonce

    def encrypt(self, signature, field_data):
        encrypt_key = truncate_or_pad(signature)
        box = SecretBox(key=encrypt_key)
        encrypted = box.encrypt(convert_to_bytes(field_data), nonce=self.nonce)
        return self._signifier + standard_b64encode(encrypted)

    def decrypt(self, signature, field_data):
        key = truncate_or_pad(signature)
        box = SecretBox(key=key)
        encoded = convert_to_bytes(field_data[len(self.signifier) :])
        decrypted = box.decrypt(standard_b64decode(encoded))
        return convert_to_string(decrypted)
