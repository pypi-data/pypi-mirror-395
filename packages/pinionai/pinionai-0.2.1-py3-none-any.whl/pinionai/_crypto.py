import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class EncryptionManager:
    """
    A utility class to handle secure encryption and decryption of strings
    using a client secret.

    This implementation uses AES-GCM for authenticated encryption, ensuring
    both confidentiality and integrity. The encryption key is derived from
    the client secret using PBKDF2.
    """
    # --- Constants for cryptographic parameters ---
    _AES_KEY_SIZE = 32      # AES key size in bytes (256 bits)
    _GCM_NONCE_SIZE = 12    # GCM nonce size in bytes (recommended)
    _PBKDF2_SALT_SIZE = 16  # PBKDF2 salt size in bytes (good minimum)
    _PBKDF2_ITERATIONS = 390_000 # Higher is more secure

    def __init__(self, client_secret: str):
        if not client_secret:
            raise ValueError("Client secret cannot be empty.")
        self._client_secret = client_secret.encode('utf-8')
        self._backend = default_backend()

    def _derive_key(self, salt: bytes) -> bytes:
        """Derives a 256-bit AES key from the client secret using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self._AES_KEY_SIZE,
            salt=salt,
            iterations=self._PBKDF2_ITERATIONS,
            backend=self._backend
        )
        return kdf.derive(self._client_secret)

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypts a string using AES-GCM and returns a URL-safe base64 encoded string.
        The output format is: salt + nonce + ciphertext + tag
        """
        if not isinstance(plaintext, str) or not plaintext:
            raise ValueError("Plaintext must be a non-empty string.")

        salt = os.urandom(self._PBKDF2_SALT_SIZE)
        nonce = os.urandom(self._GCM_NONCE_SIZE)
        key = self._derive_key(salt)

        # Using the higher-level AESGCM is often simpler and safer
        aesgcm = AESGCM(key)
        ciphertext_with_tag = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)

        encrypted_data = salt + nonce + ciphertext_with_tag
        return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypts a base64 encoded string that was encrypted by the `encrypt` method.
        """
        try:
            encrypted_data = base64.urlsafe_b64decode(encrypted_text)

            # 1. Extract the components using the CORRECT constant name
            salt = encrypted_data[:self._PBKDF2_SALT_SIZE]
            nonce = encrypted_data[self._PBKDF2_SALT_SIZE : self._PBKDF2_SALT_SIZE + self._GCM_NONCE_SIZE]
            # The rest of the data is the ciphertext + tag
            ciphertext_with_tag = encrypted_data[self._PBKDF2_SALT_SIZE + self._GCM_NONCE_SIZE:]

            # 2. Derive the key using the extracted salt
            key = self._derive_key(salt)

            # 3. Decrypt and verify the data
            aesgcm = AESGCM(key)
            decrypted_bytes = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
            
            return decrypted_bytes.decode('utf-8')

        except Exception as e:
            # Broad exception to catch any cryptographic error (e.g., InvalidTag)
            # or decoding/slicing error, which indicates invalid input.
            raise ValueError("Decryption failed. The data may be tampered, "
                             "corrupt, or encrypted with a different secret.") from e
