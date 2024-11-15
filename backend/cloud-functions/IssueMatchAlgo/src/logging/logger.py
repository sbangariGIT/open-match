import os
from dotenv import load_dotenv
from slack import WebClient


class Logger:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.slack_client = WebClient(os.getenv('SLACK_BOT_TOKEN'))

    def notify_slack(self, message):
        self.debug_print(f"Sending Slack Message: {message}")
        message = message
        self.slack_client.chat_postMessage(
        channel='monitor-cloud',
        text=message)

    def debug_print(self, message):
        print(message)


central_logger = Logger()