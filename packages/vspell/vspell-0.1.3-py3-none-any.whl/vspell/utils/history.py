from vspell.constants import HISTORY_FILE
import os

class History:
    MAX_HISTORY = 100

    def __init__(self):
        self.history_file = HISTORY_FILE

    # Add any needed helper methods
    def _ensure_history_exists(self) -> None:
        """Ensure the history file exists."""
        if not os.path.exists(self.history_file):
            # Create empty file
            with open(self.history_file, "w", encoding="utf-8") as f:
                f.write("")

    def log_history(self, transcribed_text: str) -> None:
        """Append transcribed_text to the history log file, keeping max history entries."""
        self._ensure_history_exists()

        with open(self.history_file, "r", encoding="utf-8") as f:
            entries = f.readlines()

        # Append new entry
        entries.append(transcribed_text.strip() + "\n")

        # Keep only last MAX_HISTORY entries
        entries = entries[-self.MAX_HISTORY:]

        # Write back to disk
        with open(self.history_file, "w", encoding="utf-8") as f:
            f.writelines(entries)

    def show_history(self, limit: int = MAX_HISTORY) -> None:
        """Pretty print recent command history."""
        self._ensure_history_exists()
        with open(self.history_file, "r", encoding="utf-8") as f:
            entries = f.readlines()

        if not entries:
            print("No history found.")
            return

        # Only show last `limit` entries
        entries = [e.strip() for e in entries][-limit:]

        print("\nHistory:")
        for idx, cmd in enumerate(entries, start=1):
            print(f"{idx:3d}: {cmd}")

    def get_history_command(self, index: int) -> str | None:
        """Return the text for a given history index."""
        self._ensure_history_exists()
        with open(self.history_file, "r", encoding="utf-8") as f:
            entries = f.readlines()

        if not entries:
            return None

        entries = [e.strip() for e in entries]

        # Convert 1-based index to Python index
        if 1 <= index <= len(entries):
            return entries[index - 1]

        return None
