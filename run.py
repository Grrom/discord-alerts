import base64
import json
import os

from dotenv import load_dotenv
from discord_alerts import discord_alert

load_dotenv()

test_message = {
    "webhook-id": os.environ.get("TEST_WEBHOOK_ID"),
    "webhook-token": os.environ.get("TEST_WEBHOOK_TOKEN"),
    "content": "Hello, world!",
    "embeds": [
        {
            "title": "Incident Alert",
            "type": "rich",
            "url": "https://youtu.be/dQw4w9WgXcQ?si=hMjJQuGl_OMZcitA",
            "description": "test notif",
            "fields": [
                {
                    "name": "field name",
                    "value": "field value",
                    "inline": True,
                }
            ]
        }
    ]
}
# when using this test message as a json, make sure you update True to true, as True is only for python

base64_message = base64.b64encode(json.dumps(test_message).encode("utf-8"))
discord_alert({"data": base64_message}, None)
