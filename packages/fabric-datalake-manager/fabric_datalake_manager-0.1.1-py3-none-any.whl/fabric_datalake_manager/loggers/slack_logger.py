import logging
import requests

from fabric_datalake_manager.interfaces.log_interface import ILog

# ==========================================
# Slack Logger Implementation
# ==========================================


class SlackLogger(ILog):
    def __init__(self, webhook_url: str):
        """
        Automatically creates and configures a LogConfiguration instance.
        If no webhook_url is provided, it looks for one in environment variables.
        """
        self.logger = logging.getLogger(__name__)
        self.webhook_url = webhook_url

    def log(self, message: str, **kwargs):
        if not self.webhook_url:
            self.logger.error("[SlackLogger] Webhook URL not configured.")
            return

        try:
            response = requests.post(self.webhook_url, json={
                                     "text": message}, timeout=5)
            if response.status_code != 200:
                self.logger.error(
                    f"[SlackLogger] Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            self.logger.exception(
                f"[SlackLogger] Exception sending message: {e}")
