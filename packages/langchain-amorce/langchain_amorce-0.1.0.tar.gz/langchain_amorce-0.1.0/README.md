# langchain-amorce

[![GitHub](https://img.shields.io/github/stars/trebortGolin/langchain-amorce?style=social)](https://github.com/trebortGolin/langchain-amorce)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Demo](https://img.shields.io/badge/demo-marketplace-success.svg)](https://github.com/trebortGolin/agent-marketplace-demo)

**Secure LangChain agents with Amorce in 2 lines of code**

Add Ed25519 signatures, human-in-the-loop approvals, and A2A compatibility to any LangChain agent.

---

## 🚀 Quick Start

### Installation

```bash
pip install langchain-amorce
```

### Basic Usage (2 Lines!)

```python
from langchain_amorce import AmorceAgent
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun

# Create secure agent
agent = AmorceAgent(
    llm=ChatOpenAI(model="gpt-4"),
    tools=[DuckDuckGoSearchRun()],
    secure=True  # ← Adds Amorce security
)

# Use normally - all actions are now cryptographically signed
result = agent.run("What's the latest AI news?")
print(f"Agent ID: {agent.agent_id}")  # Verified identity
```

**That's it!** Your LangChain agent now has:
- ✅ Ed25519 cryptographic signatures
- ✅ Trust Directory verification
- ✅ Automatic identity management
- ✅ A2A-compatible messages

---

## 🛡️ Features

### Cryptographic Signatures
Every agent action is signed with Ed25519, providing non-repudiable proof of authorization.

### Human-in-the-Loop (HITL)
Require human approval for sensitive operations:

```python
from langchain.tools import ShellTool

agent = AmorceAgent(
    llm=ChatOpenAI(),
    tools=[
        DuckDuckGoSearchRun(),  # No approval needed
        ShellTool()              # Dangerous!
    ],
    hitl_required=['shell'],  # Require approval for shell
    secure=True
)

# Search works normally
agent.run("Search for Python tutorials")

# Shell command triggers approval popup
agent.run("Delete tmp files")  # ← Human approval required!
```

### A2A Protocol Compatible
Messages are formatted for Agent-to-Agent Protocol compatibility:

```python
agent = AmorceAgent(
    llm=ChatOpenAI(),
    tools=[search],
    a2a_compatible=True  # ← Enable A2A format
)

# All messages use A2A envelope with Amorce signatures
```

---

## 📖 Examples

### Marketplace Demo (Sarah - Buyer Agent)

See the full [Enhanced Marketplace Demo](../marketplace-demo) showing Sarah negotiating with Henri.

```python
from langchain_amorce import AmorceAgent
from langchain.chat_models import ChatOpenAI

sarah = AmorceAgent(
    name="Sarah",
    role="Smart Shopper",
    llm=ChatOpenAI(model="gpt-4"),
    tools=[
        brave_search_tool,      # Price research
        budget_calculator,       # Affordability check
        fraud_detector,         # Verify seller
    ],
    hitl_required=['make_payment', 'share_address'],
    max_budget=500,
    secure=True
)

# Sarah autonomously:
# 1. Searches for MacBook Pro
# 2. Finds sellers in Trust Directory
# 3. Verifies reputations
# 4. Negotiates price
# 5. Requests human approval for payment
```

---

## 🔧 Advanced Configuration

### Custom Identity

```python
from amorce import IdentityManager

# Load existing identity
identity = IdentityManager.load_from_file("my_agent.pem")

agent = AmorceAgent(
    llm=ChatOpenAI(),
    tools=[...],
    identity=identity  # Use specific identity
)
```

### Custom Amorce Client

```python
from amorce import AmorceClient

client = AmorceClient(
    identity,
    directory_url='https://my-directory.com',
    orchestrator_url='https://my-orchestrator.com'
)

agent = AmorceAgent(
    llm=ChatOpenAI(),
    tools=[...],
    amorce_client=client  # Custom client
)
```

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=langchain_amorce tests/
```

---

## 📚 Documentation

- [Amorce Documentation](https://amorce.io/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [A2A Protocol](https://a2a-protocol.org/)

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🔗 Links

- **Amorce**: [amorce.io](https://amorce.io)
- **GitHub**: [github.com/amorce/langchain-amorce](https://github.com/amorce/langchain-amorce)
- **PyPI**: [pypi.org/project/langchain-amorce](https://pypi.org/project/langchain-amorce/)
- **Issues**: [github.com/amorce/langchain-amorce/issues](https://github.com/amorce/langchain-amorce/issues)

---

**Built with ❤️ by the Amorce team**
