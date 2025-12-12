# GitGotchi - Your Friendly Dev Companion

A Stardew Valley-inspired terminal companion that lives in your git repository!

## Features

- Adorable pixel art companion that evolves based on your coding habits
- Warm, encouraging stories about your code history
- Automatic feeding through git hooks
- Friendship system inspired by Stardew Valley
- Cozy terminal UI with beautiful colors
- Fast evolution - see changes every 2-3 commits!

## Installation

```bash
pip install gitgotchi
```

## Quick Start

```bash
# Navigate to any git repository
cd your-project

# Install git hooks for automatic feeding
gitgotchi install

# Meet your companion!
gitgotchi status
```

## Commands

- `gitgotchi status` - See your companion's current state
- `gitgotchi pet` - Give them affection (boosts mood)
- `gitgotchi story` - Hear an AI-generated story about your code
- `gitgotchi evolve` - Check evolution progress and requirements
- `gitgotchi name <name>` - Give your companion a custom name
- `gitgotchi install` - Install git hooks for automatic feeding
- `gitgotchi uninstall` - Remove git hooks

## Evolution Forms

Your companion evolves based on commit count and code quality:

- **Egg** (0-2 commits) - Starting form
- **Ghost** (3-5 commits) - Default evolution path
- **Angel** (6+ commits, quality > 70) - High quality code path
- **Demon** (6+ commits, quality < 30) - Chaotic but playful path
- **Zombie** (4+ reverts) - Needs coffee, sleepy form
- **Wraith** (15+ commits) - Ultimate ethereal form

## Code Quality Factors

- Descriptive commit messages (+15 points)
- Reasonable commit size (+5 points)
- Including tests (+10 points)
- Vague messages like "fix" (-20 points)
- Huge commits >500 lines (-15 points)

## Configuration

Set your Anthropic API key for story generation (optional):

```bash
export ANTHROPIC_API_KEY='your-key-here'
# or create a .env file
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

## Requirements

- Python 3.10 or higher
- Git installed and configured
- A git repository (run `git init` if needed)


## License

MIT License - see LICENSE file for details.