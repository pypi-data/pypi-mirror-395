"""
Agent Client - Simple SDK for QALDRON

Provides easy-to-use interface for secure agent communication.
Handles automatic signing, encryption, and message verification.
Requires API key from QALDRON control server.
"""

from typing import Dict, Any, Optional, List
import os
import requests
from qaldron.layer1 import MarkBluHasher
from qaldron.layer2.secure_messenger import SecureMessenger
from qaldron.layer2.message_envelope import MessageEnvelope
from qaldron.sdk.message_queue import MessageQueue


class AgentClient:
    """
    Simple client for secure agent communication
    
    **IMPORTANT:** Requires valid API key from QALDRON server.
    Get your API key at: https://qaldron.onrender.com/client
    
    Provides high-level API that automatically handles:
    - API key validation with control server
    - Quantum hash signatures
    - Encryption/decryption
    - Entropy stamps
    - Message verification
    - Replay attack prevention
    
    Example:
        ```python
        # Get API key from https://qaldron.onrender.com/client
        client = AgentClient(
            agent_id="my_agent",
            api_key="sk-free-YOUR_API_KEY_HERE"
        )
        client.send("other_agent", {"action": "hello"})
        messages = client.receive()
        ```
    
    Args:
        agent_id: Unique identifier for this agent
        api_key: Your API key from QALDRON (required)
        server_url: QALDRON server URL (default: production server)
        enable_encryption: Enable payload encryption (default: True)
        rotation_interval: Entropy rotation interval in seconds (default: 300)
        max_queue_size: Maximum message queue size (default: 1000)
    """
    
    # Production server URL
    DEFAULT_SERVER = "https://qaldron.onrender.com"
    
    def __init__(
        self,
        agent_id: str,
        api_key: str,
        server_url: Optional[str] = None,
        enable_encryption: bool = True,
        rotation_interval: int = 300,
        max_queue_size: int = 1000
    ):
        if not agent_id or not isinstance(agent_id, str):
            raise ValueError("agent_id must be a non-empty string")
        
        if not api_key or not isinstance(api_key, str):
            raise ValueError(
                "api_key is required. Get one at: https://qaldron.onrender.com/client"
            )
        
        if not api_key.startswith("sk-"):
            raise ValueError(
                "Invalid API key format. Key must start with 'sk-'\n"
                "Get your API key at: https://qaldron.onrender.com/client"
            )
        
        self.agent_id = agent_id
        self.api_key = api_key
        self.server_url = server_url or os.getenv("QALDRON_SERVER", self.DEFAULT_SERVER)
        self.enable_encryption = enable_encryption
        
        # Step 1: Validate API key with server
        print(f"🔐 Validating API key with QALDRON server...")
        self.client_info = self._validate_api_key()
        print(f"✅ API key validated! Tier: {self.client_info.get('tier', 'unknown')}")
        
        # Step 2: Get system auth key from server
        print(f"🔑 Fetching authentication key...")
        auth_key = self._get_auth_key()
        print(f"✅ Authentication key received")
        
        # Step 3: Initialize messenger with server-provided auth key
        self.hasher = MarkBluHasher(auth_key=auth_key)
        self.messenger = SecureMessenger(
            agent_id=agent_id,
            hasher=self.hasher,
            rotation_interval=rotation_interval,
            enable_encryption=enable_encryption
        )
        
        # Initialize message queue for incoming messages
        self.inbox = MessageQueue(max_size=max_queue_size)
        
        # Track connection state
        self._connected = True
        print(f"🚀 Agent '{agent_id}' initialized successfully!")
    
    def _validate_api_key(self) -> dict:
        """
        Validate API key with QALDRON control server
        
        Returns:
            dict: Client information from server
            
        Raises:
            Exception: If API key is invalid or server is unreachable
        """
        try:
            response = requests.post(
                f"{self.server_url}/api/v1/auth/validate",
                json={
                    "api_key": self.api_key,
                    "agent_id": self.agent_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                error = response.json()
                raise Exception(
                    f"❌ API Key Validation Failed: {error.get('detail', 'Invalid key')}\n\n"
                    f"Possible reasons:\n"
                    f"  • API key is invalid or expired\n"
                    f"  • API key has been suspended\n"
                    f"  • Usage limit exceeded\n\n"
                    f"Get a new API key at: {self.server_url}/client"
                )
            elif response.status_code == 429:
                raise Exception(
                    f"❌ Usage Limit Exceeded\n\n"
                    f"Your API key has reached its monthly usage limit.\n"
                    f"Upgrade your plan at: {self.server_url}/client"
                )
            else:
                raise Exception(f"❌ Server error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            raise Exception(
                f"❌ Cannot connect to QALDRON servers\n\n"
                f"Server: {self.server_url}\n"
                f"Please check:\n"
                f"  • Your internet connection\n"
                f"  • QALDRON server status\n"
                f"  • server_url parameter is correct"
            )
        except requests.exceptions.Timeout:
            raise Exception(
                f"❌ QALDRON server timeout\n\n"
                f"The server took too long to respond.\n"
                f"Please try again in a few seconds."
            )
    
    def _get_auth_key(self) -> bytes:
        """
        Get system authentication key from server
        
        Returns:
            bytes: System-wide auth key for quantum hashing
            
        Raises:
            Exception: If unable to retrieve auth key
        """
        try:
            response = requests.get(
                f"{self.server_url}/api/v1/auth/system-key",
                params={"api_key": self.api_key},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["auth_key"].encode()
            else:
                raise Exception(f"Failed to get auth key: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to retrieve system auth key: {str(e)}")

    
    def send(
        self,
        receiver_id: str,
        payload: Dict[str, Any],
        message_id: Optional[str] = None,
        encrypt: Optional[bool] = None
    ) -> str:
        """
        Send a secure message to another agent
        
        Automatically handles signing and encryption.
        
        Args:
            receiver_id: Target agent ID
            payload: Message content (dictionary)
            message_id: Optional custom message ID
            encrypt: Override encryption setting (optional)
            
        Returns:
            str: Message ID of sent message
            
        Raises:
            ValueError: If receiver_id or payload is invalid
            
        Example:
            ```python
            msg_id = client.send("agent_b", {"action": "transfer", "amount": 100})
            print(f"Sent message {msg_id}")
            ```
        """
        if not receiver_id or not isinstance(receiver_id, str):
            raise ValueError("receiver_id must be a non-empty string")
        
        if not isinstance(payload, dict):
            raise ValueError("payload must be a dictionary")
        
        # Create secure message envelope
        envelope = self.messenger.create_message(
            payload=payload,
            receiver_id=receiver_id,
            message_id=message_id,
            encrypt=encrypt
        )
        
        # In a real system, this would be sent over network
        # For now, just return the message ID
        return envelope.message_id
    
    def receive(
        self,
        filter_sender: Optional[str] = None,
        limit: Optional[int] = None,
        remove_from_queue: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Receive and verify messages from inbox
        
        Automatically verifies signatures and decrypts payloads.
        
        Args:
            filter_sender: Only return messages from this sender (optional)
            limit: Maximum number of messages to return (optional)
            remove_from_queue: Remove messages from queue after retrieval (default: True)
            
        Returns:
            list: List of verified message dictionaries with keys:
                - sender_id: ID of sender
                - receiver_id: ID of receiver (this agent)
                - payload: Decrypted message content
                - timestamp: Message timestamp
                - message_id: Unique message ID
                
        Example:
            ```python
            messages = client.receive()
            for msg in messages:
                print(f"From {msg['sender_id']}: {msg['payload']}")
            ```
        """
        # Get messages from inbox
        if remove_from_queue:
            raw_messages = self.inbox.get(filter_sender=filter_sender, limit=limit)
        else:
            raw_messages = self.inbox.peek(filter_sender=filter_sender, limit=limit)
        
        verified_messages = []
        
        for raw_msg in raw_messages:
            # Extract envelope from raw message
            envelope = raw_msg.get('envelope')
            if not envelope:
                continue
            
            # Verify and decrypt
            is_valid, reason, payload = self.messenger.verify_message(envelope)
            
            if is_valid:
                verified_messages.append({
                    'sender_id': envelope.sender_id,
                    'receiver_id': envelope.receiver_id,
                    'payload': payload,
                    'timestamp': envelope.timestamp,
                    'message_id': envelope.message_id
                })
        
        return verified_messages
    
    def receive_envelope(self, envelope: MessageEnvelope) -> bool:
        """
        Receive a message envelope into the inbox
        
        This method is called when a message arrives (e.g., from network).
        
        Args:
            envelope: MessageEnvelope to process
            
        Returns:
            bool: True if message was added to inbox
        """
        # Add to inbox for later processing
        self.inbox.add({
            'envelope': envelope,
            'sender_id': envelope.sender_id,
            'received_at': envelope.timestamp
        })
        return True
    
    def peek_messages(
        self,
        filter_sender: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Peek at messages without removing them from inbox
        
        Args:
            filter_sender: Only return messages from this sender (optional)
            limit: Maximum number of messages to return (optional)
            
        Returns:
            list: List of messages (same format as receive())
        """
        return self.receive(
            filter_sender=filter_sender,
            limit=limit,
            remove_from_queue=False
        )
    
    def clear_inbox(self):
        """Clear all messages from inbox"""
        self.inbox.clear()
    
    def inbox_size(self) -> int:
        """Get number of messages in inbox"""
        return self.inbox.size()
    
    def is_connected(self) -> bool:
        """Check if agent is connected"""
        return self._connected
    
    def disconnect(self):
        """Disconnect agent"""
        self._connected = False
    
    def reconnect(self):
        """Reconnect agent"""
        self._connected = True
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get client statistics
        
        Returns:
            dict: Statistics including agent_id, inbox size, messenger stats, etc.
        """
        messenger_stats = self.messenger.get_stats()
        inbox_stats = self.inbox.get_stats()
        
        return {
            'agent_id': self.agent_id,
            'connected': self._connected,
            'encryption_enabled': self.enable_encryption,
            'inbox': inbox_stats,
            'messenger': messenger_stats
        }
    
    def __repr__(self) -> str:
        return f"AgentClient(agent_id='{self.agent_id}', connected={self._connected})"
