"""ntfy API poller for fetching messages"""
import json
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException

from ntfy_catch.logger_setup import get_logger
from ntfy_catch.state_manager import StateManager


class NtfyPoller:
    """Polls ntfy server for new messages"""

    def __init__(self, config):
        """Initialize poller

        Args:
            config: ConfigParser object with ntfy configuration
        """
        self.base_url = config.get('server', 'base_url').rstrip('/')
        topics_str = config.get('polling', 'topics')
        self.topics = [t.strip() for t in topics_str.split(',')]
        self.state_manager = StateManager(config.get('state', 'state_dir'))
        self.logger = get_logger()

        # Authentication (optional)
        self.auth = None
        username = config.get('server', 'username', fallback=None)
        password = config.get('server', 'password', fallback=None)
        if username and password:
            self.auth = HTTPBasicAuth(username, password)
            self.logger.debug(f"Using HTTP Basic Auth with username: {username}")

        # Filters
        self.min_priority = config.getint('filters', 'min_priority', fallback=1)
        target_tags = config.get('filters', 'target_tags', fallback='')
        self.target_tags = [t.strip() for t in target_tags.split(',') if t.strip()]

    def poll_topic(self, topic):
        """Poll a single topic for new messages

        Args:
            topic: Topic name to poll

        Returns:
            list: List of message dictionaries (empty if no new messages or error)
        """
        last_time = self.state_manager.get_last_timestamp(topic)

        # Build API URL with polling mode
        url = f"{self.base_url}/{topic}/json?poll=1"
        if last_time:
            url += f"&since={last_time+1}"
            self.logger.info(f"[{topic}] Polling with since={last_time+1}")
        else:
            self.logger.info(f"[{topic}] Polling for all recent messages")

        try:
            response = requests.get(url, timeout=30, auth=self.auth)
            response.raise_for_status()

            messages = self._parse_response(response.text, topic)
            filtered_messages = self._filter_messages(messages, topic)

            if filtered_messages:
                self.logger.info(f"[{topic}] Received {len(filtered_messages)} new message(s)")
            else:
                self.logger.debug(f"[{topic}] No new messages")

            return filtered_messages

        except RequestException as e:
            self.logger.error(f"[{topic}] Failed to poll: {e}")
            return []

    def _parse_response(self, response_text, topic):
        """Parse JSON lines response from ntfy

        Args:
            response_text: Raw response text from ntfy API
            topic: Topic name for logging

        Returns:
            list: List of parsed message dictionaries
        """
        messages = []

        if not response_text or not response_text.strip():
            return messages

        for line in response_text.strip().split('\n'):
            if not line.strip():
                continue

            try:
                msg = json.loads(line)

                # Only process 'message' events, skip 'open', 'keepalive', etc.
                if msg.get('event') == 'message':
                    messages.append(msg)
                else:
                    self.logger.debug(f"[{topic}] Skipping event: {msg.get('event')}")

            except json.JSONDecodeError as e:
                self.logger.warning(f"[{topic}] Invalid JSON line: {line[:100]}... Error: {e}")

        return messages

    def _filter_messages(self, messages, topic):
        """Filter messages based on configuration

        Args:
            messages: List of message dictionaries
            topic: Topic name for logging

        Returns:
            list: Filtered list of messages
        """
        filtered = []

        for msg in messages:
            # Priority filter
            priority = msg.get('priority', 3)
            if priority < self.min_priority:
                self.logger.debug(f"[{topic}] Skipping message {msg.get('id')}: priority {priority} < {self.min_priority}")
                continue

            # Tags filter (if configured)
            if self.target_tags:
                msg_tags = msg.get('tags', [])
                if not any(tag in msg_tags for tag in self.target_tags):
                    self.logger.debug(f"[{topic}] Skipping message {msg.get('id')}: tags {msg_tags} don't match {self.target_tags}")
                    continue

            filtered.append(msg)

        return filtered

    def get_topics(self):
        """Get list of configured topics

        Returns:
            list: List of topic names
        """
        return self.topics

    def get_state_manager(self):
        """Get the state manager instance

        Returns:
            StateManager: State manager instance
        """
        return self.state_manager
