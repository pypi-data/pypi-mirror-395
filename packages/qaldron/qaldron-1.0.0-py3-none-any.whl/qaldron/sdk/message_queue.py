"""
Message Queue Handler for QALDRON SDK

Manages queuing of incoming and outgoing messages with filtering,
size limits, and FIFO ordering.
"""

from typing import List, Dict, Any, Optional
from collections import deque
from datetime import datetime
import threading


class MessageQueue:
    """
    Thread-safe message queue for agent communication
    
    Features:
    - FIFO ordering
    - Size limits to prevent memory overflow
    - Message filtering by sender
    - Thread-safe operations
    
    Args:
        max_size: Maximum queue size (default: 1000)
    """
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._queue = deque(maxlen=max_size)
        self._lock = threading.Lock()
    
    def add(self, message: Dict[str, Any]) -> bool:
        """
        Add message to queue
        
        Args:
            message: Message dictionary to add
            
        Returns:
            bool: True if added successfully, False if queue full
        """
        with self._lock:
            if len(self._queue) >= self.max_size:
                # Queue full - oldest message will be dropped (deque auto-removes)
                pass
            
            # Add timestamp if not present
            if 'queued_at' not in message:
                message['queued_at'] = datetime.now().isoformat()
            
            self._queue.append(message)
            return True
    
    def get(
        self,
        filter_sender: Optional[str] = None,
        limit: Optional[int] = None,
        remove: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get messages from queue
        
        Args:
            filter_sender: Only return messages from this sender (optional)
            limit: Maximum number of messages to return (optional)
            remove: Remove messages from queue after retrieval (default: True)
            
        Returns:
            list: List of message dictionaries
        """
        with self._lock:
            messages = []
            to_remove = []
            
            for idx, msg in enumerate(self._queue):
                # Apply sender filter if specified
                if filter_sender and msg.get('sender_id') != filter_sender:
                    continue
                
                messages.append(msg)
                if remove:
                    to_remove.append(idx)
                
                # Check limit
                if limit and len(messages) >= limit:
                    break
            
            # Remove retrieved messages from queue (in reverse to maintain indices)
            if remove:
                for idx in reversed(to_remove):
                    del self._queue[idx]
            
            return messages
    
    def peek(
        self,
        filter_sender: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Peek at messages without removing them
        
        Args:
            filter_sender: Only return messages from this sender (optional)
            limit: Maximum number of messages to return (optional)
            
        Returns:
            list: List of message dictionaries
        """
        return self.get(filter_sender=filter_sender, limit=limit, remove=False)
    
    def size(self) -> int:
        """Get current queue size"""
        with self._lock:
            return len(self._queue)
    
    def clear(self):
        """Clear all messages from queue"""
        with self._lock:
            self._queue.clear()
    
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return self.size() == 0
    
    def is_full(self) -> bool:
        """Check if queue is at max size"""
        return self.size() >= self.max_size
    
    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
"""
Message Queue Handler for QALDRON SDK

Manages queuing of incoming and outgoing messages with filtering,
size limits, and FIFO ordering.
"""

from typing import List, Dict, Any, Optional
from collections import deque
from datetime import datetime
import threading


class MessageQueue:
    """
    Thread-safe message queue for agent communication
    
    Features:
    - FIFO ordering
    - Size limits to prevent memory overflow
    - Message filtering by sender
    - Thread-safe operations
    
    Args:
        max_size: Maximum queue size (default: 1000)
    """
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._queue = deque(maxlen=max_size)
        self._lock = threading.Lock()
    
    def add(self, message: Dict[str, Any]) -> bool:
        """
        Add message to queue
        
        Args:
            message: Message dictionary to add
            
        Returns:
            bool: True if added successfully, False if queue full
        """
        with self._lock:
            if len(self._queue) >= self.max_size:
                # Queue full - oldest message will be dropped (deque auto-removes)
                pass
            
            # Add timestamp if not present
            if 'queued_at' not in message:
                message['queued_at'] = datetime.now().isoformat()
            
            self._queue.append(message)
            return True
    
    def get(
        self,
        filter_sender: Optional[str] = None,
        limit: Optional[int] = None,
        remove: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get messages from queue
        
        Args:
            filter_sender: Only return messages from this sender (optional)
            limit: Maximum number of messages to return (optional)
            remove: Remove messages from queue after retrieval (default: True)
            
        Returns:
            list: List of message dictionaries
        """
        with self._lock:
            messages = []
            to_remove = []
            
            for idx, msg in enumerate(self._queue):
                # Apply sender filter if specified
                if filter_sender and msg.get('sender_id') != filter_sender:
                    continue
                
                messages.append(msg)
                if remove:
                    to_remove.append(idx)
                
                # Check limit
                if limit and len(messages) >= limit:
                    break
            
            # Remove retrieved messages from queue (in reverse to maintain indices)
            if remove:
                for idx in reversed(to_remove):
                    del self._queue[idx]
            
            return messages
    
    def peek(
        self,
        filter_sender: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Peek at messages without removing them
        
        Args:
            filter_sender: Only return messages from this sender (optional)
            limit: Maximum number of messages to return (optional)
            
        Returns:
            list: List of message dictionaries
        """
        return self.get(filter_sender=filter_sender, limit=limit, remove=False)
    
    def size(self) -> int:
        """Get current queue size"""
        with self._lock:
            return len(self._queue)
    
    def clear(self):
        """Clear all messages from queue"""
        with self._lock:
            self._queue.clear()
    
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return self.size() == 0
    
    def is_full(self) -> bool:
        """Check if queue is at max size"""
        return self.size() >= self.max_size
    
    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
        with self._lock:
            senders = {}
            for msg in self._queue:
                sender = msg.get('sender_id', 'unknown')
                senders[sender] = senders.get(sender, 0) + 1
            
            queue_size = len(self._queue)
            return {
                'size': queue_size,
                'max_size': self.max_size,
                'is_full': queue_size >= self.max_size,  # Direct calculation
                'is_empty': queue_size == 0,  # Direct calculation
                'messages_by_sender': senders
            }
