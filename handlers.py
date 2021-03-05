import requests
from logging import StreamHandler, LogRecord


class SlackHandler(StreamHandler):
    def __init__(self, url):
        super().__init__()
        self.web_hook = url

    def format(self, record: LogRecord) -> str:
        # TODO Replace this with an override formatter
        return super().format(record)

    def emit(self, record: LogRecord) -> None:
        msg = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": self.format(record)
                    }
                }
            ]
        }
        requests.post(self.web_hook, json=msg)
