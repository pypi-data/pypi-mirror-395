# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Army Days is a Python CLI tool that displays countdown/countup information for configurable events. It follows the West Point tradition of "reciting the days" with an optional "and a butt" feature when past noon. The program reads event data from YAML/JSON configuration files and outputs formatted results either as colored terminal output or JSON.

## Development Commands

### Environment Setup
```bash
# Install Python and sync dependencies
uv python install
uv sync
```

### Running the Program
```bash
# Run with default config file search
uv run army-days

# Run with specific config file
uv run army-days -f path/to/config.yaml

# Show past events
uv run army-days --show-past
uv run army-days --show-past 365

# Generate sample configuration
uv run army-days -g > days.yaml
```

### Testing
```bash
# Basic tests with coverage
uv run pytest --cov

# Verbose tests with stdout and coverage
uv run pytest --cov -v -s

# Run a specific test file
uv run pytest tests/test_core.py

# Run a specific test function
uv run pytest tests/test_core.py::test_function_name
```

### Linting and Formatting
The project uses Ruff for linting and formatting (configured in pyproject.toml):
```bash
# Format code
uv run ruff format

# Lint code
uv run ruff check

# Lint and auto-fix
uv run ruff check --fix
```

## Code Architecture

### Module Structure
- `cli.py`: Click-based command-line interface entry point; handles argument parsing, file loading, and error handling
- `core.py`: Core business logic for computing event days and generating default configurations; implements the "army butt days" logic (subtract 0.5 days after noon)
- `models.py`: Pydantic models for configuration and data validation; supports both camelCase (JSON) and snake_case (Python) via field aliases
- `config.py`: Configuration file search paths
- `output.py`: Dual-mode output system - colored ANSI terminal output when stdout is a TTY, JSON output otherwise
- `ansi_text/`: ANSI escape code utilities for terminal color formatting
- `utils/`: Utility functions including config file discovery

### Data Flow
1. CLI parses arguments and locates config file (search order: `./days.yaml`, `./days.json`, `~/days.yaml`, `~/days.json`, `~/.days.yaml`, `~/.days.json`)
2. Config file is loaded and validated via Pydantic models (DaysModel)
3. `compute_results()` processes each entry, calculating time deltas and applying display rules (future events, past event filters, always_show flags)
4. Events are sorted by date
5. Output module detects TTY and formats accordingly (colored ANSI or JSON)

### Key Logic: Past Event Display
Past events are shown based on three independent conditions (any can trigger display):
- Global config: `show_completed: true` in config section
- CLI parameter: `--show-past` flag (optionally with day limit)
- Per-event: `alwaysShow: true` with optional `showPastLimit` in entry

### Configuration File Format
YAML/JSON with two main sections:
- `config`: Global settings (`use_army_butt_days`, `show_completed`)
- `entries`: Array of events with `title`, `date`, and optional `alwaysShow`/`showPastLimit` fields

Field aliases support both camelCase and snake_case (e.g., `use_army_butt_days` or `useArmyButtDays`).

## Testing Strategy

Tests use freezegun to mock datetime for deterministic testing of date calculations. Test files mirror source structure:
- `test_core.py`: Tests for compute_results logic and default config generation
- `test_models.py`: Pydantic model validation tests
- `test_output.py`: Output formatting tests

## Dependencies

Core dependencies:
- **click**: CLI framework
- **pydantic**: Data validation and settings management
- **pyyaml**: YAML parsing

Dev dependencies:
- **pytest** + **pytest-cov**: Testing and coverage
- **freezegun**: Time mocking for tests
