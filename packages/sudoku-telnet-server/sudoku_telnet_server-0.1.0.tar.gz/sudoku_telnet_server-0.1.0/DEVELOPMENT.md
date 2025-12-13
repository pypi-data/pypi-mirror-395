# Development Guide

This guide covers development workflows, testing, and deployment for the Sudoku Telnet Server.

## Quick Start

```bash
# Install development dependencies
make dev-install

# Run the server
make run

# Run tests
make test

# Run all checks (lint, format, type check)
make check
```

## Makefile Commands

Run `make help` to see all available commands. Here are the most common ones:

### Development Workflow

```bash
# Set up development environment
make dev                  # Install all dev dependencies

# Run the server locally
make run                  # Using chuk-protocol-server launcher
make run-direct           # Direct execution of sudoku_handler.py

# Quick development check
make quick-check          # Format + lint (fast)
```

### Testing

```bash
# Run tests
make test                 # Run all tests
make test-cov            # Run tests with coverage report
make test-watch          # Run tests in watch mode (auto-rerun on changes)

# View coverage report in browser
make serve-coverage      # Serves on http://localhost:8000
```

### Code Quality

```bash
# Run all checks
make check               # Runs lint, type-check, and format-check

# Individual checks
make lint                # Run flake8 linter
make format              # Format code with black
make format-check        # Check formatting without modifying
make type-check          # Run mypy type checker
```

### Docker Development

```bash
# Build and run in Docker
make docker-build        # Build Docker image
make docker-run          # Build and run container
make docker-logs         # View container logs
make docker-shell        # Open shell in running container

# Clean up
make docker-stop         # Stop container
make docker-clean        # Remove container and image
```

### Deployment

```bash
# Deploy to Fly.io
make fly-deploy          # Deploy to Fly.io
make fly-status          # Check deployment status
make fly-logs            # View production logs
make fly-open            # Open app in browser
make fly-ssh             # SSH into production container
```

### Examples

```bash
# Run example clients
make example-telnet              # Telnet client (automated)
make example-telnet-interactive  # Telnet client (interactive)
make example-ws                  # WebSocket client (automated)
make example-ws-interactive      # WebSocket client (interactive)
make example-ws-solve            # WebSocket solve demo
```

### Cleanup

```bash
make clean               # Remove generated files and caches
make clean-all           # Remove everything including Docker images
```

## Development Environment Setup

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized development)
- Fly CLI (optional, for deployment)

### Initial Setup

1. Clone the repository and navigate to the project:
```bash
cd sudoku-telnet-server
```

2. Install dependencies:
```bash
make dev-install
```

3. Run tests to verify setup:
```bash
make test
```

4. Start the server:
```bash
make run
```

## Testing Guide

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest tests/test_sudoku_game.py -v

# Run specific test
pytest tests/test_sudoku_game.py::TestSudokuGame::test_puzzle_generation -v

# Run in watch mode (auto-rerun on changes)
make test-watch
```

### Writing Tests

Tests are located in the `tests/` directory:

- `test_sudoku_game.py` - Tests for the SudokuGame class
- `test_sudoku_handler.py` - Tests for the SudokuHandler class

Example test:

```python
import pytest
from sudoku_handler import SudokuGame

def test_game_initialization():
    game = SudokuGame(difficulty="easy")
    assert game.difficulty == "easy"
    assert game.moves_made == 0
```

For async tests:

```python
import pytest

@pytest.mark.asyncio
async def test_handler():
    handler = SudokuHandler()
    await handler.on_connect()
    assert handler.game_started is False
```

### Coverage Reports

After running `make test-cov`, open the HTML coverage report:

```bash
# Serve coverage report
make serve-coverage

# Or open directly
open htmlcov/index.html
```

## Code Quality

### Linting

We use `flake8` for linting:

```bash
make lint
```

Configuration is in `.flake8`:
- Max line length: 120
- Ignores: E203, W503 (for black compatibility)

### Formatting

We use `black` for code formatting:

```bash
# Format all code
make format

# Check formatting without modifying
make format-check
```

Black is configured for 120 character line length.

### Type Checking

We use `mypy` for static type checking:

```bash
make type-check
```

## Docker Development

### Building

```bash
make docker-build
```

The Dockerfile:
1. Uses Python 3.11 slim image
2. Installs chuk-protocol-server from local path
3. Copies server files
4. Exposes ports 8023-8026
5. Runs health checks

### Running Locally

```bash
# Run in background
make docker-run

# View logs
make docker-logs

# Open shell
make docker-shell

# Stop
make docker-stop
```

### Testing in Docker

```bash
# Build and run
make docker-run

# In another terminal, test with telnet
telnet localhost 8023

# Or use example client
make example-telnet
```

## Deployment to Fly.io

### Initial Setup

1. Install Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Login:
```bash
fly auth login
```

3. Create app (first time only):
```bash
fly launch --config fly.toml --now
```

### Deploying Updates

```bash
# Deploy
make fly-deploy

# Check status
make fly-status

# View logs
make fly-logs
```

### Managing Production

```bash
# SSH into production
make fly-ssh

# Scale instances
fly scale count 2

# Scale resources
fly scale vm shared-cpu-1x --memory 512

# View metrics
fly dashboard
```

## Continuous Integration

For CI/CD pipelines:

```bash
# Run full CI pipeline
make ci

# This runs:
# 1. dev-install (install dependencies)
# 2. check (lint, format-check, type-check)
# 3. test (run all tests)
```

Example GitHub Actions workflow:

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: make ci
```

## Debugging

### Local Debugging

```bash
# Run server with debug logging
LOG_LEVEL=DEBUG make run

# Run specific transport only
python sudoku_handler.py  # Runs telnet only on 8023
```

### Docker Debugging

```bash
# Build and run
make docker-run

# Check logs
make docker-logs

# Enter container
make docker-shell

# Inside container, you can:
ps aux                    # Check processes
netstat -tlnp            # Check ports
python -c "import sudoku_handler"  # Test imports
```

### Production Debugging

```bash
# View logs
make fly-logs

# SSH into production
make fly-ssh

# Check health
fly status
fly checks list
```

## Common Issues

### Port Already in Use

```bash
# Find process using port 8023
lsof -i :8023

# Kill it
kill -9 <PID>
```

### Import Errors

```bash
# Reinstall dependencies
make clean
make dev-install
```

### Test Failures

```bash
# Run tests with verbose output
pytest tests/ -vv

# Run specific failing test
pytest tests/test_sudoku_game.py::TestSudokuGame::test_puzzle_generation -vv
```

## Project Structure

```
sudoku-telnet-server/
├── sudoku_handler.py      # Main server implementation
├── config.yaml            # Server configuration
├── Dockerfile             # Docker build instructions
├── fly.toml              # Fly.io deployment config
├── Makefile              # Development commands
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── pytest.ini            # Pytest configuration
├── .flake8              # Flake8 configuration
├── tests/
│   ├── __init__.py
│   ├── test_sudoku_game.py
│   └── test_sudoku_handler.py
├── examples/
│   ├── README.md
│   ├── simple_client.py
│   └── websocket_client.py
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and ensure tests pass: `make check test`
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

## Version Information

Check versions:

```bash
make version
```

This shows:
- Python version
- Pip version
- Installed packages (chuk-protocol-server, pytest, etc.)
