"""
Basic tests for langchain-amorce
"""

import pytest
from unittest.mock import Mock, MagicMock

def test_amorce_agent_initialization():
    """Test that AmorceAgent can be initialized."""
    from langchain_amorce import AmorceAgent
    from langchain.chat_models.fake import FakeListChatModel
    
    llm = FakeListChatModel(responses=["test response"])
    
    agent = AmorceAgent(
        llm=llm,
        tools=[],
        secure=False  # Don't require Amorce in tests
    )
    
    assert agent is not None
    assert agent.llm == llm

def test_agent_id_generated():
    """Test that agent ID is generated when secure=True."""
    from langchain_amorce import AmorceAgent
    from langchain.chat_models.fake import FakeListChatModel
    
    # Mock Amorce SDK
    try:
        agent = AmorceAgent(
            llm=FakeListChatModel(responses=["test"]),
            tools=[],
            secure=True
        )
        assert agent.agent_id is not None
    except ImportError:
        # Amorce SDK not installed in test env
        pytest.skip("Amorce SDK not available")

def test_tool_wrapper():
    """Test AmorceToolWrapper."""
    from langchain_amorce.tools import AmorceToolWrapper
    from langchain.tools import Tool
    
    # Create fake tool
    fake_tool = Tool(
        name="test_tool",
        description="A test tool",
        func=lambda x: f"Result: {x}"
    )
    
    # Mock identity and client
    mock_identity = Mock()
    mock_identity.agent_id = "test_agent_id"
    mock_identity.sign = Mock(return_value="fake_signature")
    
    mock_client = Mock()
    
    # Wrap tool
    wrapper = AmorceToolWrapper(
        tool=fake_tool,
        identity=mock_identity,
        client=mock_client,
        requires_hitl=False
    )
    
    assert wrapper.name == "test_tool"
    assert wrapper.original_tool == fake_tool

def test_a2a_envelope():
    """Test A2AEnvelope creation and serialization."""
    from langchain_amorce.a2a import A2AEnvelope
    
    envelope = A2AEnvelope(
        sender_id="test_agent",
        message="Hello",
        signature="fake_sig"
    )
    
    data = envelope.to_dict()
    
    assert data['protocol'] == 'a2a/1.0'
    assert data['security']['sender_id'] == 'test_agent'
    assert data['security']['signature'] == 'fake_sig'
    assert data['payload']['message'] == 'Hello'

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
