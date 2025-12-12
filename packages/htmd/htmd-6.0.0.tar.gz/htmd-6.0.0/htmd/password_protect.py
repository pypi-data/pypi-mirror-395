import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def encrypt_text(post_text: str) -> str:
    message = post_text.encode('utf-8')

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    pem_str = pem.decode('utf-8')
    pem_str = pem_str.replace('-----BEGIN PRIVATE KEY-----\n', '').replace('-----END PRIVATE KEY-----\n', '')

    public_key = private_key.public_key()

    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    ciphertext_base64 = base64.b64encode(ciphertext).decode('utf-8')
    return pem_str, ciphertext_base64
