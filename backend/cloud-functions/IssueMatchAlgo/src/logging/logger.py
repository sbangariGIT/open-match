import os
from dotenv import load_dotenv
from slack import WebClient


class Logger:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.slack_client = WebClient(os.getenv('SLACK_BOT_TOKEN'))

    def notify_slack(self, message, level="INFO"):
        """
        Sends a message to Slack with a specific severity level.
        """
        try:
            formatted_message = f"[{level}] {message}"
            self.debug_print(f"Sending Slack Message: {formatted_message}")
            self.slack_client.chat_postMessage(
                channel='monitor-cloud',
                text=formatted_message
            )
        except Exception as e:
            self.debug_print(f"Failed to send slack message: {e}")

    def info(self, message):
        """
        Logs an informational message.
        """
        self.notify_slack(message, level="INFO")

    def warning(self, message):
        """
        Logs a warning message.
        """
        self.notify_slack(message, level="WARNING")

    def severe(self, message):
        """
        Logs a severe (critical) message.
        """
        self.notify_slack(message, level="SEVERE")

    def debug_print(self, message, level="INFO"):
        """
        Prints debug information to the console.
        """
        formatted_message = f"[{level}] {message}"
        print(formatted_message)


central_logger = Logger()