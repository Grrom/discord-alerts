import base64
import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()

BASE_WEBHOOK_URL = "https://discord.com/api/webhooks"

SUPPORTED_CHANNELS = {
    "alerts": os.getenv("ALERTS_WEBHOOK_URL"),
}
ALERTS_WEBHOOK_URL = SUPPORTED_CHANNELS["alerts"]
NOT_RICK_ROLL = "https://youtu.be/dQw4w9WgXcQ?si=hMjJQuGl_OMZcitA"

def discord_alert(event, _):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """

    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    request_body = json.loads(pubsub_message)

    url, body = _get_alert(request_body)

    request = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=body,
    )
    request.raise_for_status()
    return "done"


def _get_alert(request_body):
    channel_name = request_body.get("channel-name")
    if channel_name not in SUPPORTED_CHANNELS.keys():
        return ALERTS_WEBHOOK_URL, {"content": f"channel {channel_name} is not supported, please use one of `{', '.join(list(SUPPORTED_CHANNELS.keys()))}`"}
    
    webhook_url = SUPPORTED_CHANNELS[channel_name]

    message = request_body.get("message") or ""

    fields_param = request_body.get("fields") or []
    fields = []
    for field in fields_param:
        fields.append(
            {
                "name": field.get("name") or "",
                "value": field.get("value") or "",
                "inline": field.get("inline") or False,
            }
        )

    embeds = [
        {
            "title": message,
            "type": "rich",
            "url": request_body.get("link") or NOT_RICK_ROLL,
            "fields": fields,
        }
    ]

    attachments = request_body.get("attachments") or []

    body = {"content": "", "embeds": embeds, "attachments": attachments}
    return webhook_url, body