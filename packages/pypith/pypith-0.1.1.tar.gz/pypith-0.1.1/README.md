# pypith

Decorator-based library for building agent-native Python CLIs with progressive discovery.

- Define commands with `@app.command()` and attach intents and hints
- Auto-generated `pith` discovery subcommand with tiers 0-3
- Built-in core schema, rendering, and optional semantic search
- Schema export compatible with `pypith-cli`

## Installation

```bash
pip install pypith

# With semantic search support
pip install pypith[semantic]
```

## Quick Start

```python
from pith import Pith, Argument, Option
from pathlib import Path

app = Pith(name="fileops", pith="File manipulation utilities")

@app.command()
@app.intents("copy files", "duplicate", "backup files")
def copy(
    src: Path = Argument(..., pith="Source file or directory"),
    dest: Path = Argument(..., pith="Destination path"),
    recursive: bool = Option(False, "-r", "--recursive", pith="Copy directories recursively"),
):
    """Copy files or directories to a destination."""
    import shutil
    if src.is_dir() and recursive:
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)

if __name__ == "__main__":
    app.run()
```

## Core Module

The library includes the core schema and rendering utilities:

```python
from pith.core import PithSchema, Command, Tier1, Tier2, Tier3
from pith.core import render_tier0, build_run_line, search_commands
```
