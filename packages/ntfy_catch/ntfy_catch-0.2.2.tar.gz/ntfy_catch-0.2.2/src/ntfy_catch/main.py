#!/usr/bin/env python3
"""
ntfy_catch: A cron-driven ntfy topic watcher

Polls ntfy server topics for new messages and dispatches them to an external handler script.
"""
import argparse
import sys
from pathlib import Path

from ntfy_catch.config_loader import ConfigLoader
from ntfy_catch.logger_setup import setup_logger, get_logger
from ntfy_catch.poller import NtfyPoller
from ntfy_catch.action_dispatcher import ActionDispatcher

import os
import shutil
try:
    from importlib.resources import files
except ImportError:
    # Python < 3.9 fallback
    from importlib_resources import files

def init_config():
    """Initialize configuration by copying example files to ~/.config/ntfy_catch/"""
    config_dir = Path.home() / '.config' / 'ntfy_catch'
    config_file = config_dir / 'ntfy_catch.ini'
    handler_file = config_dir / 'handler.py'

    # Create config directory
    config_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {config_dir}")

    # Copy example config if it doesn't exist
    if config_file.exists():
        print(f"Config file already exists: {config_file}")
    else:
        try:
            # Get example from package data
            example_files = files('ntfy_catch') / 'examples' / 'ntfy-catch.ini.example'
            config_file.write_text(example_files.read_text())
            print(f"Created config file: {config_file}")
        except Exception as e:
            print(f"Warning: Could not copy example config: {e}")
            print(f"Please manually create {config_file}")

    # Copy example handler if it doesn't exist
    if handler_file.exists():
        print(f"Handler file already exists: {handler_file}")
    else:
        try:
            # Get example from package data
            example_handler = files('ntfy_catch') / 'examples' / 'handler-example.py'
            handler_file.write_text(example_handler.read_text())
            os.chmod(handler_file, 0o755)  # Make executable
            print(f"Created handler file: {handler_file}")
            print(f"Made handler executable")
        except Exception as e:
            print(f"Warning: Could not copy example handler: {e}")
            print(f"Please manually create {handler_file}")

    print("\nNext steps:")
    print(f"1. Edit config: {config_file}")
    print(f"   - Set your ntfy server URL")
    print(f"   - Configure topics to monitor")
    print(f"2. Customize handler: {handler_file}")
    print(f"3. Set up OpenRouter API key (for AI classification):")
    print(f"   - Get key from https://openrouter.ai/")
    print(f"   - Save to ~/.openrouter.key or set OPENROUTER_API_KEY env var")
    print(f"4. Run: ntfy_catch")

def main():
    """Main entry point for ntfy_catch"""
    parser = argparse.ArgumentParser(
        description='Poll ntfy topics and dispatch messages to handler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --init-config              # First-time setup
  %(prog)s                            # Use default config
  %(prog)s --config /path/to/config.ini
  %(prog)s --topic alerts             # Poll specific topic
  %(prog)s --dry-run                  # Test without executing
        """
    )
    parser.add_argument(
        '--config',
        default=os.path.expanduser(f'~/.config/ntfy_catch/ntfy_catch.ini'),
        help='Path to configuration file (default: ~/.config/ntfy_catch/ntfy_catch.ini)'
    )
    parser.add_argument(
        '--topic',
        help='Poll specific topic only (overrides config)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be processed without executing handler'
    )
    parser.add_argument(
        '--init-config',
        action='store_true',
        help='Initialize configuration files in ~/.config/ntfy_catch/'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='ntfy_catch 1.0.0'
    )

    args = parser.parse_args()

    # Handle --init-config
    if args.init_config:
        init_config()
        sys.exit(0)

    # Load configuration
    try:
        config_loader = ConfigLoader(args.config)
        config = config_loader.load()
    except SystemExit:
        # ConfigLoader already printed error message
        sys.exit(1)

    # Setup logging
    logger = setup_logger(config)

    if args.dry_run:
        logger.info("=== DRY RUN MODE ===")

    logger.info("Starting ntfy_catch")

    # Initialize components
    poller = NtfyPoller(config)

    dispatcher = None
    if not args.dry_run:
        dispatcher = ActionDispatcher(
            config.get('actions', 'handler_script'),
            timeout=config.getint('actions', 'handler_timeout', fallback=30),
            continue_on_error=config.getboolean('actions', 'continue_on_error', fallback=True)
        )

    # Determine which topics to poll
    if args.topic:
        topics = [args.topic]
        logger.info(f"Polling single topic: {args.topic}")
    else:
        topics = poller.get_topics()
        logger.info(f"Polling {len(topics)} topic(s): {', '.join(topics)}")

    # Poll each topic
    total_messages = 0
    total_success = 0
    total_failed = 0

    for topic in topics:
        try:
            messages = poller.poll_topic(topic)

            for msg in messages:
                total_messages += 1
                msg_id = msg.get('id', 'unknown')
                msg_time = msg.get('time', 0)

                if args.dry_run:
                    msg_text = msg.get('message', '')[:50]
                    logger.info(
                        f"[{topic}] [DRY RUN] Would process message {msg_id}: \"{msg_text}\""
                    )
                    # In dry run, always update timestamp
                    poller.get_state_manager().update_last_timestamp(topic, msg_time)
                    total_success += 1
                else:
                    # Dispatch to external handler
                    success, returncode, output = dispatcher.dispatch(msg)

                    if success:
                        # Update timestamp only on success
                        poller.get_state_manager().update_last_timestamp(topic, msg_time)
                        total_success += 1
                    else:
                        total_failed += 1
                        logger.warning(
                            f"[{topic}] Message {msg_id} NOT marked as processed (will retry next run)"
                        )

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            sys.exit(130)
        except Exception as e:
            logger.error(f"[{topic}] Error processing topic: {e}", exc_info=True)
            # Continue to next topic
            continue

    # Summary
    if total_messages > 0:
        logger.info(
            f"Completed: {total_messages} message(s) processed "
            f"({total_success} success, {total_failed} failed)"
        )
    else:
        logger.info("Completed: No new messages")

    # Exit with appropriate code
    if total_failed > 0 and not config.getboolean('actions', 'continue_on_error', fallback=True):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
