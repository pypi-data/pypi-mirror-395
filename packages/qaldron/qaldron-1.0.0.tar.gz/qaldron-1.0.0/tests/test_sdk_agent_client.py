"""
Test Suite for SDK - Agent Client

Comprehensive tests for AgentClient functionality.
"""

import pytest
from qaldron.sdk import AgentClient
from qaldron.layer1 import MarkBluHasher


@pytest.fixture
def shared_hasher():
    """Shared hasher for all agents"""
    return MarkBluHasher(auth_key=b"TEST_SYSTEM_KEY")


class TestAgentClient:
    """Test cases for AgentClient"""
    
    def test_client_initialization(self, shared_hasher):
        """Test agent client initialization"""
        client = AgentClient("agent_a", auth_key=b"TEST_SYSTEM_KEY")
        
        assert client.agent_id == "agent_a"
        assert client.is_connected()
        assert client.enable_encryption is True
        assert client.inbox_size() == 0
    
    def test_invalid_agent_id(self):
        """Test that invalid agent_id raises error"""
        with pytest.raises(ValueError, match="agent_id must be a non-empty string"):
            AgentClient("")
        
        with pytest.raises(ValueError, match="agent_id must be a non-empty string"):
            AgentClient(None)
    
    def test_send_message(self, shared_hasher):
        """Test sending message"""
        client = AgentClient("agent_a", auth_key=b"TEST_SYSTEM_KEY")
        
        msg_id = client.send("agent_b", {"action": "test"})
        
        assert msg_id is not None
        assert isinstance(msg_id, str)
        assert len(msg_id) > 0
    
    def test_send_invalid_receiver(self, shared_hasher):
        """Test that invalid receiver_id raises error"""
        client = AgentClient("agent_a", auth_key=b"TEST_SYSTEM_KEY")
        
        with pytest.raises(ValueError, match="receiver_id must be a non-empty string"):
            client.send("", {"data": "test"})
    
    def test_send_invalid_payload(self, shared_hasher):
        """Test that invalid payload raises error"""
        client = AgentClient("agent_a", auth_key=b"TEST_SYSTEM_KEY")
        
        with pytest.raises(ValueError, match="payload must be a dictionary"):
            client.send("agent_b", "not a dict")
    
    def test_receive_envelope(self, shared_hasher):
        """Test receiving message envelope"""
        alice = AgentClient("alice", auth_key=b"TEST_SYSTEM_KEY")
         bob = AgentClient("bob", auth_key=b"TEST_SYSTEM_KEY")
        
        # Alice creates message for Bob
        envelope = alice.messenger.create_message(
            payload={"greeting": "hello"},
            receiver_id="bob"
        )
        
        # Bob receives envelope
        result = bob.receive_envelope(envelope)
        
        assert result is True
        assert bob.inbox_size() == 1
    
    def test_full_communication_workflow(self, shared_hasher):
        """Test complete send-receive workflow"""
        alice = AgentClient("alice", auth_key=b"TEST_SYSTEM_KEY")
         bob = AgentClient("bob", auth_key=b"TEST_SYSTEM_KEY")
        
        payload = {"message": "Hello Bob!", "data": [1, 2, 3]}
        
        # Alice creates and sends
        envelope = alice.messenger.create_message(payload, receiver_id="bob")
        bob.receive_envelope(envelope)
        
        # Bob receives
        messages = bob.receive()
        
        assert len(messages) == 1
        assert messages[0]['sender_id'] == "alice"
        assert messages[0]['payload'] == payload
        assert bob.inbox_size() == 0  # Removed after receive
    
    def test_filter_by_sender(self, shared_hasher):
        """Test filtering messages by sender"""
        alice = AgentClient("alice", auth_key=b"TEST_SYSTEM_KEY")
        charlie = AgentClient("charlie", auth_key=b"TEST_SYSTEM_KEY")
         bob = AgentClient("bob", auth_key=b"TEST_SYSTEM_KEY")
        
        # Send messages from both Alice and Charlie
        env1 = alice.messenger.create_message({"from": "alice"}, "bob")
        env2 = charlie.messenger.create_message({"from": "charlie"}, "bob")
        env3 = alice.messenger.create_message({"from": "alice2"}, "bob")
        
        bob.receive_envelope(env1)
        bob.receive_envelope(env2)
        bob.receive_envelope(env3)
        
        # Filter only Alice's messages
        alice_messages = bob.receive(filter_sender="alice")
        
        assert len(alice_messages) == 2
        assert all(msg['sender_id'] == "alice" for msg in alice_messages)
        assert bob.inbox_size() == 1  # Charlie's message still there
    
    def test_peek_messages(self, shared_hasher):
        """Test peeking at messages without removing them"""
        alice = AgentClient("alice", auth_key=b"TEST_SYSTEM_KEY")
         bob = AgentClient("bob", auth_key=b"TEST_SYSTEM_KEY")
        
        envelope = alice.messenger.create_message({"data": "test"}, "bob")
        bob.receive_envelope(envelope)
        
        # Peek (don't remove)
        messages1 = bob.peek_messages()
        assert len(messages1) == 1
        assert bob.inbox_size() == 1  # Still in inbox
        
        # Peek again
        messages2 = bob.peek_messages()
        assert len(messages2) == 1
        assert bob.inbox_size() == 1  # Still in inbox
    
    def test_limit_messages(self, shared_hasher):
        """Test limiting number of received messages"""
        alice = AgentClient("alice", auth_key=b"TEST_SYSTEM_KEY")
         bob = AgentClient("bob", auth_key=b"TEST_SYSTEM_KEY")
        
        # Send 5 messages
        for i in range(5):
            env = alice.messenger.create_message({"index": i}, "bob")
            bob.receive_envelope(env)
        
        # Receive only 2
        messages = bob.receive(limit=2)
        
        assert len(messages) == 2
        assert bob.inbox_size() == 3  # 3 remaining
    
    def test_clear_inbox(self, shared_hasher):
        """Test clearing inbox"""
        alice = AgentClient("alice", auth_key=b"TEST_SYSTEM_KEY")
        bob = AgentClient("bob", auth_key=b"TEST_SYSTEM_KEY")
        
        # Add messages
        for i in range(3):
            env = alice.messenger.create_message({"index": i}, "bob")
            bob.receive_envelope(env)
        
        assert bob.inbox_size() == 3
        
        bob.clear_inbox()
        
        assert bob.inbox_size() == 0
    
    def test_disconnect_reconnect(self, shared_hasher):
        """Test disconnect/reconnect functionality"""
        client = AgentClient("agent_a", auth_key=b"TEST_SYSTEM_KEY")
        
        assert client.is_connected()
        
        client.disconnect()
        assert not client.is_connected()
        
        client.reconnect()
        assert client.is_connected()
    
    def test_get_stats(self, shared_hasher):
        """Test getting client statistics"""
        client = AgentClient("agent_a", auth_key=b"TEST_SYSTEM_KEY")
        stats = client.get_stats()
        
        assert stats['agent_id'] == "agent_a"
        assert stats['connected'] is True
        assert stats['encryption_enabled'] is True
        assert 'inbox' in stats
        assert 'messenger' in stats
    
    def test_repr(self, shared_hasher):
        """Test string representation"""
        client = AgentClient("agent_a", auth_key=b"TEST_SYSTEM_KEY")
        repr_str = repr(client)
        
        assert "AgentClient" in repr_str
        assert "agent_a" in repr_str
        assert "connected=True" in repr_str
    
    def test_encryption_disabled(self):
        """Test client with encryption disabled"""
        client = AgentClient("agent_a", auth_key=b"TEST_SYSTEM_KEY", enable_encryption=False)
        
        assert client.enable_encryption is False
        
        msg_id = client.send("agent_b", {"data": "test"})
        assert msg_id is not None
    
    def test_custom_rotation_interval(self):
        """Test client with custom rotation interval"""
        client = AgentClient(
            "agent_a",
            auth_key=b"TEST_SYSTEM_KEY",
            rotation_interval=600
        )
        
        stats = client.get_stats()
        assert stats['messenger']['rotation_interval'] == 600


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
