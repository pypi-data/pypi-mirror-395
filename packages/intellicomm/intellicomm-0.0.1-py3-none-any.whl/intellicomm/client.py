from socket import *
from typing import Dict, Any
from .models import AgentRequest, AgentResponse

class Client:
    def __init__(self, host='localhost', port=5555):
        """Initialize the client with server connection details."""
        self.host = host
        self.port = port

    def execute_agent(self, agent_name: str, params: Dict[str, Any]) -> AgentResponse:
        """
        Execute an agent on the server.
        
        Args:
            agent_name: Name of the agent to execute
            params: Parameters to pass to the agent
        
        Returns:
            AgentResponse object containing the result or error
        """
        # Create and send request
        request = AgentRequest(agent=agent_name, params=params)
        
        # Send request and get response
        with socket(AF_INET, SOCK_STREAM) as sock:
            # Connect to server
            sock.connect((self.host, self.port))
            
            # Send request
            sock.send(request.to_json().encode('utf-8'))
            
            # Receive response
            chunks = []
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                chunks.append(chunk)
            
            response_data = b''.join(chunks)
            response_str = response_data.decode('utf-8')
            
            try:
                return AgentResponse.from_json(response_str)
            except Exception as e:
                print(f"Error parsing response: {e}")
                return None