import json
from datetime import datetime
from typing import Dict, Any, Optional, Callable
import requests
import asyncio

from .utils.encrypt import encrypt_payload
from .utils.sign import sign_payload
from .exceptions import SDKError, ValidationError, APIError


class ZKIntentSDK:
    """Main SDK class for interacting with the ZK Intent API."""
    
    def __init__(self, api_key: str, hmac_secret: str, base_url: str = "http://localhost:8000/api"):
        """
        Initialize the ZKIntentSDK.
        
        Args:
            api_key: Your API key
            hmac_secret: HMAC secret for signing requests
            base_url: Base URL for the API (default: http://localhost:8000/api)
        
        Raises:
            ValidationError: If required parameters are missing
        """
        if not api_key:
            raise ValidationError("api_key is required")
        if not hmac_secret:
            raise ValidationError("hmac_secret is required")
        
        self.api_key = api_key
        self.hmac_secret = hmac_secret
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        # Configure session headers
        self.session.headers.update({
            'User-Agent': 'ZKIntentSDK-Python/1.0.0',
            'Accept': 'application/json'
        })
    
    def create_intent(self, payload: Dict[str, Any], wallet_signature: str, 
                      metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new ZK intent.
        
        Args:
            payload: Transaction payload {recipient, amount, token, walletType}
            wallet_signature: Wallet signature of the payload
            metadata: Optional metadata {note, priority, ...}
        
        Returns:
            Backend response as dictionary
        
        Raises:
            ValidationError: If validation fails
            APIError: If API request fails
        """
        # 1️⃣ Validate input
        self._validate_create_intent_input(payload, wallet_signature)
        
        # 2️⃣ Combine payload and wallet signature
        combined_data = {**payload, 'walletSignature': wallet_signature}
        
        # 3️⃣ Encrypt combined data
        encrypted_data = encrypt_payload(combined_data, self.hmac_secret)
        
        # 4️⃣ Generate HMAC signature for request
        timestamp = datetime.utcnow().isoformat() + "Z"
        signature = sign_payload(encrypted_data, self.hmac_secret, timestamp)
        
        # 5️⃣ Prepare request data
        request_data = {
            "intent": {"payload": payload},  # raw payload also sent
            "encryptedData": encrypted_data,
            "metadata": metadata or {}
        }
        
        # 6️⃣ Send request to backend
        try:
            url = f"{self.base_url}/intents/"
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "x-signature": signature,
                "x-timestamp": timestamp
            }
            
            response = self.session.post(url, json=request_data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Intent submitted successfully. ID: {result.get('intentId')}")
            return result
            
        except requests.exceptions.RequestException as e:
            error_message = self._extract_error_message(e)
            print(f"❌ Failed to submit intent: {error_message}")
            raise APIError(f"API request failed: {error_message}", status_code=getattr(e.response, 'status_code', None))
    
    def get_intent(self, intent_id: str) -> Dict[str, Any]:
        """
        Get intent details by ID.
        
        Args:
            intent_id: ID of the intent to retrieve
        
        Returns:
            Intent data as dictionary
        """
        try:
            url = f"{self.base_url}/intents/{intent_id}/"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to get intent: {e}")
    
    def list_intents(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        List all intents with pagination.
        
        Args:
            limit: Number of intents to return
            offset: Pagination offset
        
        Returns:
            List of intents
        """
        try:
            url = f"{self.base_url}/intents/"
            params = {'limit': limit, 'offset': offset}
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Failed to list intents: {e}")
    
    def _validate_create_intent_input(self, payload: Dict[str, Any], wallet_signature: str) -> None:
        """Validate create intent input parameters."""
        if not payload or not isinstance(payload, dict):
            raise ValidationError("payload must be a non-empty dictionary")
        
        if not wallet_signature or not isinstance(wallet_signature, str):
            raise ValidationError("wallet_signature is required and must be a string")
        
        # Validate required fields
        required_fields = ['recipient', 'amount', 'token', 'walletType']
        missing_fields = [field for field in required_fields if field not in payload]
        
        if missing_fields:
            raise ValidationError(f"Missing required payload fields: {', '.join(missing_fields)}")
        
        # Validate amount
        amount = payload.get('amount')
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValidationError("amount must be a positive number")
        
        # Validate recipient is a string (assuming Ethereum address)
        recipient = payload.get('recipient', '')
        if not isinstance(recipient, str) or len(recipient) < 20:
            raise ValidationError("recipient must be a valid address string")
    
    def _extract_error_message(self, error: requests.exceptions.RequestException) -> str:
        """Extract error message from request exception."""
        if hasattr(error, 'response') and error.response is not None:
            try:
                error_data = error.response.json()
                return error_data.get('message', error_data.get('detail', error.response.text))
            except:
                return error.response.text
        return str(error)
    
    async def listen_proof_async(self, intent_id: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Listen for proof ready event over WebSocket (async version).
        
        Args:
            intent_id: ID of the intent
            callback: Function called with proof data
        """
        from .utils.websockets import connect_websocket
        
        if not intent_id:
            raise ValidationError("intent_id is required")
        
        ws_url = self.base_url.replace("http://", "ws://").replace("https://", "wss://")
        ws_url = f"{ws_url}/ws/proofs/{intent_id}/"
        
        await connect_websocket(ws_url, callback)
    
    def listen_proof(self, intent_id: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Synchronous wrapper for listen_proof_async.
        
        Args:
            intent_id: ID of the intent
            callback: Function called with proof data
        """
        if not intent_id:
            raise ValidationError("intent_id is required")
        
        # Run the async function in an event loop
        asyncio.run(self.listen_proof_async(intent_id, callback))
    
    def close(self):
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()