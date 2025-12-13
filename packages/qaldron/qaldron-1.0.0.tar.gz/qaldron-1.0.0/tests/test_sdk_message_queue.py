"""
Test Suite for SDK - Message Queue

Tests for message queue operations.
"""

import pytest
import threading
import time
from qaldron.sdk.message_queue import MessageQueue


class TestMessageQueue:
    """Test cases for message queue"""
    
    def test_queue_initialization(self):
        """Test queue initialization"""
        queue = MessageQueue(max_size=100)
        
        assert queue.size() == 0
        assert queue.is_empty()
        assert not queue.is_full()
    
    def test_add_message(self):
        """Test adding messages to queue"""
        queue = MessageQueue()
        
        msg = {'sender_id': 'agent_a', 'payload': {'data': 'test'}}
        result = queue.add(msg)
        
        assert result is True
        assert queue.size() == 1
        assert not queue.is_empty()
    
    def test_get_message(self):
        """Test retrieving messages from queue"""
        queue = MessageQueue()
        
        msg1 = {'sender_id': 'agent_a', 'payload': {'data': '1'}}
        msg2 = {'sender_id': 'agent_b', 'payload': {'data': '2'}}
        
        queue.add(msg1)
        queue.add(msg2)
        
        messages = queue.get()
        
        assert len(messages) == 2
        assert messages[0]['payload']['data'] == '1'
        assert messages[1]['payload']['data'] == '2'
        assert queue.is_empty()
    
    def test_fifo_ordering(self):
        """Test FIFO (first in, first out) ordering"""
        queue = MessageQueue()
        
        for i in range(5):
            queue.add({'sender_id': f'agent_{i}', 'order': i})
        
        messages = queue.get()
        
        for i, msg in enumerate(messages):
            assert msg['order'] == i
    
    def test_filter_by_sender(self):
        """Test filtering messages by sender"""
        queue = MessageQueue()
        
        queue.add({'sender_id': 'agent_a', 'data': '1'})
        queue.add({'sender_id': 'agent_b', 'data': '2'})
        queue.add({'sender_id': 'agent_a', 'data': '3'})
        
        messages = queue.get(filter_sender='agent_a')
        
        assert len(messages) == 2
        assert all(msg['sender_id'] == 'agent_a' for msg in messages)
        
        # agent_b message should still be in queue
        assert queue.size() == 1
    
    def test_peek_without_removing(self):
        """Test peeking at messages without removing them"""
        queue = MessageQueue()
        
        queue.add({'sender_id': 'agent_a', 'data': 'test'})
        
        # Peek
        messages = queue.peek()
        assert len(messages) == 1
        assert queue.size() == 1  # Still in queue
        
        # Peek again
        messages2 = queue.peek()
        assert len(messages2) == 1
        assert queue.size() == 1  # Still in queue
    
    def test_limit_results(self):
        """Test limiting number of returned messages"""
        queue = MessageQueue()
        
        for i in range(10):
            queue.add({'sender_id': 'agent_a', 'index': i})
        
        messages = queue.get(limit=3)
        
        assert len(messages) == 3
        assert queue.size() == 7  # 3 removed, 7 remaining
    
    def test_max_size_limit(self):
        """Test queue size limit"""
        queue = MessageQueue(max_size=5)
        
        # Add more than max_size
        for i in range(10):
            queue.add({'index': i})
        
        # Queue should only contain last 5 (oldest dropped)
        assert queue.size() == 5
        assert queue.is_full()
        
        messages = queue.get()
        # Should have indices 5-9 (0-4 were dropped)
        assert messages[0]['index'] == 5
    
    def test_clear_queue(self):
        """Test clearing queue"""
        queue = MessageQueue()
        
        for i in range(5):
            queue.add({'data': i})
        
        assert queue.size() == 5
        
        queue.clear()
        
        assert queue.size() == 0
        assert queue.is_empty()
    
    def test_get_stats(self):
        """Test queue statistics"""
        queue = MessageQueue(max_size=100)
        
        queue.add({'sender_id': 'agent_a', 'data': '1'})
        queue.add({'sender_id': 'agent_a', 'data': '2'})
        queue.add({'sender_id': 'agent_b', 'data': '3'})
        
        stats = queue.get_stats()
        
        assert stats['size'] == 3
        assert stats['max_size'] == 100
        assert not stats['is_full']
        assert not stats['is_empty']
        assert stats['messages_by_sender']['agent_a'] == 2
        assert stats['messages_by_sender']['agent_b'] == 1
    
    def test_thread_safety(self):
        """Test thread-safe operations"""
        queue = MessageQueue()
        errors = []
        
        def add_messages(start, count):
            try:
                for i in range(start, start + count):
                    queue.add({'sender_id': 'thread', 'index': i})
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads adding messages
        threads = []
        for i in range(5):
            t = threading.Thread(target=add_messages, args=(i * 10, 10))
            threads.append(t)
            t.start()
        
        # Wait for all threads
        for t in threads:
            t.join()
        
        # No errors should occur
        assert len(errors) == 0
        # Should have all 50 messages
        assert queue.size() == 50
    
    def test_empty_queue_get(self):
        """Test getting from empty queue"""
        queue = MessageQueue()
        
        messages = queue.get()
        
        assert len(messages) == 0
        assert isinstance(messages, list)
    
    def test_queued_timestamp_added(self):
        """Test that queued_at timestamp is added automatically"""
        queue = MessageQueue()
        
        msg = {'sender_id': 'agent_a', 'data': 'test'}
        queue.add(msg)
        
        messages = queue.get()
        
        assert 'queued_at' in messages[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
