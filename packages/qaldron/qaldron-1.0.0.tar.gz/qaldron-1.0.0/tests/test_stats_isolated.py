"""Quick test of get_stats"""
from qaldron.sdk.message_queue import MessageQueue

print("Testing get_stats...")
queue = MessageQueue(max_size=100)

queue.add({'sender_id': 'agent_a', 'data': '1'})
queue.add({'sender_id': 'agent_a', 'data': '2'})
queue.add({'sender_id': 'agent_b', 'data': '3'})

print(f"Queue size: {queue.size()}")
print("Getting stats...")
stats = queue.get_stats()
print(f"Stats: {stats}")

print("✓ Test passed")
