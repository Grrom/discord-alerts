import base64
import json

from discord_alerts import discord_alert

test_message = {
    "webhook-id": "1234567890",
    "webhook-token": "abcdefg",
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
                    "inline": True
                }
            ]
        }
    ]
}

base64_message = base64.b64encode(json.dumps(test_message).encode("utf-8"))
discord_alert({"data": base64_message})
