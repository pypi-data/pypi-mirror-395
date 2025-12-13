"""
Pydantic Models for QALDRON API

Request and response validation models.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime


class AgentRegister(BaseModel):
    """Request model for agent registration"""
    agent_id: str = Field(..., min_length=1, max_length=100, description="Unique agent identifier")
    auth_key: Optional[str] = Field(None, description="Authentication key (optional)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "agent_id": "alice",
                "auth_key": "shared_system_key"
            }
        }


class AgentInfo(BaseModel):
    """Response model for agent information"""
    agent_id: str
    connected: bool
    created_at: str
    encryption_enabled: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "agent_id": "alice",
                "connected": True,
                "created_at": "2025-12-03T19:17:00Z",
                "encryption_enabled": True
            }
        }


class MessageSend(BaseModel):
    """Request model for sending a message"""
    receiver_id: str = Field(..., min_length=1, description="Target agent ID")
    payload: Dict[str, Any] = Field(..., description="Message content")
    encrypt: Optional[bool] = Field(True, description="Enable encryption")
    
    class Config:
        json_schema_extra = {
            "example": {
                "receiver_id": "bob",
                "payload": {
                    "action": "transfer",
                    "amount": 1000,
                    "currency": "USD"
                },
                "encrypt": True
            }
        }


class MessageResponse(BaseModel):
    """Response model for message operations"""
    message_id: str
    status: str
    timestamp: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "message_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "delivered",
                "timestamp": 1701629700
            }
        }


class MessageReceived(BaseModel):
    """Model for received message"""
    sender_id: str
    receiver_id: str
    payload: Dict[str, Any]
    timestamp: int
    message_id: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "sender_id": "alice",
                "receiver_id": "bob",
                "payload": {"action": "transfer", "amount": 1000},
                "timestamp": 1701629700,
                "message_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class InboxStats(BaseModel):
    """Response model for inbox statistics"""
    agent_id: str
    message_count: int
    messages_by_sender: Dict[str, int]
    
    class Config:
        json_schema_extra = {
            "example": {
                "agent_id": "bob",
                "message_count": 5,
                "messages_by_sender": {
                    "alice": 3,
                    "charlie": 2
                }
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2025-12-03T19:17:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Agent not found",
                "detail": "Agent 'unknown_agent' is not registered"
            }
        }
