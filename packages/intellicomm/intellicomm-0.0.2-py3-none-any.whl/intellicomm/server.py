from socket import *
import signal
import sys
import threading
import os
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

from .payments import PaymentConfig

class Server:
    def __init__(self, host='localhost', port=5555):
        self.agents = {}
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        
        # Setup Rich console for beautiful output
        self.console = Console()
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

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
            
            # Register the agent
            self.agents[agent_name] = {
                "handler": func,
                "description": agent_description.strip(),
                "payment": payment_config
            }

            self.console.print(f"[green]✅[/green] Registered agent: [bold blue]{agent_name}[/bold blue]")
            self.console.print(f"[dim]📝 Description: {agent_description.strip()}[/dim]")
            if payment_required:
                self.console.print(f"[yellow]💰 Payment Required: {price}[/yellow]")
            
            return func
        return decorator

    def _display_registered_agents(self):
        """Display all registered agents in a beautiful Rich format."""
        if not self.agents:
            self.console.print("[yellow]📋 No agents registered[/yellow]")
            return
        
        # Create a table for agents
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("🤖 Agent", style="cyan", no_wrap=True)
        table.add_column("📝 Description", style="white")
        table.add_column("💰 Payment", style="yellow", justify="center")
        table.add_column("🟢 Status", style="green", justify="center")
        
        # Add each agent to the table
        for agent_name, agent_info in self.agents.items():
            description = agent_info["description"]
            payment_info = "[dim]Free[/dim]"
            if agent_info.get("payment") and agent_info["payment"].required:
                payment_info = f"[yellow]{agent_info['payment'].price}[/yellow]"
            table.add_row(
                f"[bold]{agent_name}[/bold]",
                description,
                payment_info,
                "[bold green]ACTIVE[/bold green]"
            )
        
        # Create a beautiful panel with the table
        panel_content = Align.center(table)
        panel = Panel(
            panel_content,
            title="[bold blue]🤖 Registered Agents[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print()
        self.console.print(panel)
        self.console.print()

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.console.print("\n[red]🛑 Received shutdown signal. Stopping server...[/red]")
        self.stop()

    def stop(self):
        """Stop the server gracefully."""
        self.running = False
        if self.socket:
            self.socket.close()
        self.console.print("[green]✅ Server stopped successfully[/green]")

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

    def _handle_client(self, client_socket, client_address):
        """Handle individual client connections."""
        try:
            self.console.print(f"[cyan]🔗 New connection from {client_address}[/cyan]")
            
            # Receive data from client
            data = client_socket.recv(1024)
            if data:
                message = data.decode('utf-8')
                self.console.print(f"[yellow]📨 Received: {message}[/yellow]")
                
                # Process the message (for now, just echo it back)
                response = f"Server received: {message}"
                client_socket.send(response.encode('utf-8'))
                
        except Exception as e:
            self.console.print(f"[red]❌ Error handling client {client_address}: {e}[/red]")
        finally:
            client_socket.close()
            self.console.print(f"[dim]🔌 Connection closed for {client_address}[/dim]")

    def start(self):
        """Start the server and begin accepting connections."""
        try:
            # Create socket
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            
            # Bind to host and port
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            # Set running flag
            self.running = True
            
            # Beautiful startup sequence with Rich
            self.console.print()
            
            # Server startup panel
            startup_panel = Panel(
                f"[bold green]🚀 IntelliComm Protocol Server[/bold green]\n\n"
                f"[cyan]🌐 Host:[/cyan] [bold]{self.host}[/bold]\n"
                f"[cyan]🔌 Port:[/cyan] [bold]{self.port}[/bold]\n"
                f"[cyan]📡 Status:[/cyan] [bold green]LISTENING[/bold green]",
                title="[bold blue]Server Configuration[/bold blue]",
                border_style="green",
                padding=(1, 2)
            )
            self.console.print(startup_panel)
            
            # Display registered agents
            self._display_registered_agents()
            
            # Ready message
            ready_panel = Panel(
                "[bold green]✨ Server is ready to accept agents![/bold green]\n"
                "[dim]💡 Press Ctrl+C to stop the server[/dim]",
                border_style="green",
                padding=(1, 2)
            )
            self.console.print(ready_panel)
            
            # Main server loop
            while self.running:
                try:
                    # Accept incoming connections
                    self.socket.settimeout(1.0)  # 1 second timeout to allow checking self.running
                    client_socket, client_address = self.socket.accept()
                    
                    # Handle client in a separate thread
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except timeout:
                    # Timeout occurred, continue the loop to check self.running
                    continue
                except OSError:
                    # Socket was closed (likely due to stop() being called)
                    break
                except Exception as e:
                    if self.running:  # Only log if we're still supposed to be running
                        self.console.print(f"[red]❌ Error accepting connection: {e}[/red]")
            
        except Exception as e:
            self.console.print(f"[red]❌ Failed to start server: {e}[/red]")
            raise
        finally:
            self.stop()