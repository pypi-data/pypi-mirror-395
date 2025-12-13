#!/usr/bin/env python3
"""
Simple Telnet Client for Sudoku Server

This example demonstrates how to connect to the Sudoku server
and interact with it programmatically.
"""

import socket
import sys
import time


class SudokuClient:
    """Simple client for connecting to the Sudoku telnet server."""

    def __init__(self, host: str = "localhost", port: int = 8023):
        """Initialize the client.

        Args:
            host: Server hostname
            port: Server port
        """
        self.host = host
        self.port = port
        self.sock = None

    def connect(self) -> bool:
        """Connect to the server.

        Returns:
            True if connected successfully, False otherwise
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def send_command(self, command: str) -> None:
        """Send a command to the server.

        Args:
            command: Command string to send
        """
        if self.sock:
            self.sock.sendall((command + "\n").encode("utf-8"))
            print(f"> {command}")

    def receive_response(self, timeout: float = 1.0) -> str:
        """Receive response from the server.

        Args:
            timeout: Timeout in seconds

        Returns:
            Response string from server
        """
        if not self.sock:
            return ""

        self.sock.settimeout(timeout)
        response = ""
        try:
            while True:
                chunk = self.sock.recv(4096).decode("utf-8", errors="ignore")
                if not chunk:
                    break
                response += chunk
        except TimeoutError:
            pass
        except Exception as e:
            print(f"Error receiving: {e}")

        return response

    def disconnect(self) -> None:
        """Disconnect from the server."""
        if self.sock:
            try:
                self.send_command("quit")
                time.sleep(0.5)
                self.sock.close()
                print("Disconnected")
            except Exception as e:
                print(f"Error disconnecting: {e}")
            finally:
                self.sock = None

    def interactive_mode(self) -> None:
        """Run in interactive mode, allowing user input."""
        if not self.connect():
            return

        # Read welcome message
        welcome = self.receive_response()
        print(welcome)

        try:
            while True:
                command = input("\nEnter command (or 'quit' to exit): ").strip()
                if not command:
                    continue

                self.send_command(command)

                if command.lower() in ["quit", "exit", "q"]:
                    break

                response = self.receive_response(timeout=2.0)
                print(response)

        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            self.disconnect()


def example_automated_game():
    """Example of an automated game session."""
    print("=" * 60)
    print("EXAMPLE: Automated Sudoku Game Session")
    print("=" * 60)

    client = SudokuClient()

    if not client.connect():
        return

    # Read welcome message
    response = client.receive_response()
    print(response)

    # Start an easy game
    print("\n[Starting easy game]")
    client.send_command("start easy")
    time.sleep(0.5)
    response = client.receive_response(timeout=2.0)
    print(response)

    # Get a hint
    print("\n[Requesting hint]")
    client.send_command("hint")
    time.sleep(0.3)
    response = client.receive_response()
    print(response)

    # Place a number based on the hint (you would parse this in real code)
    print("\n[Placing a number]")
    client.send_command("place 1 1 5")
    time.sleep(0.3)
    response = client.receive_response(timeout=2.0)
    print(response)

    # Show the grid
    print("\n[Showing grid]")
    client.send_command("show")
    time.sleep(0.3)
    response = client.receive_response(timeout=2.0)
    print(response)

    # Check progress
    print("\n[Checking progress]")
    client.send_command("check")
    time.sleep(0.3)
    response = client.receive_response()
    print(response)

    # Get help
    print("\n[Getting help]")
    client.send_command("help")
    time.sleep(0.3)
    response = client.receive_response(timeout=2.0)
    print(response)

    # Disconnect
    client.disconnect()


def example_websocket_client():
    """Example of connecting via WebSocket (requires websockets library)."""
    print("=" * 60)
    print("EXAMPLE: WebSocket Client")
    print("=" * 60)
    print("\nTo use WebSocket, install: pip install websockets")
    print("\nExample code:")
    print("""
import asyncio
import websockets

async def connect_websocket():
    uri = "ws://localhost:8025/ws"
    async with websockets.connect(uri) as websocket:
        # Receive welcome message
        welcome = await websocket.recv()
        print(welcome)

        # Start a game
        await websocket.send("start easy")
        response = await websocket.recv()
        print(response)

        # Get a hint
        await websocket.send("hint")
        response = await websocket.recv()
        print(response)

        # Quit
        await websocket.send("quit")

asyncio.run(connect_websocket())
""")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

        if mode == "interactive":
            print("Starting interactive mode...")
            client = SudokuClient()
            client.interactive_mode()

        elif mode == "automated":
            example_automated_game()

        elif mode == "websocket":
            example_websocket_client()

        elif mode == "help":
            print("Usage: python simple_client.py [mode]")
            print("\nModes:")
            print("  interactive - Interactive command-line mode")
            print("  automated   - Run automated example session")
            print("  websocket   - Show WebSocket example code")
            print("  help        - Show this help")
            print("\nDefault: automated")

        else:
            print(f"Unknown mode: {mode}")
            print("Use 'help' for usage information")

    else:
        # Default: run automated example
        example_automated_game()


if __name__ == "__main__":
    main()
