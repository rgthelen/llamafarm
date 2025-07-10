# 🌾 LLaMA Farm CLI

Deploy AI models, agents, and databases into single deployable binaries - no cloud required.

## Installation

```bash
npm install -g @llamafarm/llamafarm
```

## Quick Start

```bash
# Deploy a model
llamafarm plant llama3-8b

# Deploy with optimization
llamafarm plant llama3-8b --optimize

# Deploy to specific target
llamafarm plant mistral-7b --target raspberry-pi
```

## Features

- 🎯 **One-Line Deployment** - Deploy complex AI models with a single command
- 📦 **Zero Dependencies** - Compiled binaries run anywhere
- 🔒 **100% Private** - Your data never leaves your device
- ⚡ **Lightning Fast** - 10x faster than traditional deployments
- 💾 **90% Smaller** - Optimized models use fraction of original size

## Commands

### `plant`
Deploy a model to create a standalone binary.

```bash
llamafarm plant <model> [options]

Options:
  --target <platform>    Target platform (mac, linux, windows, raspberry-pi)
  --optimize            Enable size optimization
  --agent <name>        Include an agent
  --rag                 Enable RAG pipeline
  --database <type>     Include database (vector, sqlite)
```

### Examples

```bash
# Basic deployment
llamafarm plant llama3-8b

# Deploy with RAG and vector database
llamafarm plant mixtral-8x7b --rag --database vector

# Deploy optimized for Raspberry Pi
llamafarm plant llama3-8b --target raspberry-pi --optimize

# Deploy with custom agent
llamafarm plant llama3-8b --agent customer-service
```

## Configuration

Create a `llamafarm.yaml` file for advanced configurations:

```yaml
name: my-assistant
base_model: llama3-8b
plugins:
  - vector_search
  - voice_recognition
data:
  - path: ./company-docs
    type: knowledge
optimization:
  quantization: int8
  target_size: 2GB
```

Then build:
```bash
llamafarm build
```

## Requirements

- Node.js 18+ 
- 8GB RAM (minimum)
- 10GB free disk space

## Documentation

For full documentation, visit [https://docs.llamafarm.ai](https://docs.llamafarm.ai)

## Support

- 📖 [Documentation](https://docs.llamafarm.ai)
- 💬 [Discord Community](https://discord.gg/llamafarm-ai)
- 🐛 [Issue Tracker](https://github.com/llamafarm-ai/llamafarm/issues)

## License

MIT © LLaMA Farm Team 