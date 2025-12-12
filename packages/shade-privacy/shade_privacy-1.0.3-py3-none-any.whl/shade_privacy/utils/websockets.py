import json
import websockets
from typing import Dict, Any, Callable

from ..exceptions import WebSocketError


async def connect_websocket(ws_url: str, callback: Callable[[Dict[str, Any]], None]) -> None:
    """
    Connect to WebSocket and listen for messages.
    
    Args:
        ws_url: WebSocket URL
        callback: Function to call when message is received
    
    Raises:
        WebSocketError: If connection fails
    """
    try:
        async with websockets.connect(ws_url) as websocket:
            print(f"🔗 Connected to WebSocket: {ws_url}")
            
            # Send initial ping to keep connection alive
            await websocket.ping()
            
            while True:
                try:
                    message = await websocket.recv()
                    
                    # Handle ping/pong
                    if isinstance(message, bytes):
                        continue
                    
                    try:
                        data = json.loads(message)
                        callback(data)
                    except json.JSONDecodeError:
                        print(f"⚠️  Received non-JSON message: {message}")
                        
                except websockets.exceptions.ConnectionClosed as e:
                    print(f"🔌 WebSocket connection closed: {e}")
                    break
                    
    except Exception as e:
        raise WebSocketError(f"WebSocket connection failed: {str(e)}")