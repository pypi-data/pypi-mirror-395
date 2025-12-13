# Sudoku Telnet Server

[![Test](https://github.com/YOUR_USERNAME/sudoku-telnet-server/workflows/Test/badge.svg)](https://github.com/YOUR_USERNAME/sudoku-telnet-server/actions)
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen)](htmlcov/index.html)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A multi-transport Sudoku game server built using the [chuk-protocol-server](https://github.com/YOUR_USERNAME/chuk-protocol-server) framework.

## Try It Now

A live demo server is running on Fly.io. Try it instantly:

```bash
# Connect via Telnet (IPv6)
telnet 2a09:8280:1::b8:274e:0 8023

# WebSocket connections
ws://sudoku-telnet-server.fly.dev:8025/ws
```

Once connected, type `help` to see available commands, or `start easy` to begin playing!

## Features

- Classic Sudoku gameplay with three difficulty levels (easy, medium, hard)
- Multiple transport protocols:
  - **Telnet** (port 8023) - Classic telnet protocol
  - **TCP** (port 8024) - Raw TCP connections
  - **WebSocket** (port 8025) - Modern WebSocket protocol
  - **WebSocket-Telnet** (port 8026) - WebSocket with telnet negotiation
- Interactive text-based interface
- Hint system for when you're stuck
- Solution checker and auto-solver
- Automatic puzzle generation using backtracking algorithm
- Move tracking and validation
- Comprehensive test suite (50 tests, 94% coverage)
- Modern Python packaging with pyproject.toml
- GitHub Actions CI/CD workflows
- Docker and Fly.io deployment ready

## Game Commands

### Starting and Managing Games
- `start [easy|medium|hard]` - Start a new game (default: easy)
- `show` - Display the current grid
- `help` - Show all available commands
- `quit` - Exit the game

### Playing the Game
- `place <row> <col> <num>` - Place a number on the grid
  - Example: `place 1 5 7` (places 7 at row 1, column 5)
- `clear <row> <col>` - Clear a cell you've filled
- `hint` - Get a hint for the next move
- `check` - Check your progress
- `solve` - Show the solution (ends current game)

## Quick Start

### Prerequisites

- Python 3.11 or higher
- [UV](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

#### From Source (Development)

##### Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/sudoku-telnet-server.git
cd sudoku-telnet-server

# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install development dependencies
make dev-install

# Run the server
make run
```

##### Using pip

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/sudoku-telnet-server.git
cd sudoku-telnet-server

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run the server
PYTHONPATH=. uv run --with chuk-protocol-server chuk-protocol-server server-launcher -c config.yaml
```

#### From PyPI (Production)

```bash
# Install from PyPI (when published)
pip install sudoku-telnet-server

# Run the server using the installed command
sudoku-server

# Or run with custom config
python -m chuk_protocol_server.server_launcher -c /path/to/config.yaml
```

### Using Make (All Commands)

```bash
# See all available commands
make help

# Development workflow
make dev-install      # Install dev dependencies
make run              # Run the server
make test             # Run tests
make test-cov         # Run tests with coverage report
make check            # Run linting and type checking
make format           # Format code with ruff

# Docker workflow
make docker-build     # Build Docker image
make docker-run       # Run in Docker container

# Deployment
make fly-deploy       # Deploy to Fly.io
make fly-logs         # View Fly.io logs
```

### Docker Setup

Build and run with Docker:

```bash
# Using Make
make docker-run

# Or manually
docker build -t sudoku-telnet-server .
docker run -p 8023:8023 -p 8024:8024 -p 8025:8025 -p 8026:8026 sudoku-telnet-server
```

## Deployment to Fly.io

### Using Make (Recommended)

```bash
# Deploy to Fly.io
make fly-deploy

# Check status
make fly-status

# View logs
make fly-logs
```

### Manual Deployment

1. Install the Fly CLI: https://fly.io/docs/hands-on/install-flyctl/

2. Login to Fly:
```bash
fly auth login
```

3. Create and deploy the app:
```bash
# First deployment (creates the app)
fly launch --config fly.toml --now

# Subsequent deployments
fly deploy
```

4. **Important:** Allocate a public IP address for TCP services:
```bash
# Allocate IPv6 (free - recommended)
fly ips allocate-v6

# Optional: Allocate IPv4 (costs $2/month, only needed for IPv4-only clients)
# fly ips allocate-v4 --yes

# Verify IP is allocated
fly ips list
```

5. Check the status:
```bash
fly status
```

6. View logs:
```bash
fly logs
```

7. Connect to your Sudoku server:
```bash
# Get your app's IP address
fly ips list

# Connect via telnet using IPv6 (free tier)
telnet <your-ipv6> 8023

# WebSocket connections work with hostname
# ws://<your-app>.fly.dev:8025/ws
```

**Note:** TCP services (Telnet, raw TCP) require a public IP address on Fly.io. IPv6 is free and sufficient for most users. Only allocate IPv4 if you need to support IPv4-only clients ($2/month cost).

## Connecting to the Server

### Live Demo Server

A live instance is running on Fly.io (IPv6):

**Telnet/TCP:**
```bash
# Via Telnet
telnet 2a09:8280:1::b8:274e:0 8023

# Via TCP
nc 2a09:8280:1::b8:274e:0 8024
```

**WebSocket:**
```
ws://sudoku-telnet-server.fly.dev:8025/ws
ws://sudoku-telnet-server.fly.dev:8026/ws
```

### Local Development

**Via Telnet:**
```bash
telnet localhost 8023
```

**Via Netcat (TCP):**
```bash
nc localhost 8024
```

**Via WebSocket:**
```
ws://localhost:8025/ws
ws://localhost:8026/ws
```

## Game Rules

Sudoku is a logic-based number puzzle. The objective is to fill a 9×9 grid with digits so that:

1. Each **row** contains the digits 1-9 without repetition
2. Each **column** contains the digits 1-9 without repetition
3. Each **3×3 box** contains the digits 1-9 without repetition

Some cells are pre-filled (these cannot be modified) and your task is to fill the remaining cells.

## Difficulty Levels

- **Easy**: 35 cells removed from the solved puzzle
- **Medium**: 45 cells removed from the solved puzzle
- **Hard**: 55 cells removed from the solved puzzle

## Example Gameplay

```
> start medium

==================================================
SUDOKU - MEDIUM MODE
==================================================
Fill the grid so that every row, column, and 3x3 box
contains the digits 1-9 without repetition.

Type 'help' for commands or 'hint' for a clue.
==================================================

    1 2 3   4 5 6   7 8 9
  -------------------------
1 | . . 3 | . 2 . | 6 . . |
2 | 9 . . | 3 . 5 | . . 1 |
3 | . . 1 | 8 . 6 | 4 . . |
  -------------------------
4 | . . 8 | 1 . 2 | 9 . . |
5 | 7 . . | . . . | . . 8 |
6 | . . 6 | 7 . 8 | 2 . . |
  -------------------------
7 | . . 2 | 6 . 9 | 5 . . |
8 | 8 . . | 2 . 3 | . . 9 |
9 | . . 5 | . 1 . | 3 . . |
  -------------------------
Moves made: 0
==================================================

> hint
Hint: Try placing 4 at row 1, column 1

> place 1 1 4
Number placed successfully!

> check
Empty cells: 50
All filled cells are correct so far!
```

## Architecture

This server is built on the [chuk-protocol-server](https://github.com/YOUR_USERNAME/chuk-protocol-server) framework, which provides:

- Multiple transport protocol support (Telnet, TCP, WebSocket, WS-Telnet)
- Telnet protocol negotiation (IAC, WILL, WONT, DO, DONT)
- WebSocket handling with ping/pong keepalive
- Connection management and monitoring
- Asynchronous I/O with Python asyncio

The Sudoku game logic (`SudokuGame` class) includes:
- Puzzle generation using backtracking algorithm
- Move validation according to Sudoku rules (row, column, 3x3 box)
- Automatic solution generation
- Difficulty-based cell removal (35/45/55 cells for easy/medium/hard)
- Hint system (suggests next valid move)
- Progress checking and validation

The game handler (`SudokuHandler` class) extends `TelnetHandler` and provides:
- Command parsing and validation
- Grid display with ANSI formatting
- Game state management
- Multi-game support per connection

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/sudoku-telnet-server.git
cd sudoku-telnet-server

# Install development dependencies (with UV)
make dev-install

# Or with pip
pip install -e ".[dev]"
```

### Testing

The project has comprehensive test coverage (94%, 50 tests):

```bash
# Run all tests
make test

# Run tests with coverage report
make test-cov

# Run tests in watch mode
make test-watch

# View coverage report in browser
make serve-coverage
```

### Code Quality

The project uses modern Python tooling:

- **Ruff**: Fast linter and formatter (replaces black + flake8)
- **MyPy**: Static type checking
- **Pytest**: Testing framework with async support

```bash
# Run all checks (lint + typecheck + test)
make check

# Run linter
make lint

# Format code
make format

# Type checking
make typecheck
```

### Running Example Clients

```bash
# Telnet client (automated mode)
make example-telnet

# Telnet client (interactive mode)
make example-telnet-interactive

# WebSocket client (automated mode)
make example-ws

# WebSocket client (solve mode - shows full solution)
make example-ws-solve
```

### CI/CD

The project includes GitHub Actions workflows:

- **test.yml**: Runs tests on Ubuntu, Windows, macOS with Python 3.11, 3.12, 3.13
- **publish.yml**: Publishes to PyPI on release
- **release.yml**: Creates GitHub releases
- **fly-deploy.yml**: Auto-deploys to Fly.io on main branch push

Coverage threshold is set to 90% - builds fail if coverage drops below this.

## Project Structure

```
sudoku-telnet-server/
├── src/
│   └── sudoku_telnet_server/
│       ├── __init__.py       # Package initialization
│       └── server.py         # Main server implementation (SudokuGame, SudokuHandler)
├── tests/
│   ├── test_sudoku_game.py   # Game logic tests (15 tests)
│   └── test_sudoku_handler.py # Handler tests (35 tests)
├── examples/
│   ├── simple_client.py      # Telnet client example
│   ├── websocket_client.py   # WebSocket client example
│   └── README.md             # Example usage guide
├── .github/
│   └── workflows/
│       ├── test.yml          # Multi-platform CI testing
│       ├── publish.yml       # PyPI publishing
│       ├── release.yml       # GitHub releases
│       └── fly-deploy.yml    # Fly.io deployment
├── pyproject.toml            # Modern Python project config (deps, tools, metadata)
├── config.yaml               # Multi-transport server configuration
├── Dockerfile                # Docker build instructions
├── fly.toml                  # Fly.io deployment config
├── Makefile                  # Development commands (run, test, lint, etc.)
├── MANIFEST.in               # Package distribution files
└── README.md                 # This file
```

### Key Files

- **src/sudoku_telnet_server/server.py** (289 lines, 94% coverage)
  - `SudokuGame`: Core game logic, puzzle generation, validation
  - `SudokuHandler`: Command handling, display, game state
  - `main()`: Server entry point

- **pyproject.toml**: Modern Python packaging
  - Project metadata and dependencies
  - Tool configurations (ruff, mypy, pytest, coverage)
  - Entry point: `sudoku-server` command

- **config.yaml**: Multi-transport server configuration
  - Telnet (8023), TCP (8024), WebSocket (8025), WS-Telnet (8026)
  - Connection limits, timeouts, SSL settings
  - Handler class mapping

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and checks (`make check`)
5. Ensure coverage stays above 90% (`make test-cov`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide (enforced by ruff)
- Add type hints to all functions
- Write tests for new features
- Update documentation as needed
- Keep coverage above 90%

## Troubleshooting

### Server won't start
- Ensure chuk-protocol-server is installed: `uv pip install chuk-protocol-server`
- Check ports aren't already in use: `lsof -i :8023,8024,8025,8026`
- Verify Python version is 3.11+: `python --version`

### Tests failing
- Install dev dependencies: `make dev-install`
- Clear cache: `make clean`
- Check Python version compatibility

### Coverage too low
- Run coverage report: `make test-cov`
- View HTML report: `make serve-coverage`
- Add tests for uncovered code

## License

MIT License - see the main chuk-protocol-server project for details.

## Credits

- Built using the [chuk-protocol-server](https://github.com/YOUR_USERNAME/chuk-protocol-server) framework
- Sudoku puzzle generation algorithm based on backtracking
- Uses modern Python tooling: UV, Ruff, MyPy, Pytest

## Links

- [chuk-protocol-server](https://github.com/YOUR_USERNAME/chuk-protocol-server) - Multi-transport server framework
- [UV](https://github.com/astral-sh/uv) - Fast Python package manager
- [Ruff](https://github.com/astral-sh/ruff) - Fast Python linter and formatter
- [Fly.io](https://fly.io) - Cloud deployment platform
