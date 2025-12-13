"""
Amorce-wrapped LangChain tools with signatures + HITL
"""

from typing import Optional, Any
from langchain.tools import BaseTool


class AmorceToolWrapper(BaseTool):
    """
    Wraps LangChain tool with Amorce security.
    
    Adds:
    - Ed25519 signatures to tool calls
    - HITL approvals for sensitive operations
    - Transaction logging
    """
    
    def __init__(
        self,
        tool: BaseTool,
        identity: Any,
        client: Any,
        requires_hitl: bool = False
    ):
        """
        Initialize tool wrapper.
        
        Args:
            tool: Original LangChain tool
            identity: Amorce IdentityManager
            client: Amorce client
            requires_hitl: Whether this tool requires human approval
        """
        # Copy tool metadata
        super().__init__(
            name=tool.name,
            description=tool.description,
            func=tool.func if hasattr(tool, 'func') else None
        )
        
        # Amorce integration
        self.identity = identity
        self.client = client
        self.requires_hitl = requires_hitl
        self.original_tool = tool
    
    def _run(self, *args, **kwargs) -> Any:
        """
        Run tool with Amorce signature.
        
        Returns tool result with security metadata.
        """
        import json
        
        # Prepare tool call data
        call_data = {
            'tool': self.name,
            'args': list(args),
            'kwargs': kwargs,
            'agent_id': self.identity.agent_id
        }
        
        # Sign the tool call
        signature = self.identity.sign(json.dumps(call_data, sort_keys=True))
        
        # HITL if required
        if self.requires_hitl:
            print(f"\n⏸️  HUMAN APPROVAL REQUIRED for {self.name}")
            print(f"   Tool: {self.name}")
            print(f"   Args: {args}")
            print(f"   Kwargs: {kwargs}")
            
            approval_id = self.client.request_approval(
                summary=f"Approve {self.name} execution",
                details=call_data,
                timeout_seconds=300
            )
            
            # Check approval status
            import time
            max_wait = 300  # 5 minutes
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                status = self.client.check_approval(approval_id)
                
                if status['status'] == 'approved':
                    print(f"✅ Approval granted for {self.name}")
                    break
                elif status['status'] == 'rejected':
                    raise PermissionError(
                        f"HITL approval denied for {self.name}"
                    )
                elif status['status'] == 'expired':
                    raise TimeoutError(
                        f"HITL approval expired for {self.name}"
                    )
                
                time.sleep(1)  # Poll every second
            else:
                raise TimeoutError(
                    f"HITL approval timeout for {self.name}"
                )
        
        # Execute original tool
        result = self.original_tool._run(*args, **kwargs)
        
        # Return with signature proof
        return {
            'result': result,
            'tool': self.name,
            'agent_id': self.identity.agent_id,
            'signature': signature,
            'hitl_required': self.requires_hitl
        }
    
    async def _arun(self, *args, **kwargs) -> Any:
        """Async version of _run."""
        # For now, call sync version
        # TODO: Implement true async
        return self._run(*args, **kwargs)
