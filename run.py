import base64
import json
import os

from dotenv import load_dotenv
from discord_alerts import discord_alert

load_dotenv()

test_message = {
    "channel-name": os.environ.get("TEST_CHANNEL_NAME"),
    "message": "Hello, world!",
    "link": "https://youtu.be/dQw4w9WgXcQ?si=hMjJQuGl_OMZcitA",
    "fields": [
        {
            "name": "field name",
            "value": "field value",
            "inline": True
        }
    ]
}
# when using this test message as a json, make sure you update uppercase True to lowercase true, as uppercase True is only for python not json

base64_message = base64.b64encode(json.dumps(test_message).encode("utf-8"))
discord_alert({"data": base64_message}, None)
