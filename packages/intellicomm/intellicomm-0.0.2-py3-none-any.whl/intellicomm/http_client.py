"""
HTTP Client for IntelliComm Protocol with x402 payment integration.

This module provides an HTTP client that automatically handles x402 payment
flows when interacting with payment-protected agents.
"""

from typing import Dict, Any, Optional
import os
from eth_account import Account
from x402.clients.httpx import x402HttpxClient
import httpx

from .models import AgentResponse
from .payments import load_wallet_config


class HttpClient:
    """
    HTTP client for IntelliComm Protocol with automatic x402 payment handling.
    
    This client automatically processes 402 Payment Required responses and
    completes payment flows using the x402 protocol.
    """
    
    def __init__(self, base_url: str, private_key: Optional[str] = None):
        """
        Initialize HTTP client.
        
        Args:
            base_url: Base URL of the server (e.g., "http://localhost:8000")
            private_key: Wallet private key (optional, reads from WALLET_PRIVATE_KEY env var if not provided)
        """
        self.base_url = base_url.rstrip('/')
        
        # Load wallet configuration
        try:
            wallet_config = load_wallet_config()
            self.private_key = private_key or wallet_config["private_key"]
            self.network = wallet_config.get("network", "base-sepolia")
            self.facilitator_url = wallet_config.get("facilitator_url", "https://x402.org/facilitator")
        except ValueError as e:
            # If no wallet configured, create a basic client without payment support
            self.private_key = None
            self.network = None
            self.facilitator_url = None
            print(f"Warning: No wallet configured. Payment-protected agents will not be accessible. {e}")
        
        # Create wallet account if private key is available
        if self.private_key:
            self.account = Account.from_key(self.private_key)
        else:
            self.account = None
    
    async def execute_agent(self, agent_name: str, params: Dict[str, Any]) -> AgentResponse:
        """
        Execute an agent on the server with automatic payment handling.
        
        Args:
            agent_name: Name of the agent to execute
            params: Parameters to pass to the agent
            
        Returns:
            AgentResponse object containing the result or error
            
        Raises:
            Exception: If request fails or payment cannot be completed
        """
        url = f"{self.base_url}/agent/{agent_name}"
        payload = {"params": params}
        
        if self.account:
            # Use x402 client with payment support
            async with x402HttpxClient(
                account=self.account,
                base_url=self.base_url
            ) as client:
                try:
                    response = await client.post(
                        f"/agent/{agent_name}",
                        json=payload
                    )
                    
                    # Check response status
                    if response.status_code == 200:
                        data = response.json()
                        print(f"Response: {data}")
                        return AgentResponse(
                            status=data.get("status", "success"),
                            result=data.get("result"),
                            error=data.get("error")
                        )
                    else:
                        error_msg = f"HTTP {response.status_code}: {response.text}"
                        return AgentResponse.error(error_msg)
                        
                except Exception as e:
                    return AgentResponse.error(f"Request failed: {str(e)}")
        else:
            # Use regular httpx client without payment support
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(url, json=payload)
                    
                    if response.status_code == 402:
                        return AgentResponse.error(
                            "Payment required but no wallet configured. "
                            "Set WALLET_PRIVATE_KEY environment variable."
                        )
                    elif response.status_code == 200:
                        data = response.json()
                        return AgentResponse(
                            status=data.get("status", "success"),
                            result=data.get("result"),
                            error=data.get("error")
                        )
                    else:
                        error_msg = f"HTTP {response.status_code}: {response.text}"
                        return AgentResponse.error(error_msg)
                        
                except Exception as e:
                    return AgentResponse.error(f"Request failed: {str(e)}")
    
    def execute_agent_sync(self, agent_name: str, params: Dict[str, Any]) -> AgentResponse:
        """
        Synchronous version of execute_agent for convenience.
        
        Args:
            agent_name: Name of the agent to execute
            params: Parameters to pass to the agent
            
        Returns:
            AgentResponse object containing the result or error
        """
        import asyncio
        
        # Run the async function synchronously
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.execute_agent(agent_name, params))
    
    async def list_agents(self) -> Dict[str, Any]:
        """
        List all available agents on the server.
        
        Returns:
            Dictionary with agent information
        """
        url = f"{self.base_url}/agents"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "error": f"HTTP {response.status_code}: {response.text}",
                        "agents": [],
                        "total": 0
                    }
            except Exception as e:
                return {
                    "error": f"Request failed: {str(e)}",
                    "agents": [],
                    "total": 0
                }
    
    def list_agents_sync(self) -> Dict[str, Any]:
        """
        Synchronous version of list_agents.
        
        Returns:
            Dictionary with agent information
        """
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.list_agents())
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check server health status.
        
        Returns:
            Dictionary with health information
        """
        url = f"{self.base_url}/health"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "status": "error",
                        "error": f"HTTP {response.status_code}"
                    }
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e)
                }
    
    def health_check_sync(self) -> Dict[str, Any]:
        """
        Synchronous version of health_check.
        
        Returns:
            Dictionary with health information
        """
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.health_check())

