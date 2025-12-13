"""
Agent Registry

Manages active agent clients and their connections.
"""

from typing import Dict, Optional, Any
from qaldron.sdk import AgentClient
from datetime import datetime
import threading


class AgentRegistry:
    """
    Thread-safe registry for active agents
    
    Manages AgentClient instances and WebSocket connections.
    """
    
    def __init__(self):
        self.agents: Dict[str, AgentClient] = {}
        self.metadata: Dict[str, dict] = {}  # agent_id -> metadata
        self.websockets: Dict[str, Any] = {}  # agent_id -> WebSocket
        self._lock = threading.Lock()
    
    def register(self, agent_id: str, client: AgentClient) -> dict:
        """
        Register a new agent
        
        Args:
            agent_id: Unique agent identifier
            client: AgentClient instance
            
        Returns:
            dict: Agent metadata
        """
        with self._lock:
            self.agents[agent_id] = client
            self.metadata[agent_id] = {
                "created_at": datetime.utcnow().isoformat() + "Z",
                "connected": True,
                "encryption_enabled": client.enable_encryption
            }
            return self.metadata[agent_id]
    
    def get(self, agent_id: str) -> Optional[AgentClient]:
        """Get agent client by ID"""
        return self.agents.get(agent_id)
    
    def get_metadata(self, agent_id: str) -> Optional[dict]:
        """Get agent metadata"""
        return self.metadata.get(agent_id)
    
    def exists(self, agent_id: str) -> bool:
        """Check if agent is registered"""
        return agent_id in self.agents
    
    def deregister(self, agent_id: str) -> bool:
        """
        Remove agent from registry
        
        Returns:
            bool: True if agent was removed, False if not found
        """
        with self._lock:
            if agent_id in self.agents:
                del self.agents[agent_id]
                if agent_id in self.metadata:
                    del self.metadata[agent_id]
                if agent_id in self.websockets:
                    del self.websockets[agent_id]
                return True
            return False
    
    def list_agents(self) -> list:
        """Get list of all registered agent IDs"""
        return list(self.agents.keys())
    
    def count(self) -> int:
        """Get number of registered agents"""
        return len(self.agents)
    
    def register_websocket(self, agent_id: str, websocket):
        """Register WebSocket connection for agent"""
        with self._lock:
            self.websockets[agent_id] = websocket
    
    def get_websocket(self, agent_id: str):
        """Get WebSocket connection for agent"""
        return self.websockets.get(agent_id)
    
    def deregister_websocket(self, agent_id: str):
        """Remove WebSocket connection"""
        with self._lock:
            if agent_id in self.websockets:
                del self.websockets[agent_id]


# Global registry instance
registry = AgentRegistry()
