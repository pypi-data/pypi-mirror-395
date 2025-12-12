# Installation Guide

This guide covers all installation methods for the Agent Framework, from basic installation to advanced development setups.

## Table of Contents

- [Quick Install](#quick-install)
- [Installation Options](#installation-options)
- [Development Setup](#development-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Quick Install

The fastest way to get started:

```bash
# Install base framework
pip install agent-framework-lib

# Or with UV (recommended)
uv add agent-framework-lib

# Post-installation: Install Playwright browsers
playwright install chromium
```

**Note:** The framework automatically detects and configures PDF tools (poppler) if installed on your system. See [System Dependencies](#system-dependencies) for details.

## Installation Options

The Agent Framework supports multiple installation configurations depending on your needs.

### Base Installation

Install the core framework without any specific agent implementation:

```bash
uv add agent-framework-lib
```

**Includes:**
- Core framework components
- Session management
- State persistence
- File storage
- Web server (FastAPI)
- REST API
- Web UI

**Use this when:**
- You want to implement a custom agent from scratch
- You're using a framework not yet supported
- You only need the core infrastructure

### LlamaIndex Installation

Install with LlamaIndex support (recommended for most users):

```bash
uv add agent-framework-lib[llamaindex]
```

**Includes:**
- Everything in base installation
- LlamaIndex framework
- LlamaIndex LLM integrations (OpenAI, Anthropic, Gemini)
- LlamaIndex tools and utilities
- `LlamaIndexAgent` base class

**Use this when:**
- You want to build agents with LlamaIndex
- You need RAG (Retrieval-Augmented Generation) capabilities
- You want the simplest development experience

### Microsoft Agent Framework Installation

Install with Microsoft Agent Framework support:

```bash
uv add agent-framework-lib[microsoft]
```

**Includes:**
- Everything in base installation
- Microsoft Agent Framework
- Microsoft-specific integrations
- `MicrosoftAgent` base class

**Use this when:**
- You're building agents with Microsoft's framework
- You need Microsoft-specific features
- You're integrating with Microsoft services

### Complete Installation

Install with support for all frameworks:

```bash
uv add agent-framework-lib[all]
```

**Includes:**
- Everything from all installation options
- LlamaIndex support
- Microsoft Agent Framework support
- All optional dependencies

**Use this when:**
- You're exploring different frameworks
- You need maximum flexibility
- You're building multi-framework applications

### Development Installation

Install with development tools and testing dependencies:

```bash
uv add agent-framework-lib[dev]
```

**Includes:**
- Everything in base installation
- Testing tools (pytest, pytest-cov, pytest-asyncio)
- Code quality tools (black, flake8, mypy)
- Documentation tools
- Development utilities

**Use this when:**
- You're contributing to the framework
- You're developing custom extensions
- You need testing and debugging tools

## Development Setup

For development work on the framework itself:

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/agent-framework.git
cd agent-framework
```

### 2. Create Virtual Environment

**Using UV (Recommended):**

```bash
# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**Using venv:**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install in Editable Mode

```bash
# With UV (recommended)
uv pip install -e .[dev]

# With pip
uv add -e .[dev]
```

### 4. Configure Environment

```bash
# Copy environment template
cp env-template.txt .env

# Edit .env with your settings
nano .env  # or your preferred editor
```

**Minimal .env configuration:**

```env
# API Keys (at least one required)
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
GEMINI_API_KEY=your-gemini-api-key-here

# Default Model
DEFAULT_MODEL=gpt-4o-mini

# Authentication (optional)
REQUIRE_AUTH=false
BASIC_AUTH_USERNAME=admin
BASIC_AUTH_PASSWORD=password
API_KEYS=sk-your-secure-api-key-123

# Session Storage (optional)
SESSION_STORAGE_TYPE=memory  # or "mongodb"
# MONGODB_CONNECTION_STRING=mongodb://localhost:27017
# MONGODB_DATABASE_NAME=agent_sessions

# File Storage (optional)
LOCAL_STORAGE_PATH=./file_storage
# AWS_S3_BUCKET=my-agent-files
# AWS_REGION=us-east-1
```

### 5. Verify Installation

```bash
# Run tests
uv run pytest

# Or with pytest directly
pytest

# Check code quality
black --check .
flake8 .
mypy agent_framework
```

## Verification

### Verify Base Installation

```python
# test_install.py
from agent_framework import AgentInterface, create_basic_agent_server

print("✓ Base framework installed successfully")
```

```bash
python test_install.py
```

### Verify LlamaIndex Installation

```python
# test_llamaindex.py
from agent_framework import LlamaIndexAgent
from llama_index.core.tools import FunctionTool

class TestAgent(LlamaIndexAgent):
    def get_agent_prompt(self) -> str:
        return "Test agent"
    
    def get_agent_tools(self) -> list:
        return []

print("✓ LlamaIndex support installed successfully")
```

```bash
python test_llamaindex.py
```

### Verify Microsoft Installation

```python
# test_microsoft.py
from agent_framework import MicrosoftAgent

print("✓ Microsoft Agent Framework support installed successfully")
```

```bash
python test_microsoft.py
```

### Verify Server

```python
# test_server.py
from agent_framework import LlamaIndexAgent, create_basic_agent_server

class SimpleAgent(LlamaIndexAgent):
    def get_agent_prompt(self) -> str:
        return "I am a test agent"
    
    def get_agent_tools(self) -> list:
        return []

if __name__ == "__main__":
    print("Starting test server on http://localhost:8000")
    print("Visit http://localhost:8000/ui to test")
    create_basic_agent_server(SimpleAgent, port=8000)
```

```bash
python test_server.py
```

Then visit:
- Web UI: http://localhost:8000/ui
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## System Dependencies

### PDF Processing (Optional)

The framework automatically detects and configures PDF tools if they're installed. For better PDF processing support:

**macOS:**
```bash
brew install poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**Fedora/RHEL:**
```bash
sudo dnf install poppler-utils
```

**Note:** The framework will automatically find and configure these tools. No manual PATH configuration needed!

### Playwright Browsers

After installing the framework, install Playwright browsers:

```bash
playwright install chromium
```

**Alternative:** Run the post-install script manually:
```bash
python -m scripts.post_install
```

### Quick Environment Setup (Development)

For development, you can use the activation script to verify your environment:

```bash
# Make executable
chmod +x activate_tools.sh

# Source it
source activate_tools.sh
```

This will check for all required tools and provide installation instructions if anything is missing.

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem:**
```python
ImportError: cannot import name 'LlamaIndexAgent' from 'agent_framework'
```

**Solution:**
```bash
# Install with LlamaIndex support
uv add agent-framework-lib[llamaindex]
```

#### 2. Missing API Keys

**Problem:**
```
ValueError: No API key configured for OpenAI
```

**Solution:**
```bash
# Add to .env file
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# Or set environment variable
export OPENAI_API_KEY=sk-your-key-here
```

#### 3. Port Already in Use

**Problem:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```python
# Use a different port
create_basic_agent_server(MyAgent, port=8001)

# Or kill the process using the port
# On Unix/Mac:
lsof -ti:8000 | xargs kill -9

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### 4. Module Not Found

**Problem:**
```
ModuleNotFoundError: No module named 'llama_index'
```

**Solution:**
```bash
# Reinstall with correct extras
pip uninstall agent-framework-lib
uv add agent-framework-lib[llamaindex]
```

#### 5. Permission Errors

**Problem:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Use user installation
uv add --user agent-framework-lib

# Or use virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate
uv add agent-framework-lib
```

### Platform-Specific Issues

#### macOS

**Issue:** SSL Certificate Errors

```bash
# Install certificates
/Applications/Python\ 3.x/Install\ Certificates.command
```

**Issue:** Command Line Tools

```bash
# Install Xcode Command Line Tools
xcode-select --install
```

#### Windows

**Issue:** Long Path Support

```powershell
# Enable long paths in Windows
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

**Issue:** Visual C++ Build Tools

Download and install from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

#### Linux

**Issue:** Missing System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev build-essential

# CentOS/RHEL
sudo yum install python3-devel gcc gcc-c++

# Arch Linux
sudo pacman -S python base-devel
```

### Getting Help

If you're still having issues:

1. **Check the logs**: Look for error messages in the console output
2. **Verify Python version**: Ensure you're using Python 3.8 or higher
3. **Check dependencies**: Run `pip list` to see installed packages
4. **Search issues**: Check GitHub issues for similar problems
5. **Ask for help**: Open a new issue with:
   - Your Python version (`python --version`)
   - Your OS and version
   - Complete error message
   - Steps to reproduce

## Next Steps

Now that you have the framework installed:

1. **Create Your First Agent**: Follow the [Creating Agents Guide](creating-agents.md)
2. **Explore Examples**: Check out the [examples/](../examples/) directory
3. **Read the Docs**: Review the [API Reference](api-reference.md)
4. **Join the Community**: Connect with other developers

### Quick Start Examples

**Simple Calculator Agent:**
```bash
# Create a new file: calculator_agent.py
cat > calculator_agent.py << 'EOF'
from agent_framework import LlamaIndexAgent, create_basic_agent_server
from llama_index.core.tools import FunctionTool

class CalculatorAgent(LlamaIndexAgent):
    def get_agent_prompt(self) -> str:
        return "You are a helpful calculator."
    
    def get_agent_tools(self) -> list:
        def add(a: float, b: float) -> float:
            """Add two numbers."""
            return a + b
        
        return [FunctionTool.from_defaults(fn=add)]

if __name__ == "__main__":
    create_basic_agent_server(CalculatorAgent, port=8000)
EOF

# Run it
python calculator_agent.py
```

Visit http://localhost:8000/ui and try: "What is 5 + 3?"

### Learning Resources

- **[Creating Agents Guide](creating-agents.md)** - Comprehensive agent development guide
- **[Architecture](../ARCHITECTURE.md)** - Understanding the framework architecture
- **[API Reference](api-reference.md)** - Complete API documentation
- **[Testing Guide](UV_TESTING_GUIDE.md)** - Testing best practices
- **[Examples](../examples/)** - Real-world agent examples

## Version Compatibility

| Framework Version | Python Version | LlamaIndex Version | Microsoft Version |
|------------------|----------------|-------------------|-------------------|
| 0.3.x | 3.8+ | 0.10.x+ | Latest |

## Upgrading

```bash
# Upgrade the package
uv add --upgrade agent-framework-lib[llamaindex]

# Or with pip
uv add --upgrade agent-framework-lib[llamaindex]
```

See [CHANGELOG.md](../CHANGELOG.md) for detailed upgrade instructions and breaking changes.

## Support

- **Documentation**: https://agent-framework.readthedocs.io
- **GitHub**: https://github.com/your-org/agent-framework
- **Issues**: https://github.com/your-org/agent-framework/issues
- **Discussions**: https://github.com/your-org/agent-framework/discussions

---

**Ready to build your first agent?** Continue to the [Creating Agents Guide](creating-agents.md)!
