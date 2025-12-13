"""
Message Endpoints

Handles message sending, receiving, and inbox management.
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from qaldron.api.models import MessageSend, MessageResponse, MessageReceived, InboxStats
from qaldron.api.registry import registry
import time

router = APIRouter()


@router.post("/send", response_model=MessageResponse)
async def send_message(
    sender_id: str = Query(..., description="Sender agent ID"),
    message: MessageSend = ...
):
    """
    Send a message from one agent to another
    
    - **sender_id**: ID of the sending agent
    - **receiver_id**: ID of the receiving agent
    - **payload**: Message content (JSON object)
    - **encrypt**: Whether to encrypt the message (default: true)
    """
    # Verify sender exists
    if not registry.exists(sender_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sender agent '{sender_id}' not found"
        )
    
    # Verify receiver exists
    if not registry.exists(message.receiver_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receiver agent '{message.receiver_id}' not found"
        )
    
    try:
        # Get sender client
        sender = registry.get(sender_id)
        receiver = registry.get(message.receiver_id)
        
        # Create message envelope
        envelope = sender.messenger.create_message(
            payload=message.payload,
            receiver_id=message.receiver_id,
            encrypt=message.encrypt
        )
        
        # Deliver to receiver's inbox
        receiver.receive_envelope(envelope)
        
        return MessageResponse(
            message_id=envelope.message_id,
            status="delivered",
            timestamp=envelope.timestamp
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}"
        )


@router.get("/inbox/{agent_id}", response_model=List[MessageReceived])
async def get_inbox(
    agent_id: str,
    filter_sender: str = Query(None, description="Filter by sender ID"),
    limit: int = Query(None, ge=1, le=100, description="Max messages to return")
):
    """
    Retrieve messages from agent's inbox
    
    - **agent_id**: ID of the agent
    - **filter_sender**: Optional sender ID to filter by
    - **limit**: Maximum number of messages to return
    
    Messages are removed from inbox after retrieval.
    """
    if not registry.exists(agent_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found"
        )
    
    try:
        client = registry.get(agent_id)
        messages = client.receive(filter_sender=filter_sender, limit=limit)
        
        return [
            MessageReceived(
                sender_id=msg["sender_id"],
                receiver_id=msg["receiver_id"],
                payload=msg["payload"],
                timestamp=msg["timestamp"],
                message_id=msg["message_id"]
            )
            for msg in messages
        ]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve messages: {str(e)}"
        )


@router.get("/inbox/{agent_id}/peek", response_model=List[MessageReceived])
async def peek_inbox(
    agent_id: str,
    filter_sender: str = Query(None, description="Filter by sender ID"),
    limit: int = Query(None, ge=1, le=100, description="Max messages to return")
):
    """
    Peek at inbox messages without removing them
    
    - **agent_id**: ID of the agent
    - **filter_sender**: Optional sender ID to filter by
    - **limit**: Maximum number of messages to return
    
    Messages remain in inbox after peeking.
    """
    if not registry.exists(agent_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found"
        )
    
    try:
        client = registry.get(agent_id)
        messages = client.peek_messages(filter_sender=filter_sender, limit=limit)
        
        return [
            MessageReceived(
                sender_id=msg["sender_id"],
                receiver_id=msg["receiver_id"],
                payload=msg["payload"],
                timestamp=msg["timestamp"],
                message_id=msg["message_id"]
            )
            for msg in messages
        ]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to peek inbox: {str(e)}"
        )


@router.get("/inbox/{agent_id}/stats", response_model=InboxStats)
async def get_inbox_stats(agent_id: str):
    """
    Get inbox statistics
    
    Returns message count and breakdown by sender.
    """
    if not registry.exists(agent_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found"
        )
    
    try:
        client = registry.get(agent_id)
        inbox_stats = client.inbox.get_stats()
        
        return InboxStats(
            agent_id=agent_id,
            message_count=inbox_stats["size"],
            messages_by_sender=inbox_stats["messages_by_sender"]
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get inbox stats: {str(e)}"
        )


@router.delete("/inbox/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_inbox(agent_id: str):
    """
    Clear all messages from inbox
    
    Removes all messages from the agent's inbox.
    """
    if not registry.exists(agent_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found"
        )
    
    try:
        client = registry.get(agent_id)
        client.clear_inbox()
        return None
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear inbox: {str(e)}"
        )
