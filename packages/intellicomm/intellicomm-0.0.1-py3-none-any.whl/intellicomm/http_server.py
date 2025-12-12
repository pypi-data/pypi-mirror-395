"""
HTTP Server wrapper for IntelliComm Protocol with x402 payment integration.

This module provides an HTTP layer on top of the socket-based Server,
enabling x402 payment protocol support via FastAPI.
"""

from typing import Dict, Any, Optional
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn
from rich.console import Console

from .server import Server
from .models import AgentRequest, AgentResponse
from .payments import PaymentConfig, validate_payment_config
from x402.fastapi.middleware import require_payment


class HttpServer:
    """
    HTTP wrapper for IntelliComm Protocol Server with x402 payment support.
    
    This class wraps the socket-based Server and exposes it via HTTP/REST API
    with integrated x402 payment middleware for per-agent payment requirements.
    """
    
    def __init__(self, host='0.0.0.0', port=8000):
        """
        Initialize HTTP server.
        
        Args:
            host: Host to bind to (default: '0.0.0.0' for all interfaces)
            port: Port to bind to (default: 8000)
        """
        self.host = host
        self.port = port
        self.console = Console()
        
        # Create FastAPI app
        self.app = FastAPI(
            title="IntelliComm Protocol HTTP API",
            description="HTTP API for IntelliComm Protocol with x402 payment support",
            version="1.0.0"
        )
        
        # Store agents registry
        self.agents = {}
        
        # Setup routes
        self._setup_routes()
        
    def agent(self, payment_required=False, price=None, pay_to_address=None):
        """
        Decorator to register an agent with optional payment configuration.
        
        Args:
            payment_required: Whether payment is required to execute this agent
            price: Price in format "$0.001" (required if payment_required=True)
            pay_to_address: Wallet address to receive payment (optional, uses env var if not provided)
        """
        def decorator(func):
            agent_name = func.__name__
            agent_description = func.__doc__ or "No description provided."
            
            # Create payment configuration
            payment_config = None
            if payment_required:
                # Use provided address or fall back to environment variable
                address = pay_to_address or os.getenv("SERVER_WALLET_ADDRESS") or os.getenv("PAYMENT_ADDRESS")
                network = os.getenv("NETWORK", "base-sepolia")
                
                payment_config = PaymentConfig(
                    required=True,
                    price=price,
                    pay_to_address=address,
                    network=network
                )
                
                # Validate payment config
                try:
                    validate_payment_config(payment_config)
                except ValueError as e:
                    self.console.print(f"[red]❌ Invalid payment config for {agent_name}: {e}[/red]")
                    raise
            
            # Register the agent
            self.agents[agent_name] = {
                "handler": func,
                "description": agent_description.strip(),
                "payment": payment_config
            }
            
            # Create route for this agent
            self._create_agent_route(agent_name, payment_config)
            
            # Display registration
            self.console.print(f"[green]✅[/green] Registered agent: [bold blue]{agent_name}[/bold blue]")
            self.console.print(f"[dim]📝 Description: {agent_description.strip()}[/dim]")
            if payment_required:
                self.console.print(f"[yellow]💰 Payment Required: {price}[/yellow]")
            
            return func
        return decorator
    
    def _setup_routes(self):
        """Setup base HTTP routes."""
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {
                "status": "healthy",
                "service": "IntelliComm Protocol HTTP Server",
                "agents_registered": len(self.agents)
            }
        
        @self.app.get("/agents")
        async def list_agents():
            """List all registered agents."""
            agents_info = []
            for name, info in self.agents.items():
                agent_data = {
                    "name": name,
                    "description": info["description"],
                    "payment_required": False
                }
                if info.get("payment"):
                    payment = info["payment"]
                    agent_data["payment_required"] = True
                    agent_data["price"] = payment.price
                    agent_data["network"] = payment.network
                agents_info.append(agent_data)
            
            return {
                "agents": agents_info,
                "total": len(agents_info)
            }
    
    def _create_agent_route(self, agent_name: str, payment_config: Optional[PaymentConfig]):
        """
        Create a dynamic route for an agent with optional payment middleware.
        
        Args:
            agent_name: Name of the agent
            payment_config: Payment configuration (None if no payment required)
        """
        route_path = f"/agent/{agent_name}"
        
        # Create the handler function
        async def agent_handler(request: Request):
            try:
                # Parse request body
                body = await request.json()
                params = body.get("params", {})
                
                # Execute agent
                try:
                    result = self.agents[agent_name]["handler"](params)
                    
                    # Ensure result is a dictionary
                    if not isinstance(result, dict):
                        result = {"response": str(result)}
                    
                    response = AgentResponse.success(result)
                    return JSONResponse(content={
                        "status": response.status,
                        "result": response.result,
                        "error": response.error
                    })
                    
                except Exception as e:
                    self.console.print(f"[red]❌ Error executing agent {agent_name}: {e}[/red]")
                    response = AgentResponse.error(str(e))
                    return JSONResponse(
                        status_code=500,
                        content={
                            "status": response.status,
                            "result": response.result,
                            "error": response.error
                        }
                    )
                    
            except Exception as e:
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "error",
                        "error": f"Invalid request: {str(e)}"
                    }
                )
        
        # Set function name for FastAPI
        agent_handler.__name__ = f"execute_{agent_name}"
        
        # Apply payment middleware if required
        if payment_config and payment_config.required:
            # Apply x402 middleware to this specific route
            payment_middleware = require_payment(
                path=route_path,
                price=payment_config.price,
                pay_to_address=payment_config.pay_to_address,
                network=payment_config.network,
            )
            
            # Add middleware to the app
            self.app.middleware("http")(payment_middleware)
        
        # Register the route
        self.app.post(route_path)(agent_handler)
        
        self.console.print(f"[dim]🛤️  Created route: POST {route_path}[/dim]")
    
    def get_agent_payment_config(self, agent_name: str) -> Optional[PaymentConfig]:
        """
        Get payment configuration for a specific agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            PaymentConfig object or None if no payment required
            
        Raises:
            ValueError: If agent not found
        """
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not found")
        return self.agents[agent_name].get("payment")
    
    def start(self, reload=False):
        """
        Start the HTTP server using uvicorn.
        
        Args:
            reload: Enable auto-reload for development (default: False)
        """
        from rich.panel import Panel
        
        # Display startup panel
        startup_panel = Panel(
            f"[bold green]🚀 IntelliComm Protocol HTTP Server[/bold green]\n\n"
            f"[cyan]🌐 Host:[/cyan] [bold]{self.host}[/bold]\n"
            f"[cyan]🔌 Port:[/cyan] [bold]{self.port}[/bold]\n"
            f"[cyan]📡 Status:[/cyan] [bold green]STARTING[/bold green]\n"
            f"[cyan]🤖 Agents:[/cyan] [bold]{len(self.agents)}[/bold]\n"
            f"[cyan]💰 Payment:[/cyan] [bold]x402 Enabled[/bold]",
            title="[bold blue]Server Configuration[/bold blue]",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(startup_panel)
        
        # Display API documentation URL
        self.console.print(f"\n[cyan]📚 API Docs:[/cyan] [link]http://{self.host}:{self.port}/docs[/link]")
        self.console.print(f"[cyan]📖 ReDoc:[/cyan] [link]http://{self.host}:{self.port}/redoc[/link]\n")
        
        # Start uvicorn server
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            reload=reload,
            log_level="info"
        )

