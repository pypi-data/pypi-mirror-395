#!/usr/bin/env python3
"""
Sudoku Telnet Server

A telnet server that hosts a text-based Sudoku game.
This implementation uses the chuk-protocol-server framework.
"""

import asyncio
import logging
import os
import random

# Import from the chuk-protocol-server framework
import sys

# Add the chuk-protocol-server to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "chuk-protocol-server", "src"))

from chuk_protocol_server.handlers.telnet_handler import TelnetHandler
from chuk_protocol_server.servers.telnet_server import TelnetServer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger("sudoku-server")


class SudokuGame:
    """Sudoku game logic and state management."""

    def __init__(self, difficulty: str = "easy"):
        """Initialize a new sudoku game.

        Args:
            difficulty: Game difficulty level (easy, medium, hard)
        """
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.initial_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.difficulty = difficulty
        self.moves_made = 0

    def is_valid_move(self, row: int, col: int, num: int, grid: list[list[int]] | None = None) -> bool:
        """Check if placing num at (row, col) is valid according to sudoku rules.

        Args:
            row: Row index (0-8)
            col: Column index (0-8)
            num: Number to place (1-9)
            grid: Grid to check against (defaults to self.grid)

        Returns:
            True if the move is valid, False otherwise
        """
        if grid is None:
            grid = self.grid

        # Check row
        for c in range(9):
            if c != col and grid[row][c] == num:
                return False

        # Check column
        for r in range(9):
            if r != row and grid[r][col] == num:
                return False

        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r != row or c != col) and grid[r][c] == num:
                    return False

        return True

    def solve(self, grid: list[list[int]]) -> bool:
        """Solve the sudoku puzzle using backtracking.

        Args:
            grid: The sudoku grid to solve

        Returns:
            True if solved, False otherwise
        """
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        # Temporarily place the number
                        grid[row][col] = num

                        # Check if it's valid (check against the grid being solved)
                        if self.is_valid_move(row, col, num, grid) and self.solve(grid):
                            return True

                        # Backtrack
                        grid[row][col] = 0

                    return False
        return True

    def generate_puzzle(self) -> None:
        """Generate a new sudoku puzzle."""
        # Start with an empty grid
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

        # Fill diagonal 3x3 boxes (they don't interfere with each other)
        for box in range(3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for i in range(3):
                for j in range(3):
                    self.grid[box * 3 + i][box * 3 + j] = nums[i * 3 + j]

        # Solve the complete grid
        self.solution = [row[:] for row in self.grid]
        self.solve(self.solution)
        self.grid = [row[:] for row in self.solution]

        # Remove numbers based on difficulty
        cells_to_remove = {"easy": 35, "medium": 45, "hard": 55}.get(self.difficulty, 35)

        # Randomly remove numbers
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        for r, c in cells[:cells_to_remove]:
            self.grid[r][c] = 0

        # Store the initial state
        self.initial_grid = [row[:] for row in self.grid]
        self.moves_made = 0

    def place_number(self, row: int, col: int, num: int) -> tuple[bool, str]:
        """Place a number on the grid.

        Args:
            row: Row index (1-9, user-facing)
            col: Column index (1-9, user-facing)
            num: Number to place (1-9, or 0 to clear)

        Returns:
            Tuple of (success, message)
        """
        # Convert to 0-indexed
        row -= 1
        col -= 1

        # Validate coordinates
        if not (0 <= row < 9 and 0 <= col < 9):
            return False, "Invalid coordinates. Use row and column between 1-9."

        # Check if this cell is part of the initial puzzle
        if self.initial_grid[row][col] != 0:
            return False, "Cannot modify initial puzzle cells."

        # Clear the cell
        if num == 0:
            self.grid[row][col] = 0
            return True, "Cell cleared."

        # Validate number
        if not (1 <= num <= 9):
            return False, "Invalid number. Use 1-9 or 0 to clear."

        # Check if the move is valid
        old_value = self.grid[row][col]
        self.grid[row][col] = num

        if not self.is_valid_move(row, col, num):
            self.grid[row][col] = old_value
            return False, "Invalid move! This number conflicts with sudoku rules."

        self.moves_made += 1
        return True, "Number placed successfully!"

    def is_complete(self) -> bool:
        """Check if the puzzle is complete and correct."""
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return False
                if self.grid[row][col] != self.solution[row][col]:
                    return False
        return True

    def get_hint(self) -> tuple[int, int, int] | None:
        """Get a hint for the next move.

        Returns:
            Tuple of (row, col, num) in 1-indexed format, or None if puzzle is complete
        """
        empty_cells = [(r, c) for r in range(9) for c in range(9) if self.grid[r][c] == 0]
        if not empty_cells:
            return None

        row, col = random.choice(empty_cells)
        return row + 1, col + 1, self.solution[row][col]


class SudokuHandler(TelnetHandler):
    """Handler for Sudoku telnet sessions."""

    async def on_connect(self) -> None:
        """Initialize game state when a client connects."""
        await super().on_connect()
        self.game: SudokuGame | None = None
        self.game_started = False

    async def show_help(self) -> None:
        """Display help information about the game."""
        await self.send_line("\nSUDOKU - HELP")
        await self.send_line("=" * 50)
        await self.send_line("COMMANDS:")
        await self.send_line("  start [easy|medium|hard] - Start a new game")
        await self.send_line("                              (default: easy)")
        await self.send_line("  show                      - Display the current grid")
        await self.send_line("  place <row> <col> <num>   - Place a number")
        await self.send_line("                              Example: place 1 5 7")
        await self.send_line("  clear <row> <col>         - Clear a cell")
        await self.send_line("  hint                      - Get a hint")
        await self.send_line("  check                     - Check if puzzle is solved")
        await self.send_line("  solve                     - Show the solution")
        await self.send_line("  help                      - Show this help")
        await self.send_line("  quit                      - Exit the game")
        await self.send_line("\nGAME RULES:")
        await self.send_line("  - Fill the 9x9 grid with numbers 1-9")
        await self.send_line("  - Each row must contain 1-9 without repeats")
        await self.send_line("  - Each column must contain 1-9 without repeats")
        await self.send_line("  - Each 3x3 box must contain 1-9 without repeats")
        await self.send_line("=" * 50 + "\n")

    async def display_grid(self) -> None:
        """Display the current sudoku grid."""
        if not self.game:
            await self.send_line("No game in progress. Type 'start' to begin.")
            return

        await self.send_line("\n" + "=" * 50)
        await self.send_line("    1 2 3   4 5 6   7 8 9")
        await self.send_line("  " + "-" * 25)

        for row in range(9):
            if row > 0 and row % 3 == 0:
                await self.send_line("  " + "-" * 25)

            line = f"{row + 1} |"
            for col in range(9):
                if col > 0 and col % 3 == 0:
                    line += " |"

                cell = self.game.grid[row][col]
                if cell == 0:
                    line += " ."
                elif self.game.initial_grid[row][col] != 0:
                    # Initial cells shown in a different style
                    line += f" {cell}"
                else:
                    # User-placed cells
                    line += f" {cell}"

            line += " |"
            await self.send_line(line)

        await self.send_line("  " + "-" * 25)
        await self.send_line(f"Moves made: {self.game.moves_made}")
        await self.send_line("=" * 50 + "\n")

    async def start_game(self, difficulty: str = "easy") -> None:
        """Start a new game.

        Args:
            difficulty: Game difficulty (easy, medium, hard)
        """
        valid_difficulties = ["easy", "medium", "hard"]
        if difficulty not in valid_difficulties:
            await self.send_line(f"Invalid difficulty. Choose from: {', '.join(valid_difficulties)}")
            return

        self.game = SudokuGame(difficulty)
        self.game.generate_puzzle()
        self.game_started = True

        logger.info(f"Started new {difficulty} game for {self.addr}")

        await self.send_line("\n" + "=" * 50)
        await self.send_line(f"SUDOKU - {difficulty.upper()} MODE")
        await self.send_line("=" * 50)
        await self.send_line("Fill the grid so that every row, column, and 3x3 box")
        await self.send_line("contains the digits 1-9 without repetition.")
        await self.send_line("\nType 'help' for commands or 'hint' for a clue.")
        await self.send_line("=" * 50 + "\n")

        await self.display_grid()

    async def on_command_submitted(self, command: str) -> None:
        """Process a command from the player."""
        parts = command.strip().lower().split()

        if not parts:
            return

        cmd = parts[0]

        if cmd == "quit":
            await self.send_line("Thanks for playing Sudoku! Goodbye!")
            return

        elif cmd == "help":
            await self.show_help()

        elif cmd == "start":
            difficulty = parts[1] if len(parts) > 1 else "easy"
            await self.start_game(difficulty)

        elif cmd == "show":
            if self.game_started:
                await self.display_grid()
            else:
                await self.send_line("No game in progress. Type 'start' to begin.")

        elif cmd == "place":
            if not self.game_started:
                await self.send_line("No game in progress. Type 'start' to begin.")
                return

            if len(parts) != 4:
                await self.send_line("Usage: place <row> <col> <num>")
                await self.send_line("Example: place 1 5 7")
                return

            try:
                row = int(parts[1])
                col = int(parts[2])
                num = int(parts[3])

                success, message = self.game.place_number(row, col, num)
                await self.send_line(message)

                if success:
                    await self.display_grid()

                    if self.game.is_complete():
                        await self.send_line("\n" + "=" * 50)
                        await self.send_line("CONGRATULATIONS! YOU SOLVED IT!")
                        await self.send_line("=" * 50)
                        await self.send_line(f"Total moves: {self.game.moves_made}")
                        await self.send_line("\nType 'start' to play again.")
                        await self.send_line("=" * 50 + "\n")
                        self.game_started = False

            except ValueError:
                await self.send_line("Invalid input. Use numbers only.")

        elif cmd == "clear":
            if not self.game_started:
                await self.send_line("No game in progress. Type 'start' to begin.")
                return

            if len(parts) != 3:
                await self.send_line("Usage: clear <row> <col>")
                return

            try:
                row = int(parts[1])
                col = int(parts[2])

                success, message = self.game.place_number(row, col, 0)
                await self.send_line(message)

                if success:
                    await self.display_grid()

            except ValueError:
                await self.send_line("Invalid input. Use numbers only.")

        elif cmd == "hint":
            if not self.game_started:
                await self.send_line("No game in progress. Type 'start' to begin.")
                return

            hint = self.game.get_hint()
            if hint:
                row, col, num = hint
                await self.send_line(f"Hint: Try placing {num} at row {row}, column {col}")
            else:
                await self.send_line("No hints available. Puzzle is complete!")

        elif cmd == "check":
            if not self.game_started:
                await self.send_line("No game in progress. Type 'start' to begin.")
                return

            if self.game.is_complete():
                await self.send_line("Puzzle is correct! Well done!")
            else:
                # Count empty cells and errors
                empty = sum(1 for r in range(9) for c in range(9) if self.game.grid[r][c] == 0)
                errors = sum(
                    1
                    for r in range(9)
                    for c in range(9)
                    if self.game.grid[r][c] != 0 and self.game.grid[r][c] != self.game.solution[r][c]
                )

                await self.send_line(f"Empty cells: {empty}")
                if errors > 0:
                    await self.send_line(f"Incorrect cells: {errors}")
                else:
                    await self.send_line("All filled cells are correct so far!")

        elif cmd == "solve":
            if not self.game_started:
                await self.send_line("No game in progress. Type 'start' to begin.")
                return

            await self.send_line("\nShowing solution...\n")
            self.game.grid = [row[:] for row in self.game.solution]
            await self.display_grid()
            await self.send_line("Type 'start' to play again.")
            self.game_started = False

        else:
            await self.send_line("Unknown command. Type 'help' for available commands.")

    async def send_welcome(self) -> None:
        """Send a welcome message to the player."""
        await self.send_line("=" * 50)
        await self.send_line("       WELCOME TO THE SUDOKU SERVER!        ")
        await self.send_line("=" * 50)
        await self.send_line("COMMANDS:")
        await self.send_line("  start [easy|medium|hard] - Begin a new game")
        await self.send_line("  help                     - View all commands")
        await self.send_line("  quit                     - Disconnect")
        await self.send_line("=" * 50)

    async def process_line(self, line: str) -> bool:
        """Process a line of input from the client.

        Args:
            line: The line to process

        Returns:
            True to continue processing, False to terminate
        """
        logger.debug(f"SudokuHandler process_line => {line!r}")

        # Check for exit commands
        if line.lower() in ["quit", "exit", "q"]:
            await self.send_line("Thanks for playing Sudoku! Goodbye!")
            await self.end_session()
            return False

        # Process the command
        await self.on_command_submitted(line)

        return True


async def main():
    """Main entry point for the Sudoku server."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    host, port = "0.0.0.0", 8023
    server = TelnetServer(host, port, SudokuHandler)

    try:
        logger.info(f"Starting Sudoku Server on {host}:{port}")
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("Server shutdown initiated by user.")
    except Exception as e:
        logger.error(f"Error running server: {e}")
    finally:
        logger.info("Server has shut down.")


def run_server():
    """CLI entry point for running the server."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt.")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
    finally:
        logger.info("Server process exiting.")


if __name__ == "__main__":
    run_server()
