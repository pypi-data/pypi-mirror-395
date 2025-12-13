#!/usr/bin/env python3
"""
WebSocket Client for Sudoku Server

This example demonstrates how to connect to the Sudoku server
via WebSocket and interact with it.

Requirements:
    pip install websockets
"""

import asyncio
import sys

try:
    import websockets
except ImportError:
    print("This example requires the 'websockets' library.")
    print("Install it with: pip install websockets")
    sys.exit(1)


class SudokuWebSocketClient:
    """WebSocket client for the Sudoku server."""

    def __init__(self, uri: str = "ws://localhost:8025/ws"):
        """Initialize the client.

        Args:
            uri: WebSocket URI
        """
        self.uri = uri
        self.websocket = None

    async def connect(self):
        """Connect to the WebSocket server."""
        try:
            self.websocket = await websockets.connect(self.uri)
            print(f"Connected to {self.uri}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    async def send_command(self, command: str):
        """Send a command to the server.

        Args:
            command: Command to send
        """
        if self.websocket:
            await self.websocket.send(command)
            print(f"> {command}")

    async def receive_response(self, timeout: float = 2.0):
        """Receive a response from the server.

        Args:
            timeout: Timeout in seconds

        Returns:
            Response string
        """
        if not self.websocket:
            return ""

        try:
            response = await asyncio.wait_for(self.websocket.recv(), timeout=timeout)
            return response
        except TimeoutError:
            return ""
        except Exception as e:
            print(f"Error receiving: {e}")
            return ""

    async def disconnect(self):
        """Disconnect from the server."""
        if self.websocket:
            try:
                await self.send_command("quit")
                await asyncio.sleep(0.5)
                await self.websocket.close()
                print("Disconnected")
            except Exception as e:
                print(f"Error disconnecting: {e}")

    async def interactive_mode(self):
        """Run in interactive mode."""
        if not await self.connect():
            return

        # Receive welcome message
        welcome = await self.receive_response()
        print(welcome)

        try:
            while True:
                # Get user input (this is tricky in async, using run_in_executor)
                loop = asyncio.get_event_loop()
                command = await loop.run_in_executor(
                    None, lambda: input("\nEnter command (or 'quit' to exit): ").strip()
                )

                if not command:
                    continue

                await self.send_command(command)

                if command.lower() in ["quit", "exit", "q"]:
                    break

                response = await self.receive_response(timeout=2.0)
                print(response)

        except KeyboardInterrupt:
            print("\nInterrupted by user")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await self.disconnect()


async def example_automated_game():
    """Example of an automated game session via WebSocket."""
    print("=" * 60)
    print("EXAMPLE: Automated WebSocket Sudoku Game")
    print("=" * 60)

    client = SudokuWebSocketClient()

    if not await client.connect():
        return

    # Receive welcome message
    response = await client.receive_response()
    print(response)

    # Start an easy game
    print("\n[Starting easy game]")
    await client.send_command("start easy")
    response = await client.receive_response()
    print(response)

    # Get a hint
    print("\n[Requesting hint]")
    await client.send_command("hint")
    response = await client.receive_response()
    print(response)

    # Place a number
    print("\n[Placing a number]")
    await client.send_command("place 1 1 5")
    response = await client.receive_response()
    print(response)

    # Show the grid
    print("\n[Showing grid]")
    await client.send_command("show")
    response = await client.receive_response()
    print(response)

    # Check progress
    print("\n[Checking progress]")
    await client.send_command("check")
    response = await client.receive_response()
    print(response)

    # Start a medium game
    print("\n[Starting medium game]")
    await client.send_command("start medium")
    response = await client.receive_response()
    print(response)

    # Get help
    print("\n[Getting help]")
    await client.send_command("help")
    response = await client.receive_response()
    print(response)

    # Disconnect
    await client.disconnect()


async def example_solve_game():
    """Example showing how to solve a puzzle step by step."""
    print("=" * 60)
    print("EXAMPLE: Solving with Hints")
    print("=" * 60)

    client = SudokuWebSocketClient()

    if not await client.connect():
        return

    # Receive welcome
    await client.receive_response()

    # Start an easy game
    print("\n[Starting easy game]")
    await client.send_command("start easy")
    response = await client.receive_response()
    print(response)

    # Get 5 hints and place them
    print("\n[Getting 5 hints and placing numbers]")
    for i in range(5):
        await client.send_command("hint")
        hint = await client.receive_response()
        print(f"\nHint {i + 1}: {hint}")

        # In a real implementation, you would parse the hint
        # and automatically place the number
        # Example hint: "Hint: Try placing 5 at row 1, column 3"
        # You would extract: row=1, col=3, num=5
        # Then: await client.send_command('place 1 3 5')

        await asyncio.sleep(0.5)

    # Show current state
    print("\n[Showing current grid]")
    await client.send_command("show")
    response = await client.receive_response()
    print(response)

    # Disconnect
    await client.disconnect()


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

        if mode == "interactive":
            print("Starting interactive WebSocket mode...")
            client = SudokuWebSocketClient()
            asyncio.run(client.interactive_mode())

        elif mode == "automated":
            asyncio.run(example_automated_game())

        elif mode == "solve":
            asyncio.run(example_solve_game())

        elif mode == "help":
            print("Usage: python websocket_client.py [mode]")
            print("\nModes:")
            print("  interactive - Interactive command-line mode")
            print("  automated   - Run automated example session")
            print("  solve       - Example using hints to solve")
            print("  help        - Show this help")
            print("\nDefault: automated")
            print("\nRequires: pip install websockets")

        else:
            print(f"Unknown mode: {mode}")
            print("Use 'help' for usage information")

    else:
        # Default: run automated example
        asyncio.run(example_automated_game())


if __name__ == "__main__":
    main()
