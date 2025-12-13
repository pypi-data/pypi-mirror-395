"""
MCP Helpers for Amorce Python SDK

Convenience methods for calling MCP tools through Amorce protocol.
"""

from typing import Dict, Any, Optional
from .client import AmorceClient


class MCPToolClient:
    """
    Helper for calling MCP tools via Amorce.
    
    Usage:
        identity = IdentityManager.generate_ephemeral()
        mcp = MCPToolClient(identity)
        
        # Call filesystem tool
        result = mcp.call_tool('filesystem', 'read_file', {'path': '/tmp/test.txt'})
        
        # Call with HITL
        approval_id = mcp.request_tool_approval(
            'filesystem', 
            'write_file',
            {'path': '/tmp/test.txt', 'content': 'Hello'},
            summary="Write test file"
        )
        # After human approval...
        result = mcp.call_tool(
            'filesystem', 
            'write_file',
            {'path': '/tmp/test.txt', 'content': 'Hello'},
            approval_id=approval_id
        )
    """
    
    def __init__(self, identity, orchestrator_url: Optional[str] = None):
        """
        Initialize MCP tool client.
        
        Args:
            identity: Amorce identity for signing requests
            orchestrator_url: Optional orchestrator URL
        """
        self.client = AmorceClient(identity, orchestrator_url=orchestrator_url)
        self.identity = identity
        
    def list_tools(self, server_name: str) -> Dict[str, Any]:
        """
        List available tools from an MCP server.
        
        Args:
            server_name: MCP server name (e.g., 'filesystem')
            
        Returns:
            Dictionary with available tools
        """
        service_contract = {
            "service_id": f"mcp-{server_name}-list-tools",
            "provider_agent_id": f"agent-mcp-{server_name}"
        }
        
        return self.client.transact(
            service_contract=service_contract,
            payload={"action": "list_tools"}
        )
        
    def call_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
        approval_id: Optional[str] = None
    ) -> Any:
        """
        Call MCP tool through Amorce protocol.
        
        Args:
            server_name: MCP server name (e.g., 'filesystem')
            tool_name: Tool to call (e.g., 'read_file')
            arguments: Tool arguments
            approval_id: Optional HITL approval ID
            
        Returns:
            Tool execution result
        """
        service_contract = {
            "service_id": f"mcp-{server_name}-{tool_name}",
            "provider_agent_id": f"agent-mcp-{server_name}"
        }
        
        payload = {
            "tool_name": tool_name,
            "arguments": arguments
        }
        
        if approval_id:
            payload["approval_id"] = approval_id
            
        return self.client.transact(
            service_contract=service_contract,
            payload=payload
        )
        
    def request_tool_approval(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
        summary: str,
        timeout_seconds: int = 300
    ) -> str:
        """
        Request HITL approval for MCP tool call.
        
        Args:
            server_name: MCP server name
            tool_name: Tool requiring approval
            arguments: Tool arguments to be approved
            summary: Human-readable summary
            timeout_seconds: Approval timeout
            
        Returns:
            Approval ID
        """
        return self.client.request_approval(
            summary=f"[MCP/{server_name}] {summary}",
            details={
                "server": server_name,
                "tool": tool_name,
                "arguments": arguments
            },
            timeout_seconds=timeout_seconds
        )
        
    def list_resources(self, server_name: str) -> Dict[str, Any]:
        """
        List available resources from an MCP server.
        
        Args:
            server_name: MCP server name
            
        Returns:
            Dictionary with available resources
        """
        service_contract = {
            "service_id": f"mcp-{server_name}-list-resources",
            "provider_agent_id": f"agent-mcp-{server_name}"
        }
        
        return self.client.transact(
            service_contract=service_contract,
            payload={"action": "list_resources"}
        )
        
    def read_resource(
        self,
        server_name: str,
        uri: str
    ) -> Any:
        """
        Read an MCP resource.
        
        Args:
            server_name: MCP server name
            uri: Resource URI
            
        Returns:
            Resource contents
        """
        service_contract = {
            "service_id": f"mcp-{server_name}-read-resource",
            "provider_agent_id": f"agent-mcp-{server_name}"
        }
        
        return self.client.transact(
            service_contract=service_contract,
            payload={
                "action": "read_resource",
                "uri": uri
            }
        )
