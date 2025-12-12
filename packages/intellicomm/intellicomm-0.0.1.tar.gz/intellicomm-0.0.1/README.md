# IntelliComm Protocol (ICP)

A powerful Python framework for intelligent communication protocol with **x402 payment integration**.

## ✨ Features

- 🤖 **Agent-based architecture** - Register and execute intelligent agents
- 💰 **x402 Payment Protocol** - Monetize your agents with crypto payments
- 🔌 **Dual Protocol Support** - Socket-based (legacy) and HTTP (with payments)
- 🎨 **Beautiful Console Output** - Rich terminal UI with colors and panels
- 🔒 **Secure Payments** - Blockchain-based payments via Ethereum/Base/Solana
- ⚙️ **Per-Agent Configuration** - Configure payments for individual agents
- 🚀 **Easy to Use** - Simple decorators and intuitive API

## 🆕 What's New: x402 Payment Integration

IntelliComm Protocol now supports **x402 payment protocol**, allowing you to:

- ✅ Require payment for specific agents (per-agent pricing)
- ✅ Accept crypto payments on multiple networks (Base, Ethereum, Solana)
- ✅ Automatic payment handling on the client side
- ✅ Test with testnet and deploy to mainnet
- ✅ Beautiful console output showing payment status

## 📁 Project Structure

```
IntelliComm-Protocol-ICP/
├── intellicomm/                 # Core Python framework package
│   ├── __init__.py              # Package exports
│   ├── models.py                # Data models (Request, Response)
│   ├── server.py                # Socket-based server (legacy)
│   ├── client.py                # Socket-based client (legacy)
│   ├── http_server.py           # HTTP server with x402 payments ⭐ NEW
│   ├── http_client.py           # HTTP client with x402 payments ⭐ NEW
│   ├── payments.py              # Payment configuration & utilities ⭐ NEW
│   ├── agent.py                 # Agent implementations
│   └── utils.py                 # Helper functions
├── tests/                       # Example & test files
│   ├── run_server.py            # Socket-based server example
│   ├── run_client.py            # Socket-based client example
│   ├── run_http_server.py       # HTTP server with payments example ⭐ NEW
│   └── run_http_client.py       # HTTP client with payments example ⭐ NEW
├── env.example                  # Environment configuration template ⭐ NEW
├── PAYMENT_GUIDE.md            # Complete payment integration guide ⭐ NEW
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/IntelliComm-Protocol-ICP.git
cd IntelliComm-Protocol-ICP

# Install dependencies
pip install -r requirements.txt

# Configure environment (for payment features)
cp env.example .env
# Edit .env with your wallet details
```

### Basic Usage (Socket-based - No Payments)

**Server:**
```python
from intellicomm import Server

server = Server(host='localhost', port=5555)

@server.agent()
def greet(params):
    """Simple greeting agent"""
    name = params.get("name", "Guest")
    return {"greeting": f"Hello, {name}!"}

server.start()
```

**Client:**
```python
from intellicomm import Client

client = Client(host='localhost', port=5555)
response = client.execute_agent("greet", {"name": "Alice"})
print(response.result)
```

### HTTP with Payments (x402)

**Server:**
```python
from intellicomm import HttpServer

server = HttpServer(host='0.0.0.0', port=8000)

@server.agent()  # Free agent
def free_service(params):
    """Free service - no payment required"""
    return {"data": "free content"}

@server.agent(payment_required=True, price="$0.001")  # Paid agent
def premium_service(params):
    """Premium service - requires $0.001 payment"""
    return {"data": "premium content"}

server.start()
```

**Client:**
```python
from intellicomm import HttpClient
import asyncio

async def main():
    client = HttpClient(base_url="http://localhost:8000")
    
    # Call free service
    response = await client.execute_agent("free_service", {})
    print(response.result)
    
    # Call paid service (payment handled automatically!)
    response = await client.execute_agent("premium_service", {})
    print(response.result)

asyncio.run(main())
```

## 💰 Payment Configuration

### Environment Setup

Create a `.env` file (copy from `env.example`):

```bash
# Client wallet (for making payments)
WALLET_PRIVATE_KEY=0x1234567890abcdef...

# Server address (for receiving payments)
PAYMENT_ADDRESS=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7

# Network (testnet for development)
NETWORK=base-sepolia

# Facilitator (optional, uses default)
FACILITATOR_URL=https://x402.org/facilitator
```

### Getting Test Funds

For Base Sepolia testnet:
1. Visit [Base Sepolia Faucet](https://www.coinbase.com/faucets/base-ethereum-goerli-faucet)
2. Enter your wallet address
3. Receive test ETH

## 📚 Documentation

- **[PAYMENT_GUIDE.md](PAYMENT_GUIDE.md)** - Complete guide to x402 payment integration
- **[env.example](env.example)** - Environment configuration template
- **API Docs** - Auto-generated at `http://localhost:8000/docs` when server runs

## 🧪 Examples

Run the example server with payments:
```bash
python tests/run_http_server.py
```

In another terminal, run the client:
```bash
python tests/run_http_client.py
```

## 🔑 Key Features

### Per-Agent Payment Configuration

Configure payment requirements for each agent individually:

```python
@server.agent()  # Free
def free_agent(params):
    return {"data": "free"}

@server.agent(payment_required=True, price="$0.001")  # Costs $0.001
def cheap_agent(params):
    return {"data": "cheap"}

@server.agent(payment_required=True, price="$0.010")  # Costs $0.010
def premium_agent(params):
    return {"data": "premium"}
```

### Automatic Payment Handling

Clients automatically handle payment flows - no manual transaction code needed:

```python
# Just call the agent - payment is automatic!
response = await client.execute_agent("premium_agent", {})
```

### Multiple Networks Supported

- **base-sepolia** (testnet) - Recommended for development
- **base-mainnet** (production)
- **ethereum-sepolia** / **ethereum-mainnet**
- **solana-devnet** / **solana-mainnet**

## 🛠️ Development

### Project Status

✅ Core framework complete  
✅ Socket-based communication  
✅ HTTP layer with FastAPI  
✅ x402 payment integration  
✅ Beautiful console output  
🔄 Documentation in progress  

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Support

- 📧 Email: ahsentahir007@gmail.com
- 📖 Documentation: See PAYMENT_GUIDE.md
- 🐛 Issues: GitHub Issues

## 🌟 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com)
- Payments via [x402 Protocol](https://docs.x402.org)
- Beautiful console with [Rich](https://rich.readthedocs.io)

---

**Made with ❤️ by Ahsen Tahir**
