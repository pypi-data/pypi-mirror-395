# Meld CLI

Command-line interface for the Meld personal memory system.

## Installation

```bash
pip install meld-memory
```

## Usage

### Login

```bash
# Request magic link
meld login
# Enter your email: you@example.com
# Check your email for a login link!

# After clicking the link, you're logged in
meld status
# ✓ Logged in as: you@example.com
# ✓ API: Connected
```

### Setup Claude Code

```bash
meld setup
# ✓ Found Claude Code
# ✓ Updated Claude Code settings
# ✓ Added session hook
#
# Setup complete! Restart Claude Code to activate Meld.
```

### Other Commands

```bash
# Check status
meld status

# Show current user
meld whoami

# Logout
meld logout
```

## How It Works

1. `meld login` sends a magic link to your email
2. Click the link to authenticate
3. Token is saved to `~/.meld/credentials.json`
4. `meld setup` configures Claude Code to use the Meld MCP server
5. On next Claude Code session, Meld greets you and offers check-ins

