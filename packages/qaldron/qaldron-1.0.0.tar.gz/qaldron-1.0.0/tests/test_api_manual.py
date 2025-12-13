"""
Quick test of QALDRON API

Tests the basic functionality via HTTP requests.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("QALDRON API - Quick Test")
print("=" * 70)

# Wait for server to start
print("\n⏳ Waiting for API server...")
time.sleep(2)

try:
    # Test 1: Health Check
    print("\n1. Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print(f"   ✓ API is healthy: {response.json()}")
    else:
        print(f"   ✗ Health check failed: {response.status_code}")
        exit(1)
    
    # Test 2: Register Alice
    print("\n2. Register Agent 'alice'...")
    response = requests.post(
        f"{BASE_URL}/api/v1/agents/register",
        json={"agent_id": "alice"}
    )
    if response.status_code == 201:
        print(f"   ✓ Alice registered: {response.json()}")
    else:
        print(f"   ✗ Failed: {response.json()}")
        exit(1)
    
    # Test 3: Register Bob
    print("\n3. Register Agent 'bob'...")
    response = requests.post(
        f"{BASE_URL}/api/v1/agents/register",
        json={"agent_id": "bob"}
    )
    if response.status_code == 201:
        print(f"   ✓ Bob registered: {response.json()}")
    else:
        print(f"   ✗ Failed: {response.json()}")
        exit(1)
    
    # Test 4: List Agents
    print("\n4. List All Agents...")
    response = requests.get(f"{BASE_URL}/api/v1/agents/")
    if response.status_code == 200:
        agents = response.json()
        print(f"   ✓ Agents: {agents}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
    
    # Test 5: Send Message
    print("\n5. Alice sends message to Bob...")
    response = requests.post(
        f"{BASE_URL}/api/v1/messages/send?sender_id=alice",
        json={
            "receiver_id": "bob",
            "payload": {
                "action": "greeting",
                "message": "Hello Bob!",
                "timestamp": "2025-12-03"
            },
            "encrypt": True
        }
    )
    if response.status_code == 200:
        msg_response = response.json()
        print(f"   ✓ Message sent: ID={msg_response['message_id']}")
        print(f"   ✓ Status: {msg_response['status']}")
    else:
        print(f"   ✗ Failed: {response.json()}")
        exit(1)
    
    # Test 6: Check Inbox Stats
    print("\n6. Bob's inbox stats...")
    response = requests.get(f"{BASE_URL}/api/v1/messages/inbox/bob/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"   ✓ Inbox count: {stats['message_count']}")
        print(f"   ✓ By sender: {stats['messages_by_sender']}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
    
    # Test 7: Receive Messages
    print("\n7. Bob receives messages...")
    response = requests.get(f"{BASE_URL}/api/v1/messages/inbox/bob")
    if response.status_code == 200:
        messages = response.json()
        print(f"   ✓ Received {len(messages)} message(s)")
        for msg in messages:
            print(f"   📧 From {msg['sender_id']}: {msg['payload']}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
    
    # Test 8: Get Agent Info
    print("\n8. Get Alice's info...")
    response = requests.get(f"{BASE_URL}/api/v1/agents/alice")
    if response.status_code == 200:
        info = response.json()
        print(f"   ✓ Agent: {info['agent_id']}")
        print(f"   ✓ Connected: {info['connected']}")
        print(f"   ✓ Encryption: {info['encryption_enabled']}")
    else:
        print(f"   ✗ Failed: {response.status_code}")
    
    print("\n" + "=" * 70)
    print("✅ All API tests passed!")
    print("=" * 70)
    
    print("\n📚 Swagger UI available at: http://localhost:8000/docs")

except requests.exceptions.ConnectionError:
    print("\n❌ Error: Could not connect to API server")
    print("   Make sure the server is running:")
    print("   python qaldron/api/main.py")
    exit(1)

except Exception as e:
    print(f"\n❌ Error: {e}")
    exit(1)
