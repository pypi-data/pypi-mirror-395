"""State management for tracking processed messages"""
import fcntl
import os
from datetime import datetime
from pathlib import Path

from ntfy_catch.logger_setup import get_logger


class StateManager:
    """Manages timestamp files for tracking processed messages per topic"""

    def __init__(self, state_dir):
        """Initialize state manager

        Args:
            state_dir: Directory to store timestamp files
        """
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.logger = get_logger()

    def get_last_timestamp(self, topic):
        """Get the last processed message timestamp for a topic

        Args:
            topic: Topic name

        Returns:
            int: Unix timestamp of last processed message, or None if no previous state
        """
        timestamp_file = self._get_timestamp_file(topic)

        if not timestamp_file.exists():
            self.logger.debug(f"[{topic}] No previous state found")
            return None

        try:
            timestamp_str = self._read_timestamp_safe(timestamp_file)
            if timestamp_str:
                # Parse ISO 8601 timestamp and convert to Unix timestamp
                dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                unix_timestamp = int(dt.timestamp())
                self.logger.debug(f"[{topic}] Last timestamp: {timestamp_str} ({unix_timestamp})")
                return unix_timestamp
            return None
        except (ValueError, OSError) as e:
            self.logger.warning(f"[{topic}] Failed to read timestamp file: {e}")
            return None

    def update_last_timestamp(self, topic, unix_time):
        """Update the last processed message timestamp for a topic

        Args:
            topic: Topic name
            unix_time: Unix timestamp of the message
        """
        timestamp_file = self._get_timestamp_file(topic)

        # Convert Unix timestamp to ISO 8601 format in UTC
        dt = datetime.utcfromtimestamp(unix_time)
        iso_timestamp = dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        try:
            self._write_timestamp_safe(timestamp_file, iso_timestamp)
            self.logger.debug(f"[{topic}] Updated timestamp to {iso_timestamp}")
        except OSError as e:
            self.logger.error(f"[{topic}] Failed to update timestamp: {e}")
            raise

    def _get_timestamp_file(self, topic):
        """Get the path to the timestamp file for a topic

        Args:
            topic: Topic name

        Returns:
            Path: Path to timestamp file
        """
        # Sanitize topic name for filesystem
        safe_topic = topic.replace('/', '_')
        return self.state_dir / f"{safe_topic}.timestamp"

    def _read_timestamp_safe(self, filepath):
        """Read timestamp from file with shared locking

        Args:
            filepath: Path to timestamp file

        Returns:
            str: Timestamp string, or None if file doesn't exist
        """
        try:
            with open(filepath, 'r') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                try:
                    return f.read().strip()
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except FileNotFoundError:
            return None

    def _write_timestamp_safe(self, filepath, timestamp):
        """Write timestamp to file with exclusive locking and atomic operation

        Args:
            filepath: Path to timestamp file
            timestamp: ISO 8601 timestamp string
        """
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Write to temporary file first
        temp_path = filepath.with_suffix('.tmp')

        with open(temp_path, 'w') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                f.write(timestamp)
                f.flush()
                os.fsync(f.fileno())
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

        # Atomic rename
        os.replace(temp_path, filepath)
