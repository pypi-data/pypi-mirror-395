import hmac
import hashlib
from typing import Dict, Any

from ..exceptions import CryptoError


def sign_payload(encrypted_data: Dict[str, str], secret: str, timestamp: str) -> str:
    """
    Generate HMAC-SHA256 signature for the encrypted data.
    Compatible with Node.js CryptoJS.HmacSHA256.
    
    Args:
        encrypted_data: Dictionary with 'ciphertext' key
        secret: HMAC secret
        timestamp: Timestamp string
    
    Returns:
        HMAC-SHA256 hash as hex string
    
    Raises:
        CryptoError: If signing fails
    """
    try:
        ciphertext = encrypted_data.get('ciphertext', '')
        
        # Create message in format: ciphertext:timestamp
        message = f"{ciphertext}:{timestamp}"
        
        # Create HMAC-SHA256 signature
        signature = hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature
        
    except Exception as e:
        raise CryptoError(f"Signing failed: {str(e)}")