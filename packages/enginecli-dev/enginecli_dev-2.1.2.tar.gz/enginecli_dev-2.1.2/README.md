# Engine CLI

AI-powered code generation that understands your codebase.

## Installation

```bash
pip install enginecli-dev
```

## Quick Start

```bash
# 1. Index your project
engine index

# 2. Start a free trial (15 generations)
engine license trial you@example.com

# 3. Generate code
engine generate "Add user authentication with JWT"

# 4. Or create a multi-task plan
engine plan "Add a complete REST API for blog posts"
```

## Commands

### Indexing

```bash
# Index current project (auto-detects Python/TypeScript)
engine index

# Force a specific language
engine index --language python
engine index --language typescript
```

### Generation

```bash
# Generate code for a task
engine generate "Add pagination to the users endpoint"

# Focus on specific files
engine generate "Add error handling" --file src/api.py --file src/utils.py

# Dry run (show context without generating)
engine generate "Add caching" --dry-run
```

### Planning

```bash
# Create a multi-task plan
engine plan "Add user authentication with OAuth2"

# Limit number of tasks
engine plan "Refactor the data layer" --max-tasks 5

# Execute plan immediately
engine plan "Add unit tests" --execute
```

### Chat

```bash
# Chat about your codebase
engine chat

# You: What does the UserService class do?
# Engine: The UserService class handles...
```

### License

```bash
# Activate a license
engine license activate ENGINE-PRO-XXXX-XXXX-XXXX

# Start a free trial
engine license trial you@example.com

# Check status
engine license status

# Deactivate (for machine swap)
engine license deactivate
```

### Status

```bash
# Show index and license status
engine status
```

## How It Works

```
┌─────────────────┐         ┌─────────────────┐
│   Your Code     │         │   Engine API    │
│                 │         │                 │
│  engine index   │────────►│  Validates      │
│  (local)        │         │  license        │
│                 │         │                 │
│  Assembles      │────────►│  Generates      │
│  context        │         │  code           │
│  (local)        │         │  (Claude)       │
│                 │◄────────│                 │
│  Applies        │         │  Returns        │
│  changes        │         │  code           │
└─────────────────┘         └─────────────────┘
```

**What runs locally:**
- Code indexing (fast, no network)
- Context assembly (smart selection)
- File writing

**What runs on our server:**
- License validation
- Usage tracking
- LLM calls (prompts hidden)
- Response parsing

## Configuration

```bash
# Set API URL (for self-hosted)
engine config set api_url https://api.mycompany.com

# View all config
engine config list
```

Config file: `~/.engine/config.json`

## Pricing

| Plan | Price | Generations |
|------|-------|-------------|
| Free | $0 | 15/month |
| Pro | $39/month | 200/month |
| Team | $119/month | 500/month (5 seats) |

Start a free trial: `engine license trial you@example.com`

Upgrade at: https://engine.dev/pricing

## Requirements

- Python 3.9+
- Internet connection (for generation)

## Support

- Documentation: https://docs.engine.dev
- Discord: https://discord.gg/engine
- Email: support@engine.dev

## License

Proprietary - All rights reserved
