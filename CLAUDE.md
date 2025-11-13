# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important Guidelines

**NEVER install anything globally.** Always use project-local installations via `uv add --dev` or other project-scoped methods. Do not use `uv tool install` or any global installation commands.

## Project Overview

This is a Snake game implementation using pygame. The entire game is contained in a single file (`main.py`) with a class-based architecture.

## Development Commands

**Running the game:**
```bash
uv run python main.py
```

**Installing dependencies:**
```bash
uv sync
```

## Code Architecture

The game uses a single `SnakeGame` class that handles all game logic, rendering, and input:

- **Game loop**: Located in `SnakeGame.run()` - handles input, update, and draw cycle at 10 FPS
- **State management**: Snake position stored as list of (x, y) tuples with head at index 0
- **Direction handling**: Uses `Direction` enum and separates current direction from next direction to prevent invalid 180-degree turns
- **Collision detection**: Checks for wall boundaries and self-collision in `update()` method
- **Food spawning**: Ensures food never spawns on snake body segments

The game uses a grid-based coordinate system (40x30 grid with 20px cell size) rather than pixel-perfect positioning.
