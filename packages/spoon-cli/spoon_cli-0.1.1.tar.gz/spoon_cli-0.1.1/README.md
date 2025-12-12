# spoon-cli

SpoonAI command-line interface for building and running AI agents with MCP (Model Context Protocol) support. Provides rich functionality including AI agent interaction, chat history management, cryptocurrency operations, and document loading.

## Installation

### From PyPI (Recommended)

```bash
pip install spoon-cli
```

### From Source (Development)

1. Clone the repository and navigate to the CLI directory:

```bash
git clone <repository-url>
cd spoon-cli
```

2. Install in editable mode:

```bash
pip install -e .
```

## Configuration

The spoon-cli uses a unified configuration system that supports multiple configuration sources with the following priority order (highest to lowest):

1. **Command-line arguments**
2. **Environment variables**
3. **JSON configuration file** (`config.json`)
4. **Default values**

### Configuration File Setup

Create a `config.json` file in your project root or home directory:

```json
{
  "agents": {
    "my_agent": {
      "class_name": "SpoonReactAI",
      "description": "My custom agent",
      "aliases": ["ma"],
      "config": {
        "llm_provider": "openai",
        "model_name": "gpt-4.1",
        "temperature": 0.7
      },
      "tools": [
        {
          "name": "tavily_search",
          "type": "mcp",
          "mcp_server": {
            "command": "npx",
            "args": ["-y", "tavily-mcp"],
            "env": {
              "TAVILY_API_KEY": "your-tavily-api-key"
            }
          }
        },
        {
          "name": "crypto_powerdata_cex",
          "type": "builtin"
        },
        "calculator"
      ]
    }
  },
  "default_agent": "my_agent",
  "api_keys": {
    "openai": "sk-your-openai-key-here",
    "anthropic": "sk-ant-your-anthropic-key-here"
  },
  "mcp_servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/workspace"]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "/path/to/git/repo"]
    }
  }
}
```

### Environment Variables

Set required API keys before starting:

```bash
# Required for web search (Tavily MCP)
export TAVILY_API_KEY="your-tavily-api-key"

# Required for LLM functionality
export OPENAI_API_KEY="your-openai-api-key"

# Optional: Additional LLM providers
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export DEEPSEEK_API_KEY="your-deepseek-key"
export GEMINI_API_KEY="your-gemini-key"

# Optional: Blockchain operations
export PRIVATE_KEY="your-wallet-private-key"
export RPC_URL="https://mainnet.infura.io/v3/YOUR_PROJECT_ID"
export CHAIN_ID="1"

# Optional: Debug mode
export DEBUG=true
export LOG_LEVEL=debug

# Optional: Social media integration
export TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
```

### Configuration Commands

The CLI provides built-in commands to manage configuration:

```bash
# Show current configuration
spoon-cli config

# Get specific configuration value
spoon-cli config api_keys.openai

# Set configuration value
spoon-cli config api_keys.openai "sk-your-key"

# Set API key (shorthand)
spoon-cli config api_key openai "sk-your-key"

# Reload configuration
spoon-cli reload-config

# Validate configuration
spoon-cli validate-config

# Check configuration migration status
spoon-cli check-config

# Migrate legacy configuration
spoon-cli migrate-config
```

### MCP Server Configuration

Configure MCP servers for extended tool capabilities. SpoonOS supports stdio and URL-based (SSE/WebSocket) MCP servers.

| Method | Use Case | Configuration Example |
|--------|----------|----------------------|
| `npx` | Node.js packages | `"command": "npx", "args": ["-y", "package-name"]` |
| `python` | Python scripts | `"command": "python", "args": ["server.py"]` |
| `uvx` | uvx-installed CLIs | `"command": "uvx", "args": ["package-or-entrypoint"]` |
| `http` | HTTP/HTTPS | `"url": "https://example.com/mcp", "transport": "http"` |
| `sse` | HTTP/HTTPS SSE | `"url": "https://example.com/mcp", "transport": "sse"` |

```json
{
  "mcp_servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/Documents"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"
      }
    },
    "tavily": {
      "command": "npx",
      "args": ["-y", "tavily-mcp"],
      "env": {
        "TAVILY_API_KEY": "your-tavily-api-key"
      }
    }
  }
}
```

#### MCP-Enabled Agent Example

```json
{
  "agents": {
    "search_agent": {
      "class": "SpoonReactMCP",
      "description": "Search agent with web search capabilities",
      "aliases": ["search", "web"],
      "tools": [
        {
          "name": "tavily_search",
          "type": "mcp",
          "description": "Web search using Tavily API",
          "mcp_server": {
            "command": "npx",
            "args": ["-y", "tavily-mcp"],
            "env": {
              "TAVILY_API_KEY": "your-tavily-api-key"
            }
          }
        },
        {
          "name": "crypto_powerdata_cex",
          "type": "builtin",
          "description": "Cryptocurrency market data from centralized exchanges"
        }
      ]
    }
  }
}
```

## Usage

### Quick Start

```bash
# Start interactive CLI
spoon-cli

# Or for development
python -m spoon_cli
```

### Available Agents

The CLI includes these built-in agents:

| Agent | Aliases | Type | MCP Support | Description |
|-------|---------|------|-------------|-------------|
| `react` | `spoon_react` | SpoonReactAI | ❌ | Standard blockchain analysis agent |
| `spoon_react_mcp` | - | SpoonReactMCP | ✅ | MCP-enabled blockchain agent |

**Note**: Additional agents can be configured in `config.json`.

### Loading Agents

```bash
# List all available agents
spoon-cli list-agents

# Load built-in agent by name
spoon-cli load-agent react
spoon-cli load-agent spoon_react_mcp

# Load agent by alias
spoon-cli load-agent spoon_react
```

### Basic Usage Examples

```bash
# Start interactive CLI
spoon-cli

# Load specific agent
spoon-cli load-agent react

# Start chat with default agent
spoon-cli action chat
```

### Example: Using Search Agent

After configuring the search agent with Tavily MCP and crypto tools, you can use it for comprehensive market analysis:

```bash
# Load the search agent
spoon-cli load-agent search_agent

# Ask about market analysis combining web search and crypto data
spoon-cli action chat
# Then type: "Analyze the current Bitcoin market sentiment and provide the latest price data from major exchanges"

# Ask about specific cryptocurrency news
# "Search for recent news about Ethereum layer 2 solutions and their market impact"
```

### Available Commands

#### Core Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `help` | `h`, `?` | Display help information |
| `exit` | `quit`, `q` | Exit the CLI |
| `system-info` | `sysinfo`, `status`, `info` | Display comprehensive system information, environment status, and health checks |

#### Agent Management

| Command | Aliases | Description |
|---------|---------|-------------|
| `load-agent <name>` | `load` | Load an agent with the specified name |
| `list-agents` | `agents` | List all available agents |
| `reload-config` | `reload` | Reload the current agent's configuration |

#### Chat Management

| Command | Aliases | Description |
|---------|---------|-------------|
| `action <action>` | `a` | Perform a specific action using the current agent |
| `new-chat` | `new` | Start a new chat (clear history) |
| `list-chats` | `chats` | List available chat history records |
| `load-chat <ID>` | - | Load a specific chat history record |

#### Configuration Management

| Command | Aliases | Description |
|---------|---------|-------------|
| `config` | `cfg`, `settings` | Configure settings (such as API keys) |
| `migrate-config` | `migrate` | Migrate legacy configuration to new unified format |
| `check-config` | `check-migration` | Check if configuration needs migration |
| `validate-config` | `validate` | Validate current configuration and check for issues |

#### LLM Provider Management

| Command | Aliases | Description |
|---------|---------|-------------|
| `list-providers` | `providers` | List all available LLM providers |
| `set-provider <provider>` | `provider` | Set the default LLM provider |
| `test-provider <provider>` | `test` | Test connectivity to a specific provider |
| `llm-status` | `llm` | Show LLM provider configuration and availability |
| `provider-status` | `status` | Show health status of all providers |
| `provider-stats <provider>` | `stats` | Show performance statistics for a provider |
| `config provider <name> <key> <value>` | - | Configure provider-specific settings |

#### Blockchain Operations

| Command | Aliases | Description |
|---------|---------|-------------|
| `transfer <address> <amount> <token>` | `send` | Transfer tokens to a specified address |
| `swap <source_token> <target_token> <amount>` | - | Exchange tokens using an aggregator |
| `token-info <address>` | `token` | Get token information by address |
| `token-by-symbol <symbol>` | `symbol` | Get token information by symbol |

#### Document Management

| Command | Aliases | Description |
|---------|---------|-------------|
| `load-docs <directory_path>` | `docs` | Load documents from the specified directory to the current agent |

#### Toolkit Management

| Command | Aliases | Description |
|---------|---------|-------------|
| `list-toolkit-categories` | `toolkit-categories`, `categories` | List all available toolkit categories |
| `list-toolkit-tools <category>` | `toolkit-tools` | List tools in a specific category |
| `load-toolkit-tools <categories>` | `load-tools` | Load toolkit tools from specified categories |
| `tool-status` | - | Check tool loading status and diagnose issues |

#### Social Integration

| Command | Aliases | Description |
|---------|---------|-------------|
| `telegram` | `tg` | Start the Telegram client |

## LLM Provider Management Examples

### List Available Providers

```bash
spoon-cli list-providers
```

Output:
```
Available LLM providers:
✅ openai (gpt-4.1) - Healthy
✅ anthropic (claude-sonnet-4-20250514) - Healthy
❌ gemini (gemini-2.5-pro) - Unhealthy
Default provider: openai
```

### Switch Default Provider

```bash
spoon-cli set-provider anthropic
# Output: Default LLM provider set to: anthropic
```

### Test Provider Connectivity

```bash
spoon-cli test-provider openai
```

Output:
```
Testing OpenAI provider...
✅ Connection successful
Model: gpt-4.1
Response time: 1.2s
```

### View Provider Statistics

```bash
spoon-cli provider-stats openai
```

Output:
```
OpenAI Provider Statistics:
Total requests: 1,247
Successful requests: 1,198 (96.1%)
Average response time: 2.3s
Rate limit hits: 12
Last error: 2 hours ago
```

### Configure Provider Settings

```bash
# Configure OpenAI model
spoon-cli config provider openai model gpt-4.1

# Configure Anthropic temperature
spoon-cli config provider anthropic temperature 0.7

# Configure OpenAI max tokens
spoon-cli config provider openai max_tokens 8192
```

## Interactive Examples

### Basic Configuration Setup

```bash
# 1. Check current configuration
spoon-cli config

# 2. Set API keys
spoon-cli config api_key openai "sk-your-key-here"
spoon-cli config api_key anthropic "sk-ant-your-key-here"

# 3. View current configuration
spoon-cli config
```

### LLM Provider Management

```bash
# 1. List available providers
spoon-cli list-providers

# 2. Test OpenAI connectivity
spoon-cli test-provider openai

# 3. Switch to Anthropic as default
spoon-cli set-provider anthropic

# 4. View provider statistics
spoon-cli provider-stats anthropic
```

### Agent and Chat Management

```bash
# 1. List available agents
spoon-cli list-agents

# 2. Load React agent
spoon-cli load-agent react

# 3. Start chat session
spoon-cli action chat

# 4. Inside chat, you can interact with the agent
# Type: "Hello, can you help me analyze some cryptocurrency data?"
# Type: "What cryptocurrencies are you familiar with?"
```

### Cryptocurrency Operations

```bash
# 1. Load agent with crypto tools
spoon-cli load-agent react
spoon-cli load-toolkit-tools crypto

# 2. Get token information
spoon-cli token-by-symbol SPO

# 3. Get centralized exchange market data
spoon-cli action chat
# Then type: "Get the latest Bitcoin price and volume data from major CEXs"

# 4. Transfer tokens (requires PRIVATE_KEY)
spoon-cli transfer 0x123... 0.1 SPO

# 5. Swap tokens (requires PRIVATE_KEY)
spoon-cli swap ETH USDC 1.0
```

## Advanced Configuration

### Custom Agent Definition

Define custom agents in your `config.json`:

```json
{
  "agents": {
    "crypto_analyzer": {
      "class_name": "SpoonReactAI",
      "description": "Cryptocurrency analysis agent with web search",
      "config": {
        "llm_provider": "anthropic",
        "model_name": "claude-3-sonnet-20240229",
        "temperature": 0.3,
        "max_tokens": 4000
      },
      "tools": [
        {
          "name": "tavily_search",
          "type": "mcp",
          "mcp_server": {
            "command": "npx",
            "args": ["-y", "tavily-mcp"],
            "env": {
              "TAVILY_API_KEY": "your-tavily-api-key"
            }
          }
        },
        {
          "name": "crypto_powerdata_cex",
          "type": "builtin",
          "description": "Cryptocurrency market data from centralized exchanges"
        }
      ]
    }
  }
}
```

### MCP Integration

Enable MCP servers for enhanced capabilities:

```json
{
  "agents": {
    "mcp_agent": {
      "class_name": "SpoonReactMCP",
      "description": "Agent with MCP protocol support for web search and crypto data",
      "tools": [
        {
          "name": "tavily_search",
          "type": "mcp",
          "mcp_server": {
            "command": "npx",
            "args": ["-y", "tavily-mcp"],
            "env": {
              "TAVILY_API_KEY": "your-tavily-api-key"
            }
          }
        },
        {
          "name": "crypto_powerdata_cex",
          "type": "builtin",
          "description": "Cryptocurrency market data from centralized exchanges"
        }
      ]
    }
  }
}
```

### Environment-Specific Configuration

Use different configurations for different environments:

```json
{
  "development": {
    "agents": { ... },
    "api_keys": { ... }
  },
  "production": {
    "agents": { ... },
    "api_keys": { ... }
  }
}
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install spoon-cli --upgrade
   ```

2. **Configuration Not Found**
   ```bash
   spoon-cli check-config
   spoon-cli migrate-config
   ```

3. **API Key Issues**
   ```bash
   spoon-cli llm-status
   # Set missing keys
   spoon-cli config api_key openai "your-key"
   ```

4. **Tool Loading Problems**
   ```bash
   spoon-cli tool-status
   spoon-cli reload-config
   ```

5. **MCP Server Issues**
   ```bash
   spoon-cli validate-config --check-servers
   ```

### Debug Mode

Enable debug logging:

```bash
export SPOON_CLI_DEBUG=1
spoon-cli
```

### Health Check

Run comprehensive health check:

```bash
spoon-cli system-info
```

## Development

### Setting up Development Environment

```bash
# Clone and setup
git clone <repo-url>
cd spoon-cli

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.