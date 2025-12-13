"""
AmorceAgent - Secure LangChain agent wrapper

Provides Ed25519 signatures, HITL approvals, and A2A compatibility.
"""

from typing import List, Optional, Dict, Any
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chat_models.base import BaseChatModel
from langchain.tools import BaseTool
from langchain import hub


class AmorceAgent:
    """
    LangChain agent with Amorce security.
    
    All agent actions are:
    - Cryptographically signed (Ed25519)
    - Verified via Trust Directory
    - HITL for sensitive operations
    - A2A-compatible
    
    Example:
        ```python
        from langchain_amorce import AmorceAgent
        from langchain.chat_models import ChatOpenAI
        
        agent = AmorceAgent(
            llm=ChatOpenAI(),
            tools=[search_tool],
            secure=True
        )
        
        result = agent.run("What's the weather?")
        ```
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        tools: List[BaseTool],
        secure: bool = True,
        identity: Optional[Any] = None,
        hitl_required: Optional[List[str]] = None,
        a2a_compatible: bool = True,
        verbose: bool = False,
        name: Optional[str] = None,
        role: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize secure LangChain agent.
        
        Args:
            llm: Language model (e.g., ChatOpenAI)
            tools: List of LangChain tools
            secure: Enable Amorce security (default: True)
            identity: Amorce identity (auto-generated if None)
            hitl_required: Tool names requiring human approval
            a2a_compatible: Use A2A message format
            verbose: Show agent reasoning
            name: Agent name (optional)
            role: Agent role description (optional)
        """
        self.llm = llm
        self.tools = tools
        self.secure = secure
        self.verbose = verbose
        self.a2a_compatible = a2a_compatible
        self.name = name or "AmorceAgent"
        self.role = role or "Secure AI Agent"
        
        # Generate or load Amorce identity
        if secure:
            from amorce import IdentityManager, AmorceClient
            
            self.identity = identity or IdentityManager.generate()
            
            # Initialize Amorce client
            self.amorce_client = AmorceClient(
                self.identity,
                directory_url='https://directory.amorce.io',
                orchestrator_url='https://api.amorce.io'
            )
        else:
            self.identity = None
            self.amorce_client = None
        
        # HITL configuration
        self.hitl_required = hitl_required or []
        
        # Wrap tools with Amorce security
        if secure:
            from langchain_amorce.tools import AmorceToolWrapper
            self.tools = [
                AmorceToolWrapper(
                    tool=tool,
                    identity=self.identity,
                    client=self.amorce_client,
                    requires_hitl=(tool.name in self.hitl_required)
                )
                for tool in tools
            ]
        
        # Create LangChain agent
        self.agent_executor = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        """Create LangChain AgentExecutor."""
        # Get base prompt
        prompt = hub.pull("hwchase17/react")
        
        if self.secure:
            # Add Amorce security context
            prompt.template += f"""

🔐 Security Context:
- Agent Name: {self.name}
- Role: {self.role}
- Agent ID: {self.identity.agent_id}
- All actions are cryptographically signed
- Sensitive operations require human approval
"""
        
        # Create agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=self.verbose,
            handle_parsing_errors=True
        )
    
    def run(self, input: str) -> Dict[str, Any]:
        """
        Run agent with Amorce security.
        
        Args:
            input: User input/query
            
        Returns:
            Agent response with security metadata
        """
        if self.secure and self.a2a_compatible:
            # Wrap in A2A-compatible envelope
            from langchain_amorce.a2a import A2AEnvelope
            
            envelope = A2AEnvelope(
                sender_id=self.identity.agent_id,
                message=input,
                signature=self.identity.sign(input)
            )
            
            # Run agent
            result = self.agent_executor.invoke({"input": input})
            
            # Return with A2A metadata
            return {
                "output": result.get("output"),
                "agent_id": self.identity.agent_id,
                "signature": self.identity.sign(result.get("output", "")),
                "protocol": "a2a/1.0",
                "security_layer": "amorce/3.0"
            }
        else:
            # Standard execution
            result = self.agent_executor.invoke({"input": input})
            return result
    
    @property
    def agent_id(self) -> Optional[str]:
        """Get Amorce agent ID."""
        return self.identity.agent_id if self.identity else None
    
    def discover_agents(self, capability: str) -> List[Dict[str, Any]]:
        """
        Discover other agents in Trust Directory.
        
        Args:
            capability: Required capability (e.g., 'sell_laptops')
            
        Returns:
            List of matching agents
        """
        if not self.secure:
            raise RuntimeError("Discovery requires secure mode")
        
        # Query Trust Directory
        return self.amorce_client.discover(capability)
    
    def negotiate_with(self, target_agent: Dict[str, Any], **kwargs):
        """
        Negotiate with another agent.
        
        Args:
            target_agent: Agent from Trust Directory
            **kwargs: Negotiation parameters
        """
        if not self.secure:
            raise RuntimeError("Negotiation requires secure mode")
        
        # Implementation for agent-to-agent negotiation
        # This would use Amorce's transact() method
        pass
