import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from typing import Dict, Any

from ..exceptions import CryptoError


def encrypt_payload(payload: Dict[str, Any], secret: str) -> Dict[str, str]:
    """
    Encrypt payload using AES-256-CBC encryption.
    Compatible with Node.js CryptoJS.AES.encrypt.
    
    Args:
        payload: Data to encrypt
        secret: Encryption secret/key
    
    Returns:
        Dictionary with 'ciphertext' key
    
    Raises:
        CryptoError: If encryption fails
    """
    try:
        # Convert payload to JSON string
        json_str = json.dumps(payload, separators=(',', ':'))  # Compact JSON
        
        # Generate key from secret (32 bytes for AES-256)
        key = hashlib.sha256(secret.encode()).digest()
        
        # Generate IV from secret (16 bytes for AES)
        iv = hashlib.md5(secret.encode()).digest()
        
        # Pad the data to be multiple of 16 bytes (AES block size)
        padded_data = pad(json_str.encode('utf-8'), AES.block_size)
        
        # Create AES cipher in CBC mode
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Encrypt the data
        ciphertext = cipher.encrypt(padded_data)
        
        # Combine IV and ciphertext
        combined = iv + ciphertext
        
        # Return as Base64 string in a dict (matching Node.js structure)
        return {"ciphertext": base64.b64encode(combined).decode('utf-8')}
        
    except Exception as e:
        raise CryptoError(f"Encryption failed: {str(e)}")