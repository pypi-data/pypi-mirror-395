# Groqqy 🤖

**Clean, composable micro agentic bot powered by Groq**

Ultra-fast, ultra-cheap, and truly agentic. Groqqy is a multi-step reasoning agent that reads files, runs commands, searches content, and chains tool calls to complete complex tasks—all with production-ready code that's perfect for learning.

## Why Groqqy?

- ⚡ **Blazing Fast**: 460+ tokens/sec (11x faster than standard inference)
- 💰 **Ultra Cheap**: $0.00002-$0.00006 per interaction (300x cheaper than GPT-4)
- 🧠 **Truly Agentic**: Multi-step reasoning loop (THINK → ACT → OBSERVE)
- 🛠️ **Tool-Capable**: Execute local and platform tools with automatic chaining
- 🧩 **Composable**: Mix and match components (Agent, Tools, Strategies, etc.)
- 📚 **Teaching-Friendly**: Clean, readable code (<200 lines per file) perfect for learning agentic AI
- 📝 **Export Ready**: Save conversations to markdown/HTML with full tool call visibility

## What's New in v2.2.2

**Pure LLM Mode & Code Quality:**

- 🚫 **Disable Tools**: New `tools=None` parameter for pure text generation without tool-calling overhead
- 🔒 **Security Fixes**: Replaced bare except clauses with specific exception handling
- 📏 **PEP 8 Compliance**: All core modules now pass linting with zero issues
- ✅ **Comprehensive Testing**: 20/20 tests passing including new --no-tools test suite
- 📝 **Complete Documentation**: README and CHANGELOG fully updated

**Previous Features (v2.1.0):**

- 📝 **Conversation Export**: Export full conversations to markdown/HTML with tool call details
- 🎓 **Self-Discovery**: Agents can autonomously learn new tools via minimal seed prompts
- 🧪 **Container Testing**: Reproducible testing infrastructure with Podman
- 📚 **Documentation Reorganization**: Clean structure with guides and examples
- 🧹 **Project Cleanup**: Professional structure, organized tests, comprehensive examples

See [CHANGELOG.md](CHANGELOG.md) for full history.

## Installation

```bash
# Clone the repository
git clone https://github.com/scottsen/groqqy.git
cd groqqy

# Install in development mode (recommended)
pip install -e .

# Or install directly
pip install .
```

**Requirements:** Python 3.8+ and a Groq API key (free at [console.groq.com](https://console.groq.com))

**Setup:**
```bash
export GROQ_API_KEY="your-api-key-here"
```

## Quick Start

### Interactive Chat

```bash
groqqy
```

```
Groqqy 🤖 (llama-3.1-8b-instant)
Type 'help' for commands, 'exit' to quit

You: Find all Python files in the current directory
Groqqy: I'll search for Python files...
        [Searches, finds files, reports results]

You: Read the first one and summarize it
Groqqy: [Reads file, provides summary]

You: export markdown my_session.md
✅ Conversation exported to my_session.md
```

### Programmatic Use

```python
from groqqy import Groqqy

# Create bot
bot = Groqqy()

# Simple chat
response, cost = bot.chat("Hello! What can you do?")
print(response)
print(f"Cost: ${cost:.6f}")

# Agentic task (agent chains tools automatically)
response, cost = bot.chat("Find all .py files and count lines in each")
print(response)
# Agent will: search_files("*.py") → read_file(each) → count → report

# Export conversation
bot.save_conversation("session.html")  # Auto-styled HTML
bot.save_conversation("session.md")     # Clean markdown
```

## Model Selection for Tool Calling

When using Groqqy for agentic workflows with tool calling, **model selection matters**:

### Recommended Models (2025)

| Model | Tool Calling | Speed | Cost | Recommendation |
|-------|--------------|-------|------|----------------|
| **llama-3.3-70b-versatile** | ✅ Excellent | Fast | $0.001/query | **Best for production** |
| **llama-4-scout** | ✅ Excellent | Fast | $0.0004/query | Optimized for tool use |
| **llama-3.1-8b-instant** | ⚠️ Inconsistent | Fastest | $0.0003/query | Testing only |

### Known Issue: `tool_use_failed` Errors

**Symptom**: `RuntimeError: Groq API error (400): tool_use_failed`

**Cause**: Some models (especially 8b) occasionally generate tool calls wrapped in XML tags (`<function=name>{...}</function>`) instead of pure JSON. Groq's API rejects this format.

**Solution**: Use `llama-3.3-70b-versatile` for production tool calling:

```python
from groqqy import Groqqy

# Recommended for production
bot = Groqqy(model="llama-3.3-70b-versatile")

# Cheaper but less reliable
bot = Groqqy(model="llama-3.1-8b-instant")  # May fail on tool calls
```

**Cost trade-off**: 70b model costs ~3x more ($0.001 vs $0.0003 per query) but provides consistent tool calling. **Still 100x cheaper than Claude.**

**See also**: [Groq Tool Use Documentation](https://console.groq.com/docs/tool-use) | [Supported Models](https://console.groq.com/docs/models)

### Custom Tools

```python
from groqqy import Groqqy

def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # Your implementation
    return f"Weather in {city}: Sunny, 72°F"

def calculate_tip(bill: float, percent: float = 15.0) -> str:
    """Calculate tip amount for a bill."""
    tip = bill * (percent / 100)
    return f"Tip: ${tip:.2f}, Total: ${bill + tip:.2f}"

# Just pass functions - auto-registration!
bot = Groqqy(tools=[get_weather, calculate_tip])

response, cost = bot.chat("What's the weather in San Francisco?")
# Agent automatically calls get_weather("San Francisco")
```

### Pure LLM Mode (No Tools)

Sometimes you want pure text generation without any tool-calling:

```python
from groqqy import Groqqy

# Disable tools entirely for pure LLM mode
bot = Groqqy(tools=None)

# Fast, focused text generation (no tool overhead)
response, cost = bot.chat("Write a haiku about coding")
# Agent generates text directly, no tool calls attempted
```

**When to use `tools=None`:**
- Pure text generation (summaries, creative writing, etc.)
- Fact extraction from existing data
- Scenarios where tool-calling causes problems (loops, hallucinations)
- Faster generation with smaller models (no tool overhead)

**Example use case - Fact extraction:**
```python
# Extract structured information without tools
bot = Groqqy(model="llama-3.1-8b-instant", tools=None)

data = """
Session: test-123
Files: app.py, test.py
Errors: 5 type errors, 2 lint warnings
"""

response, cost = bot.chat(f"Extract facts from this data:\n{data}")
# Clean output, no tool calls, 3x faster
```

**Note**: Omitting the `tools` parameter creates default tools (backwards compatible). Use `tools=None` explicitly to disable.

## Core Features

### 🧠 Agentic Loop

Groqqy implements the **ReAct pattern** (Reasoning + Acting) for true multi-step problem solving:

```
User: "Find Python files and count their lines"
     ↓
┌────────────────┐
│ THINK (LLM)    │  "I need to search for .py files first"
└────────┬───────┘
         ↓
┌────────────────┐
│ ACT (Tool)     │  execute: search_files("*.py")
└────────┬───────┘
         ↓
┌────────────────┐
│ OBSERVE        │  "Found: app.py, test.py, utils.py"
└────────┬───────┘
         ↓
┌────────────────┐
│ THINK (LLM)    │  "Now read each file and count lines"
└────────┬───────┘
         ↓
┌────────────────┐
│ ACT (Tools)    │  execute: read_file("app.py"), read_file("test.py")...
└────────┬───────┘
         ↓
     [Response]
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for deep dive.

### 🛠️ Built-in Tools

- `read_file(file_path)` - Read file contents
- `run_command(command)` - Execute shell commands (secure with shlex)
- `search_files(pattern, path)` - Find files by glob pattern
- `search_content(query, path)` - Search text in files (ripgrep)

### 🌐 Platform Tools (v2.0+)

Execute tools on Groq's servers (e.g., web search):

```python
from groqqy import Groqqy, ToolRegistry

registry = ToolRegistry()
registry.register_platform_tool("browser_search")

bot = Groqqy(model="llama-3.3-70b-versatile", tools=registry)

response, cost = bot.chat(
    "What are the latest AI developments this week?"
)
# Agent uses browser_search to get current web information
```

### 📝 Conversation Export

Export full conversations with tool calls and results:

```python
# During a session
bot.chat("Calculate the weather in NYC")
bot.chat("What's 15% tip on $87.50?")

# Export to markdown
bot.save_conversation("session.md")

# Export to styled HTML
bot.save_conversation("session.html")
```

**CLI auto-export:**
```bash
groqqy --export my_session.html
```

**Interactive export:**
```
You: export markdown conversation.md
✅ Conversation exported to conversation.md
```

Exports include:
- All user messages
- All assistant responses
- All tool calls with JSON arguments
- All tool results
- Timestamps and metadata

Perfect for documentation, debugging, or sharing agent behavior.

### 🎯 Strategy Pattern

Automatic tool execution strategy selection:
- **LocalToolStrategy**: Execute tools in your environment
- **PlatformToolStrategy**: Execute on Groq's servers (browser_search, etc.)
- **HybridToolStrategy**: Mix local and platform tools intelligently

No configuration needed—strategies auto-detect based on tool types.

## Examples

Check out the [`examples/`](examples/) directory:

- **basic_chat.py** - Simple conversation
- **custom_tools.py** - Adding custom tools with decorator pattern
- **tool_usage.py** - Tool calling and chaining
- **export_conversation.py** - Exporting to markdown/HTML
- **example_web_search.py** - Using platform tools for web access
- **reveal_mvp_demo.py** - Self-discovery pattern with reveal-cli
- **self_discovery_demo.py** - Autonomous tool learning

Run any example:
```bash
python examples/basic_chat.py
```

## Documentation

- **[docs/USER_GUIDE.md](docs/USER_GUIDE.md)** - Comprehensive usage guide
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Deep dive into design and components
- **[docs/TEACHING_GUIDE.md](docs/TEACHING_GUIDE.md)** - Using Groqqy to learn/teach agentic AI
- **[docs/guides/](docs/guides/)** - Feature-specific guides and tutorials
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Developer setup and workflow

## Architecture

Groqqy is built with clean, composable components:

```
groqqy/
├── bot.py              # Simple facade (Groqqy class)
├── agent.py            # Agentic loop (THINK/ACT/OBSERVE)
├── strategy.py         # Tool execution strategies
├── tool.py             # Tool registry system
├── tools.py            # Built-in tools
├── components/
│   ├── conversation.py # Message history
│   ├── executor.py     # Tool execution
│   ├── exporter.py     # Conversation export
│   └── tracker.py      # Cost tracking
└── providers/
    └── groq.py         # Groq API integration
```

**Design Principles:**
- All files <365 lines (most <200)
- Single responsibility per component
- Easy to read, understand, and modify
- Production-ready patterns (logging, error handling, cost tracking)

## Teaching & Learning

Groqqy is designed as a **teaching kernel for agentic AI**. Unlike production frameworks (LangChain, LangGraph) with 50,000+ lines of code, Groqqy is:

- ✅ **~1,500 lines** for complete agentic loop
- ✅ **88-line core algorithm** - read and understand in 5 minutes
- ✅ **Explicit patterns** - THINK/ACT/OBSERVE labeled in code
- ✅ **Production-ready** - not toy code, real patterns
- ✅ **Pedagogical** - designed for learning then extending

**Perfect for:**
- Computer science courses on AI agents
- Self-learners exploring agentic patterns
- Developers understanding agents before using frameworks
- Workshops and tutorials on tool-calling LLMs

See [docs/TEACHING_GUIDE.md](docs/TEACHING_GUIDE.md) for lesson plans and learning paths.

## Cost Examples

Real costs from actual usage:

| Task | Cost |
|------|------|
| Simple conversation | $0.000022 |
| Search files | $0.000028 |
| Run command | $0.000032 |
| Multi-step task (3 tools) | ~$0.000120 |
| **1,000 interactions** | **~$0.03-$0.12** |

Compare to GPT-4: ~$10-$100 for 1,000 interactions (300x more expensive)

## Testing

```bash
# Run all tests
pytest

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/examples/

# Run with coverage
pytest --cov=groqqy

# Container testing (reproducible environment)
./container_test.sh
```

## Configuration

Groqqy supports persistent configuration via `~/.groqqy/`:

```bash
~/.groqqy/
├── boot.md              # System instructions loaded on startup
└── knowledge/           # Additional context files
    └── domain_info.md
```

**CLI options:**
```bash
groqqy                              # Interactive with boot.md
groqqy --prompt "What's 2+2?"       # Single-shot
groqqy --model llama-3.3-70b-versatile  # Custom model
groqqy --export chat.html           # Auto-export on exit
groqqy --no-boot                    # Skip boot.md
```

## Models

Groqqy supports all Groq models:

```python
# Fast and cheap (default)
bot = Groqqy(model="llama-3.1-8b-instant")

# Fastest (460+ tok/sec)
bot = Groqqy(model="llama-4-scout")

# Best quality
bot = Groqqy(model="llama-3.3-70b-versatile")

# Mixture of experts
bot = Groqqy(model="mixtral-8x7b-32768")

# Platform tools (required for browser_search)
bot = Groqqy(model="llama-3.3-70b-versatile")  # or openai/gpt-oss-20b
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick start for contributors:**
```bash
# Clone and install
git clone https://github.com/scottsen/groqqy.git
cd groqqy
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black groqqy/ tests/

# Type check
mypy groqqy/
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Related Projects

- [Groq API Docs](https://console.groq.com/docs) - Groq's LPU inference
- [ReAct Paper](https://arxiv.org/abs/2210.03629) - Reasoning + Acting framework (Yao et al., 2022)
- [LangChain](https://python.langchain.com/) - Production agentic framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Graph-based agents

## Support & Community

- **Issues**: [GitHub Issues](https://github.com/scottsen/groqqy/issues)
- **Discussions**: [GitHub Discussions](https://github.com/scottsen/groqqy/discussions)
- **Examples**: Check [`examples/`](examples/) directory

---

**Built with ❤️ using Groq's blazing-fast LPU inference**

**Perfect for:** Learning agentic AI • Rapid prototyping • Cost-conscious automation • Teaching AI agents • Building proof-of-concepts
