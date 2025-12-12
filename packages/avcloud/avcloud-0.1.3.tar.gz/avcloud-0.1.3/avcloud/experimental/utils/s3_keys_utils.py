from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jose import jwe


def generate_key_pair() -> tuple[str, str]:
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    public_key = private_key.public_key()

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),  # or a password
    ).decode("utf-8")

    return private_key_pem, public_key_pem


def decrypt_with_private_key(encrypted_key: str, private_key_pem: str) -> str:
    # Convert string PEM back to bytes for load_pem_private_key
    private_key_bytes = private_key_pem.encode("utf-8")
    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,
    )

    decrypted = jwe.decrypt(encrypted_key, private_key)
    return decrypted.decode("utf-8")
