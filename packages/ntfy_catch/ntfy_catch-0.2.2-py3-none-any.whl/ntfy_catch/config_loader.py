"""Configuration loader for ntfy-catch"""
import configparser
import os
import sys
from pathlib import Path


class ConfigLoader:
    """Loads and validates INI configuration for ntfy_catch"""

    REQUIRED_FIELDS = {
        'server': ['base_url'],
        'polling': ['topics'],
        'actions': ['handler_script']
    }

    DEFAULTS = {
        'state': {
            'state_dir': './state'
        },
        'logging': {
            'log_level': 'INFO',
            'log_dir': './logs'
        },
        'actions': {
            'handler_timeout': '30',
            'continue_on_error': 'true'
        },
        'filters': {
            'min_priority': '1',
            'target_tags': ''
        }
    }

    def __init__(self, config_path):
        """Initialize config loader with path to INI file"""
        self.config_path = config_path
        self.config = None

    def load(self):
        """Load and validate configuration

        Returns:
            configparser.ConfigParser: Validated configuration object

        Raises:
            SystemExit: If configuration is invalid
        """
        if not os.path.exists(self.config_path):
            self._error(f"Configuration file not found: {self.config_path}")

        self.config = configparser.ConfigParser()
        try:
            self.config.read(self.config_path)
        except configparser.Error as e:
            self._error(f"Failed to parse configuration: {e}")

        # Apply defaults
        self._apply_defaults()

        # Validate required fields
        self._validate_required_fields()

        # Validate handler script
        self._validate_handler_script()

        # Validate topics
        self._validate_topics()

        return self.config

    def _apply_defaults(self):
        """Apply default values for missing optional fields"""
        for section, defaults in self.DEFAULTS.items():
            if not self.config.has_section(section):
                self.config.add_section(section)

            for key, value in defaults.items():
                if not self.config.has_option(section, key):
                    self.config.set(section, key, value)

    def _validate_required_fields(self):
        """Validate that all required fields are present"""
        missing = []

        for section, fields in self.REQUIRED_FIELDS.items():
            if not self.config.has_section(section):
                missing.append(f"Missing section: [{section}]")
                continue

            for field in fields:
                if not self.config.has_option(section, field):
                    missing.append(f"Missing field: [{section}] {field}")

        if missing:
            self._error("Configuration validation failed:\n  " + "\n  ".join(missing))

    def _validate_handler_script(self):
        """Validate that handler script exists and is executable"""
        handler_script = self.config.get('actions', 'handler_script')

        if not handler_script or handler_script.strip() == '':
            self._error("Handler script path is empty")

        handler_path = Path(handler_script).expanduser()

        if not handler_path.exists():
            self._error(
                f"Handler script not found: {handler_script}\n"
                f"  Please create the handler script or update the configuration"
            )

        if not os.access(handler_path, os.X_OK):
            self._error(
                f"Handler script is not executable: {handler_script}\n"
                f"  Run: chmod +x {handler_script}"
            )

    def _validate_topics(self):
        """Validate topics configuration"""
        topics = self.config.get('polling', 'topics')

        if not topics or topics.strip() == '':
            self._error("No topics configured in [polling] topics")

        # Check for valid topic names (basic validation)
        topic_list = [t.strip() for t in topics.split(',')]
        for topic in topic_list:
            if not topic:
                self._error("Empty topic name in topics list")
            if '/' in topic:
                self._error(f"Invalid topic name '{topic}': topic names should not contain '/'")

    def _error(self, message):
        """Print error message and exit"""
        print(f"Configuration Error: {message}", file=sys.stderr)
        sys.exit(1)
