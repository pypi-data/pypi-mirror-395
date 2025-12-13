<div align="center">
  <h1><b>Buchi CLI</b></h1>
  <p><b>The Safety-First Autonomous AI Coding Agent.</b></p>
</div>

<div align="center">
  <img src="./static/buchi-char.png" alt="Buchi CLI Logo" width="300">
</div>

**Buchi** is a command-line agent that acts as your autonomous pair programmer. It plans tasks, writes code, and manages files using an agentic workflow (LangGraph).

Unlike "autocomplete" tools, Buchi can handle complex instructions like "Refactor the login logic and add tests." Because this requires high-level reasoning, **Buchi is designed to ensure safety** even when the AI makes mistakes.


## Main Commands

### `buchi run` - Execute AI Coding Tasks

```bash
# Basic usage
buchi run "Create a login endpoint"

# Specify model
buchi run "Add tests" --model qwen3-coder:480b-cloud

# Set working directory
buchi run "Refactor code" --dir ./my-project

# Verbose mode (show detailed logs)
buchi run "Create API" --verbose

# Control max iterations (prevent runaway loops)
buchi run "Build project" --max-iterations 75
```

### Options:
`-m, --model` - Ollama model to use (default: qwen3-coder:480b-cloud)

`-d, --dir` - Working directory (default: current directory)

`-v, --verbose` - Show detailed execution logs

`--max-iterations` - Maximum agent iterations (default: 50)

## History Management

### `buchi history` - View Conversation History

```bash
# Show last 10 messages (default)
buchi history

# Show last 5 messages
buchi history -n 5

# Show all messages
buchi history --full

# For specific project
buchi history --dir ./my-project
```

### `buchi clear` - Clear Conversation History

```bash
# Clear history for current project
buchi clear

# Clear for specific project
buchi clear --dir ./my-project
```

### `buchi limit` - Manage Message Context Limit

```bash
# View current limit
buchi limit

# Set limit to 30 messages
buchi limit 30

# Set unlimited
buchi limit 0

# For specific project
buchi limit 50 --dir ./my-project
```

### `buchi info` - Project Statistics

```bash
# Show conversation statistics
buchi info

# For specific project
buchi info --dir ./my-project
```

### Shows:
- Total Messages

- Message Limit

- First/Last Interaction Dates

- Storage Location


