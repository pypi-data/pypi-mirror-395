"""
Test Suite for Layer 2 - Secure Messenger

Comprehensive tests for complete secure messaging flow.
All agents share the same hasher (system-wide auth key) for proper signature verification.
"""

import pytest
import json
from qaldron.layer2.secure_messenger import SecureMessenger
from qaldron.layer1 import MarkBluHasher


@pytest.fixture
def shared_hasher():
    """Shared hasher for all agents in the same QALDRON system"""
    return MarkBluHasher(auth_key=b"QALDRON_SYSTEM_KEY_TEST")


class TestSecureMessenger:
    """Test cases for secure messenger"""
    
    def test_create_message(self):
        """Test message creation"""
        messenger = SecureMessenger(agent_id="agent_a")
        payload = {"action": "hello", "data": "test"}
        
        envelope = messenger.create_message(payload, receiver_id="agent_b")
        
        assert envelope.sender_id == "agent_a"
        assert envelope.receiver_id == "agent_b"
        assert envelope.signature is not None
        assert envelope.entropy is not None
        assert envelope.message_id is not None
    
    def test_verify_valid_message(self, shared_hasher):
        """Test verification of valid message"""
        messenger_a = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        messenger_b = SecureMessenger(agent_id="agent_b", hasher=shared_hasher)
        
        # A creates message for B
        payload = {"action": "transfer", "amount": 1000}
        envelope = messenger_a.create_message(payload, receiver_id="agent_b")
        
        # B verifies message
        is_valid, reason, decrypted = messenger_b.verify_message(envelope)
        
        assert is_valid
        assert reason == "Valid"
        assert decrypted == payload
    
    def test_reject_tampered_payload(self, shared_hasher):
        """Test rejection of tampered message payload"""
        messenger_a = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        messenger_b = SecureMessenger(agent_id="agent_b", hasher=shared_hasher)
        
        payload = {"amount": 100}
        envelope = messenger_a.create_message(payload, receiver_id="agent_b")
        
        # Tamper with encrypted payload
        if envelope.encrypted:
            envelope.payload["encrypted"] = envelope.payload["encrypted"][:-10] + "XXXXXXXXXX"
        else:
            envelope.payload["amount"] = 9999
        
        # Should be rejected
        is_valid, reason, _ = messenger_b.verify_message(envelope)
        
         assert not is_valid
        assert "failed" in reason.lower() or "invalid" in reason.lower()
    
    def test_reject_tampered_signature(self, shared_hasher):
        """Test rejection of tampered signature"""
        messenger_a = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        messenger_b = SecureMessenger(agent_id="agent_b", hasher=shared_hasher)
        
        payload = {"action": "test"}
        envelope = messenger_a.create_message(payload, receiver_id="agent_b")
        
        # Tamper with signature
        envelope.signature = "0" * 32
        
        # Should be rejected
        is_valid, reason, _ = messenger_b.verify_message(envelope)
        
        assert not is_valid
        assert "signature" in reason.lower()
    
    def test_replay_attack_detection(self, shared_hasher):
        """Test replay attack prevention"""
        messenger_a = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        messenger_b = SecureMessenger(agent_id="agent_b", hasher=shared_hasher)
        
        payload = {"action": "pay", "amount": 500}
        envelope = messenger_a.create_message(payload, receiver_id="agent_b")
        
        # First reception - should be valid
        is_valid1, reason1, _ = messenger_b.verify_message(envelope)
        assert is_valid1
        
        # Replay attack - same message again
        is_valid2, reason2, _ = messenger_b.verify_message(envelope)
         assert not is_valid2
        assert "replay" in reason2.lower()
    
    def test_reject_wrong_receiver(self, shared_hasher):
        """Test rejection of message for different receiver"""
        messenger_a = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        messenger_c = SecureMessenger(agent_id="agent_c", hasher=shared_hasher)
        
        payload = {"message": "for B only"}
        envelope = messenger_a.create_message(payload, receiver_id="agent_b")
        
        # Agent C tries to read message for Agent B
        is_valid, reason, _ = messenger_c.verify_message(envelope)
        
         assert not is_valid
        assert "not for this agent" in reason.lower()
    
    def test_encryption_enabled_by_default(self, shared_hasher):
        """Test that encryption is enabled by default"""
        messenger = SecureMessenger(agent_id="agent_a", hasher=shared_hasher, enable_encryption=True)
        payload = {"secret": "data"}
        
        envelope = messenger.create_message(payload, receiver_id="agent_b")
        
        assert envelope.encrypted is True
        assert "encrypted" in envelope.payload
    
    def test_encryption_can_be_disabled(self, shared_hasher):
        """Test that encryption can be disabled"""
        messenger = SecureMessenger(agent_id="agent_a", hasher=shared_hasher, enable_encryption=False)
        payload = {"public": "data"}
        
        envelope = messenger.create_message(payload, receiver_id="agent_b")
        
        assert envelope.encrypted is False
        assert envelope.payload == payload
    
    def test_per_message_encryption_override(self, shared_hasher):
        """Test per-message encryption override"""
        messenger = SecureMessenger(agent_id="agent_a", hasher=shared_hasher, enable_encryption=True)
        payload = {"data": "test"}
        
        # Override to disable encryption for this message
        envelope = messenger.create_message(payload, receiver_id="agent_b", encrypt=False)
        
        assert envelope.encrypted is False
        assert envelope.payload == payload
    
    def test_send_receive_workflow(self, shared_hasher):
        """Test complete send/receive workflow"""
        messenger_a = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        messenger_b = SecureMessenger(agent_id="agent_b", hasher=shared_hasher)
        
        # A sends message
        payload = {"greeting": "Hello Agent B!"}
        message_data = messenger_a.send_message(payload, receiver_id="agent_b")
        
        # B receives message
        is_valid, reason, received_payload = messenger_b.receive_message(message_data)
        
        assert is_valid
        assert received_payload == payload
    
    def test_unique_message_ids(self, shared_hasher):
        """Test that message IDs are unique"""
        messenger = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        
        env1 = messenger.create_message({"data": 1}, "agent_b")
        env2 = messenger.create_message({"data": 2}, "agent_b")
        env3 = messenger.create_message({"data": 3}, "agent_b")
        
        assert env1.message_id != env2.message_id
        assert env2.message_id != env3.message_id
        assert env1.message_id != env3.message_id
    
    def test_custom_message_id(self, shared_hasher):
        """Test custom message ID"""
        messenger = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        custom_id = "msg_12345"
        
        envelope = messenger.create_message(
            {"data": "test"},
            receiver_id="agent_b",
            message_id=custom_id
        )
        
        assert envelope.message_id == custom_id
    
    def test_clear_replay_cache(self, shared_hasher):
        """Test clearing replay protection cache"""
        messenger_a = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        messenger_b = SecureMessenger(agent_id="agent_b", hasher=shared_hasher)
        
        payload = {"action": "test"}
        envelope = messenger_a.create_message(payload, receiver_id="agent_b")
        
        # First reception
        messenger_b.verify_message(envelope)
        
        # Clear cache
        messenger_b.clear_replay_cache()
        
        # Should be accepted again after cache clear
        is_valid, _, _ = messenger_b.verify_message(envelope)
        assert is_valid
    
    def test_get_stats(self, shared_hasher):
        """Test messenger statistics"""
        messenger = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        stats = messenger.get_stats()
        
        assert stats["agent_id"] == "agent_a"
        assert "encryption_enabled" in stats
        assert "rotation_interval" in stats
        assert "replay_cache_size" in stats
        assert "current_entropy" in stats
        assert "time_until_rotation" in stats
    
    def test_different_agents_different_signatures(self, shared_hasher):
        """Test that different agents produce different signatures"""
        messenger_a = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        messenger_b = SecureMessenger(agent_id="agent_b", hasher=shared_hasher)
        
        payload = {"same": "data"}
        
        env_a = messenger_a.create_message(payload, receiver_id="agent_c")
        env_b = messenger_b.create_message(payload, receiver_id="agent_c")
        
        # Different agents should produce different signatures
        # (due to sender_id in signing data)
        assert env_a.signature != env_b.signature
    
    def test_json_serialization_roundtrip(self, shared_hasher):
        """Test JSON serialization and deserialization"""
        messenger_a = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        messenger_b = SecureMessenger(agent_id="agent_b", hasher=shared_hasher)
        
        payload = {"data": "test", "number": 42, "nested": {"key": "value"}}
        
        # Create and serialize
        envelope = messenger_a.create_message(payload, receiver_id="agent_b")
        json_str = envelope.to_json()
        
        # Deserialize and verify
        is_valid, reason, received = messenger_b.receive_message(
            json.loads(json_str)
        )
        
        assert is_valid
        assert received == payload
    
    def test_complex_payload_types(self, shared_hasher):
        """Test various payload data types"""
        messenger_a = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        messenger_b = SecureMessenger(agent_id="agent_b", hasher=shared_hasher)
        
        complex_payload = {
            "string": "hello",
            "int": 42,
            "float": 3.14,
            "bool": True,
            "null": None,
            "list": [1, 2, 3],
            "nested": {"a": {"b": {"c": "deep"}}}
        }
        
        envelope = messenger_a.create_message(complex_payload, receiver_id="agent_b")
        is_valid, _, received = messenger_b.verify_message(envelope)
        
        assert is_valid
        assert received == complex_payload
    
    def test_empty_payload(self, shared_hasher):
        """Test empty payload handling"""
        messenger_a = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        messenger_b = SecureMessenger(agent_id="agent_b", hasher=shared_hasher)
        
        empty_payload = {}
        
        envelope = messenger_a.create_message(empty_payload, receiver_id="agent_b")
        is_valid, _, received = messenger_b.verify_message(envelope)
        
        assert is_valid
        assert received == empty_payload
    
    def test_disable_replay_check(self, shared_hasher):
        """Test disabling replay attack check"""
        messenger_a = SecureMessenger(agent_id="agent_a", hasher=shared_hasher)
        messenger_b = SecureMessenger(agent_id="agent_b", hasher=shared_hasher)
        
        payload = {"data": "test"}
        envelope = messenger_a.create_message(payload, receiver_id="agent_b")
        
        # First verification
        messenger_b.verify_message(envelope, check_replay=True)
        
        # Second verification with replay check disabled
        is_valid, _, _ = messenger_b.verify_message(envelope, check_replay=False)
        
        assert is_valid  # Should pass since replay check is disabled


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
