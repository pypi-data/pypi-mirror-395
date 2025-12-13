"""Action dispatcher for invoking external handler scripts"""
import json
import subprocess

from ntfy_catch.logger_setup import get_logger


class ActionDispatcher:
    """Dispatches messages to external handler script"""

    def __init__(self, handler_script, timeout=30, continue_on_error=True):
        """Initialize action dispatcher

        Args:
            handler_script: Path to external handler script
            timeout: Timeout in seconds for handler execution
            continue_on_error: Whether to continue on handler failure
        """
        self.handler_script = handler_script
        self.timeout = timeout
        self.continue_on_error = continue_on_error
        self.logger = get_logger()

    def dispatch(self, message):
        """Send message to external handler via stdin

        Handler receives JSON message on stdin and should exit with:
        - 0: Success (timestamp will be updated)
        - Non-zero: Failure (timestamp NOT updated, message replays)

        Args:
            message: Message dictionary to dispatch

        Returns:
            tuple: (success: bool, returncode: int, output: str)
        """
        topic = message.get('topic', 'unknown')
        msg_id = message.get('id', 'unknown')
        msg_text = message.get('message', '')[:50]  # First 50 chars for logging

        self.logger.info(f"[{topic}] Message {msg_id}: \"{msg_text}\" → dispatching")

        try:
            payload = json.dumps(message)

            result = subprocess.run(
                [self.handler_script],
                input=payload,
                stdout=subprocess.PIPE,
                stderr=None,
                timeout=self.timeout,
                text=True
            )

            if result.returncode != 0:
                self.logger.error(
                    f"[{topic}] Handler failed for message {msg_id} (exit {result.returncode})"
                )
                if not self.continue_on_error:
                    raise RuntimeError(f"Handler failed with exit code {result.returncode}")
                return (False, result.returncode, "")
            else:
                self.logger.info(f"[{topic}] Handler executed successfully (exit 0)")
                if result.stdout:
                    self.logger.debug(f"[{topic}] Handler stdout: {result.stdout.strip()}")
                return (True, 0, result.stdout)

        except subprocess.TimeoutExpired:
            self.logger.error(f"[{topic}] Handler timeout after {self.timeout}s for message {msg_id}")
            if not self.continue_on_error:
                raise
            return (False, -1, "Timeout")

        except Exception as e:
            self.logger.error(f"[{topic}] Dispatch failed for message {msg_id}: {e}")
            if not self.continue_on_error:
                raise
            return (False, -1, str(e))
