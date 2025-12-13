#!/usr/bin/env python3
"""
AI message classifier using OpenRouter API

Classifies messages into categories: CALENDAR, TASK, MEMO, or OTHER
"""
import requests
import json
import os
import logging

logger = logging.getLogger(__name__)

# OpenRouter API configuration
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "x-ai/grok-4.1-fast"

# Classification system prompt
SYSTEM_PROMPT = """You are a very responsible classifier. For every user message, output exactly one uppercase token and nothing else: CALENDAR, TASK, MEMO, or OTHER. Rules:
- CALENDAR: scheduling intent or an event/reminder with a date/time or scheduling words (e.g., "tomorrow", "at 3pm", "on Jan 5", "meeting", "appointment", "schedule", "remind me on"). If both scheduling and other intent appear, choose CALENDAR.
- TASK: actionable instruction or to‑do without specific scheduling (imperative verbs like "buy", "write", "call", "create", "finish", requests to add a task). If both task and memo appear, choose TASK.
- MEMO: factual note or something meant to be remembered (phrases like "remember that", "note", personal info to keep, facts).
- OTHER: none of the above (questions, casual chat, ambiguous content).

Tie-breakers: prefer CALENDAR over TASK over MEMO. Always return only the tag (no punctuation, no explanation).

Examples:
"Meeting with Alice tomorrow at 10am" -> CALENDAR
"Buy groceries" -> TASK
"Remember my passport number: 1234" -> MEMO
"What's the weather like?" -> OTHER
"""


def classify_message(message_text, timeout=10):
    """
    Classify a message using OpenRouter API

    Args:
        message_text: The message content to classify
        timeout: API request timeout in seconds (default: 10)

    Returns:
        tuple: (success: bool, classification: str, raw_response: dict)
            - success: True if API call succeeded
            - classification: One of CALENDAR, TASK, MEMO, OTHER, or None on error
            - raw_response: Full API response dict or error dict
    """
    api_key = os.environ.get('OPENROUTER_API_KEY')

    # If not in environment, try reading from ~/.openrouter.key
    if not api_key:
        key_file = os.path.expanduser('~/.openrouter.key')
        try:
            if os.path.isfile(key_file):
                with open(key_file, 'r') as f:
                    api_key = f.read().strip()
                    if api_key:
                        logger.debug(f"Loaded API key from {key_file}")
        except Exception as e:
            logger.warning(f"Failed to read API key from {key_file}: {e}")

    if not api_key:
        logger.error("OPENROUTER_API_KEY environment variable not set and ~/.openrouter.key not found")
        return False, None, {"error": "Missing API key"}

    if not message_text or not message_text.strip():
        logger.warning("Empty message text provided for classification")
        return False, "OTHER", {"error": "Empty message"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message_text
            }
        ]
    }

    try:
        logger.info(f"Classifying message: {message_text[:100]}...")
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=timeout
        )
        response.raise_for_status()

        response_data = response.json()

        # Extract classification from response
        try:
            classification = response_data['choices'][0]['message']['content'].strip()

            # Validate classification
            valid_classes = ['CALENDAR', 'TASK', 'MEMO', 'OTHER']
            if classification not in valid_classes:
                logger.warning(f"Unexpected classification: {classification}, defaulting to OTHER")
                classification = 'OTHER'

            logger.info(f"Classification result: {classification}")
            return True, classification, response_data

        except (KeyError, IndexError) as e:
            logger.error(f"Failed to extract classification from response: {e}")
            return False, None, response_data

    except requests.exceptions.Timeout:
        logger.error(f"OpenRouter API request timed out after {timeout}s")
        return False, None, {"error": "Timeout"}

    except requests.exceptions.RequestException as e:
        logger.error(f"OpenRouter API request failed: {e}")
        return False, None, {"error": str(e)}

    except Exception as e:
        logger.error(f"Unexpected error during classification: {e}", exc_info=True)
        return False, None, {"error": str(e)}


def classify_message_simple(message_text, timeout=10):
    """
    Simplified classification function that returns just the classification

    Args:
        message_text: The message content to classify
        timeout: API request timeout in seconds (default: 10)

    Returns:
        str: Classification (CALENDAR, TASK, MEMO, OTHER) or None on error
    """
    success, classification, _ = classify_message(message_text, timeout)
    return classification if success else None
