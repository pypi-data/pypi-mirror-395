# Sudoku Server Client Examples

This directory contains example clients demonstrating how to connect to and interact with the Sudoku server.

## Available Examples

### 1. Simple Telnet Client (`simple_client.py`)

A basic telnet client that connects to the server using raw TCP sockets.

**Usage:**

```bash
# Interactive mode (type commands manually)
python examples/simple_client.py interactive

# Automated demo (runs a pre-programmed sequence)
python examples/simple_client.py automated

# Show help
python examples/simple_client.py help
```

**Features:**
- Connect via TCP/Telnet (port 8023 or 8024)
- Send commands and receive responses
- Interactive and automated modes
- No external dependencies (uses standard library)

### 2. WebSocket Client (`websocket_client.py`)

A WebSocket client for connecting to the WebSocket endpoints.

**Requirements:**
```bash
pip install websockets
```

**Usage:**

```bash
# Interactive mode
python examples/websocket_client.py interactive

# Automated demo
python examples/websocket_client.py automated

# Solving example with hints
python examples/websocket_client.py solve

# Show help
python examples/websocket_client.py help
```

**Features:**
- Connect via WebSocket (port 8025 or 8026)
- Async/await pattern using Python asyncio
- Multiple example scenarios
- Shows how to handle WebSocket connections

## Example Workflows

### Starting and Playing a Game

```python
# Connect to server
client = SudokuClient()
client.connect()

# Start an easy game
client.send_command('start easy')
response = client.receive_response()
print(response)

# Get a hint
client.send_command('hint')
hint = client.receive_response()
# Example: "Hint: Try placing 5 at row 1, column 3"

# Place the number
client.send_command('place 1 3 5')
response = client.receive_response()

# Show the grid
client.send_command('show')
grid = client.receive_response()
print(grid)

# Check progress
client.send_command('check')
status = client.receive_response()

# Disconnect
client.disconnect()
```

### WebSocket Example

```python
import asyncio
import websockets

async def play_sudoku():
    uri = "ws://localhost:8025/ws"
    async with websockets.connect(uri) as websocket:
        # Receive welcome
        welcome = await websocket.recv()
        print(welcome)

        # Start game
        await websocket.send("start medium")
        response = await websocket.recv()
        print(response)

        # Play the game...
        await websocket.send("hint")
        hint = await websocket.recv()
        print(hint)

        # Quit
        await websocket.send("quit")

asyncio.run(play_sudoku())
```

## Connecting to Different Transports

The server supports multiple transports. Here's how to connect to each:

### Telnet (Port 8023)
```bash
telnet localhost 8023
# Or
nc localhost 8023
# Or
python examples/simple_client.py interactive
```

### TCP (Port 8024)
```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8024))
sock.sendall(b'start easy\n')
response = sock.recv(4096)
```

### WebSocket (Port 8025)
```python
import asyncio
import websockets

async def connect():
    async with websockets.connect('ws://localhost:8025/ws') as ws:
        await ws.send('start easy')
        response = await ws.recv()
        print(response)

asyncio.run(connect())
```

### WebSocket-Telnet (Port 8026)
```python
# Same as WebSocket, but with Telnet protocol negotiation
async with websockets.connect('ws://localhost:8026/ws') as ws:
    # Server will perform Telnet handshake
    await ws.send('start easy')
    response = await ws.recv()
```

## Building Your Own Client

### Basic Client Structure

```python
import socket

class MyClient:
    def __init__(self, host='localhost', port=8023):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send(self, command):
        self.sock.sendall((command + '\n').encode('utf-8'))

    def receive(self):
        return self.sock.recv(4096).decode('utf-8')

    def close(self):
        self.sock.close()

# Use it
client = MyClient()
client.connect()
client.send('start easy')
print(client.receive())
client.send('help')
print(client.receive())
client.close()
```

## Available Commands

All clients can send these commands:

- `start [easy|medium|hard]` - Start a new game
- `show` - Display the current grid
- `place <row> <col> <num>` - Place a number (e.g., `place 1 5 7`)
- `clear <row> <col>` - Clear a cell
- `hint` - Get a hint
- `check` - Check progress
- `solve` - Show the solution
- `help` - Show help
- `quit` - Disconnect

## Tips for Client Development

1. **Always handle line endings**: Commands should end with `\n`
2. **Set timeouts**: Network operations can hang, use timeouts
3. **Parse responses**: The server returns formatted text, parse it as needed
4. **Handle disconnects**: The server may disconnect on errors or timeout
5. **Buffer responses**: Large responses (like grids) may come in chunks

## Testing Your Client

Make sure the server is running first:

```bash
# In one terminal, start the server
cd /path/to/sudoku-telnet-server
chuk-protocol-server server-launcher -c config.yaml

# In another terminal, run your client
python examples/simple_client.py automated
```

## Advanced: AI/Bot Client

You could build a bot that solves sudoku automatically:

1. Connect to the server
2. Start a game
3. Parse the grid from the `show` command
4. Use a sudoku solver algorithm
5. Send `place` commands to fill the grid
6. Use `check` to verify

See the example clients for parsing and command patterns.
