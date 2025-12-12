"""
cryptographic identity and signature verification for a2a messages.

provides ed25519 signature verification to ensure message authenticity.
"""

import base64
import hashlib
import json
from typing import Any, Dict

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.exceptions import InvalidSignature
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class SignatureVerificationError(Exception):
    """raised when signature verification fails."""
    pass


def compute_payload_hash(
    sender: str,
    recipient: str,
    message: Dict[str, Any],
    thread_id: str,
) -> bytes:
    """
    compute canonical hash of message payload for signing/verification.
    
    creates deterministic byte representation by:
    1. concatenating sender + recipient + thread_id
    2. adding json-serialized message (sorted keys)
    3. hashing with sha256
    
    args:
        sender: canonical agent uri of sender
        recipient: canonical agent uri of recipient
        message: the message envelope dict
        thread_id: thread identifier from message
        
    returns:
        sha256 hash bytes
    """
    # create canonical payload
    payload_parts = [
        sender,
        recipient,
        thread_id,
        json.dumps(message, sort_keys=True, separators=(",", ":")),
    ]
    payload_str = "|".join(payload_parts)
    
    # hash with sha256
    return hashlib.sha256(payload_str.encode("utf-8")).digest()


def verify_signature(
    public_key_b64: str,
    signature_b64: str,
    sender: str,
    recipient: str,
    message: Dict[str, Any],
    thread_id: str,
) -> bool:
    """
    verify ed25519 signature on message envelope.
    
    validates that the message was signed by the holder of the private key
    corresponding to the provided public key.
    
    args:
        public_key_b64: base64-encoded ed25519 public key (32 bytes)
        signature_b64: base64-encoded signature (64 bytes)
        sender: canonical agent uri of sender
        recipient: canonical agent uri of recipient
        message: the message envelope dict
        thread_id: thread identifier from message
        
    returns:
        True if signature is valid
        
    raises:
        SignatureVerificationError: if signature is invalid or crypto unavailable
    """
    if not CRYPTO_AVAILABLE:
        raise SignatureVerificationError(
            "cryptography library not available - install with: pip install cryptography"
        )
    
    try:
        # decode public key
        public_key_bytes = base64.b64decode(public_key_b64)
        public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
        
        # decode signature
        signature_bytes = base64.b64decode(signature_b64)
        
        # compute payload hash
        payload_hash = compute_payload_hash(sender, recipient, message, thread_id)
        
        # verify signature
        public_key.verify(signature_bytes, payload_hash)
        return True
        
    except InvalidSignature:
        return False
    
    except Exception as e:
        raise SignatureVerificationError(f"signature verification failed: {e}") from e


def generate_keypair() -> tuple[str, str]:
    """
    generate new ed25519 keypair for testing/development.
    
    returns:
        tuple of (private_key_b64, public_key_b64)
        
    raises:
        SignatureVerificationError: if crypto unavailable
    """
    if not CRYPTO_AVAILABLE:
        raise SignatureVerificationError(
            "cryptography library not available - install with: pip install cryptography"
        )
    
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import (
        Encoding,
        NoEncryption,
        PrivateFormat,
        PublicFormat,
    )
    
    # generate keypair
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    # serialize to bytes
    private_bytes = private_key.private_bytes(
        encoding=Encoding.Raw,
        format=PrivateFormat.Raw,
        encryption_algorithm=NoEncryption(),
    )
    public_bytes = public_key.public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )
    
    # encode to base64
    private_b64 = base64.b64encode(private_bytes).decode("utf-8")
    public_b64 = base64.b64encode(public_bytes).decode("utf-8")
    
    return (private_b64, public_b64)


def sign_message(
    private_key_b64: str,
    sender: str,
    recipient: str,
    message: Dict[str, Any],
    thread_id: str,
) -> str:
    """
    sign message envelope with ed25519 private key.
    
    args:
        private_key_b64: base64-encoded ed25519 private key
        sender: canonical agent uri of sender
        recipient: canonical agent uri of recipient
        message: the message envelope dict
        thread_id: thread identifier from message
        
    returns:
        base64-encoded signature
        
    raises:
        SignatureVerificationError: if crypto unavailable or signing fails
    """
    if not CRYPTO_AVAILABLE:
        raise SignatureVerificationError(
            "cryptography library not available - install with: pip install cryptography"
        )
    
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        
        # decode private key
        private_key_bytes = base64.b64decode(private_key_b64)
        private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
        
        # compute payload hash
        payload_hash = compute_payload_hash(sender, recipient, message, thread_id)
        
        # sign
        signature_bytes = private_key.sign(payload_hash)
        
        # encode to base64
        return base64.b64encode(signature_bytes).decode("utf-8")
        
    except Exception as e:
        raise SignatureVerificationError(f"message signing failed: {e}") from e

