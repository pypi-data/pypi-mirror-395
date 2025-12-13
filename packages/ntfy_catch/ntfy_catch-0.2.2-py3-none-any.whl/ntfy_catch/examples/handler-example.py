#!/usr/bin/env python3
"""
Example action handler for ntfy-catch

This script receives ntfy messages as JSON on stdin and performs actions based on
message attributes like priority, tags, and content.

Customize this script to implement your own actions:
- Execute shell commands
- Make HTTP requests
- Process message data
- Log/notify to other systems
- Store to database
- etc.

Exit codes:
  0 = Success (message will be marked as processed)
  Non-zero = Failure (message will be reprocessed on next run)
"""
import json
import sys
import subprocess
import logging
import os
from datetime import datetime

# Import AI classifier from ntfy_catch package
try:
    from ntfy_catch.ai_classifier import classify_message
except ImportError:
    # Fallback if package not installed - add src to path
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
    from ntfy_catch.ai_classifier import classify_message

# Configuration: Key to extract from JSON message content
TRANSCRIPT_KEY = 'transcript'

# Timestamp tracking file
TIMESTAMP_FILE = os.path.expanduser('~/.ntfy-catch-last-timestamp')

# Setup logging for handler with file output
log_file = os.path.expanduser('~/ntfy-catch-handler.log')
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] HANDLER: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)


def get_last_timestamp():
    """Read the last processed message timestamp"""
    try:
        if os.path.exists(TIMESTAMP_FILE):
            with open(TIMESTAMP_FILE, 'r') as f:
                return int(f.read().strip())
    except (ValueError, IOError):
        pass
    return None


def save_timestamp(timestamp):
    """Save the current message timestamp"""
    try:
        with open(TIMESTAMP_FILE, 'w') as f:
            f.write(str(timestamp))
    except IOError as e:
        logger.warning(f"Failed to save timestamp: {e}")


def format_time_delta(seconds):
    """Format time delta in human-readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        return f"{days}d {hours}h"


def main():
    """Main handler entry point"""
    try:
        # Read message from stdin
        message = json.load(sys.stdin)

        # Extract message attributes
        topic = message.get('topic', 'unknown')
        msg_id = message.get('id', 'unknown')
        priority = message.get('priority', 3)
        tags = message.get('tags', [])
        title = message.get('title', '')
        text = message.get('message', '')
        click_url = message.get('click', '')
        msg_time = message.get('time', 0)

        # Calculate time delta from last message
        last_time = get_last_timestamp()
        if last_time and msg_time:
            time_delta = msg_time - last_time
            delta_str = format_time_delta(time_delta)
            logger.info(f"Processing message from topic '{topic}': {msg_id} (Δt: {delta_str})")
        else:
            logger.info(f"Processing message from topic '{topic}': {msg_id}")

        # Try to parse message content as JSON and extract transcript
        EXTRACTED_MESSAGE = text  # Default to original text
        if text:
            try:
                # Attempt to parse message as JSON
                message_json = json.loads(text)
                # Extract the configured key
                extracted = message_json.get(TRANSCRIPT_KEY)
                if extracted:
                    EXTRACTED_MESSAGE = extracted
                    logger.info(f"Extracted '{TRANSCRIPT_KEY}': {EXTRACTED_MESSAGE}")
                else:
                    logger.debug(f"No '{TRANSCRIPT_KEY}' field found in message JSON, using original text")
            except (json.JSONDecodeError, TypeError):
                # Not JSON or invalid JSON - use original text
                logger.debug("Message is not JSON, using as plain text")

        # Save current timestamp for next delta calculation
        if msg_time:
            save_timestamp(msg_time)

        # Example: High priority messages
        if priority >= 4:
            logger.info(f"High priority alert: {title}")
            # Example: Send desktop notification (requires notify-send)
            # subprocess.run(['notify-send', f'Critical: {title}', text], check=False)

        # Example: Tag-based actions
        if 'deploy' in tags:
            logger.info("Deploy tag detected - would trigger deployment")
            # Example: Trigger deployment script
            # subprocess.run(['/usr/local/bin/deploy.sh', topic], check=True)

        if 'alert' in tags:
            logger.info("Alert tag detected")
            # Example: Send to alerting system
            # send_to_pagerduty(message)

        if 'http' in tags and click_url:
            logger.info(f"HTTP tag detected - would POST to {click_url}")
            # Example: Make HTTP request
            # import requests
            # requests.post(click_url, json=message, timeout=10)

        # Example: Topic-based routing
        if topic == 'monitoring':
            logger.info("Monitoring message - would update dashboard")
            # Example: Update monitoring dashboard
            # update_grafana_annotation(message)

        if topic == 'alerts':
            logger.info("Alert message - would notify on-call")
            # Example: Notify on-call engineer
            # notify_oncall(message)

        # Example: Log to syslog
        logger.info(f"Message content: {EXTRACTED_MESSAGE[:100] if EXTRACTED_MESSAGE else '(empty)'}")
        # subprocess.run(['logger', f"ntfy[{topic}]: {EXTRACTED_MESSAGE}"], check=False)


        logger.info(f"...          processing message {msg_id}")
        if (topic == "zapier_carbon") and len(EXTRACTED_MESSAGE) > 3:
            # Call AI classifier
            success, classification, api_response = classify_message(EXTRACTED_MESSAGE)

            if success:
                logger.info(f"AI Classification: {classification}")
                # TODO: Add your custom logic based on classification
                # Example:
                if classification == "CALENDAR":
                    print("================>> CALENDAR")
                      # Add to calendar system
                    pass
                elif classification == "TASK":
                #     # Add to task management system
                    print("================>> TASK")
                    pass
                elif classification == "MEMO":
                #     # Save to notes/memo system
                    print("================>> MEMO")
                    pass
                elif classification == "OTHER":
                #     # Handle other messages
                    print("================>> other")
                    pass
            else:
                logger.warning(f"AI classification failed: {api_response.get('error', 'Unknown error')}")

        # Example: Store to file
        # with open('/var/log/ntfy-catch/messages.log', 'a') as f:
        #     f.write(f"{msg_id}|{topic}|{priority}|{text}\n")

        logger.info(f"Successfully processed message {msg_id}")
        sys.exit(0)  # Success

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        sys.exit(1)  # Failure

    except Exception as e:
        logger.error(f"Handler error: {e}", exc_info=True)
        sys.exit(1)  # Failure


if __name__ == '__main__':
    main()
