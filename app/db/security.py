"""
Security utilities for database
"""

import hashlib
import base64


def hash_bytes(message: bytes) -> bytes:
    """Hash a message into a raw bytes digest.

    ## Return
    `digest` where, `digest` is the hashed message (as bytes).
    """
    hash_obj = hashlib.md5(message)
    digest = hash_obj.digest()
    digest = base64.b64encode(digest)  # convert to byte-safe bytestring

    return digest
