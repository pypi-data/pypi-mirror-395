"""
Agent Management Endpoints

Handles agent registration, information, and lifecycle.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from qaldron.api.models import AgentRegister, AgentInfo, ErrorResponse
from qaldron.api.registry import registry
from qaldron.sdk import AgentClient

router = APIRouter()


@router.post("/register", response_model=AgentInfo, status_code=status.HTTP_201_CREATED)
async def register_agent(agent_data: AgentRegister):
    """
    Register a new agent
    
    Creates a new AgentClient and registers it in the system.
    
    - **agent_id**: Unique identifier for the agent
    - **auth_key**: Optional authentication key (uses default if not provided)
    """
    # Check if agent already exists
    if registry.exists(agent_data.agent_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Agent '{agent_data.agent_id}' is already registered"
        )
    
    try:
        # Create agent client
        if agent_data.auth_key:
            client = AgentClient(
                agent_id=agent_data.agent_id,
                auth_key=agent_data.auth_key.encode()
            )
        else:
            client = AgentClient(agent_id=agent_data.agent_id)
        
        # Register in registry
        metadata = registry.register(agent_data.agent_id, client)
        
        return AgentInfo(
            agent_id=agent_data.agent_id,
            connected=metadata["connected"],
            created_at=metadata["created_at"],
            encryption_enabled=metadata["encryption_enabled"]
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register agent: {str(e)}"
        )


@router.get("/{agent_id}", response_model=AgentInfo)
async def get_agent(agent_id: str):
    """
    Get agent information
    
    Returns metadata about a registered agent.
    """
    if not registry.exists(agent_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found"
        )
    
    client = registry.get(agent_id)
    metadata = registry.get_metadata(agent_id)
    
    return AgentInfo(
        agent_id=agent_id,
        connected=client.is_connected(),
        created_at=metadata["created_at"],
        encryption_enabled=client.enable_encryption
    )


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deregister_agent(agent_id: str):
    """
    Deregister an agent
    
    Removes the agent from the system.
    """
    if not registry.deregister(agent_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found"
        )
    
    return None


@router.get("/{agent_id}/stats")
async def get_agent_stats(agent_id: str):
    """
    Get agent statistics
    
    Returns detailed statistics about the agent.
    """
    if not registry.exists(agent_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found"
        )
    
    client = registry.get(agent_id)
    stats = client.get_stats()
    
    return stats


@router.get("/", response_model=List[str])
async def list_agents():
    """
    List all registered agents
    
    Returns a list of all agent IDs currently registered.
    """
    return registry.list_agents()
