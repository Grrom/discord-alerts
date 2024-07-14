import base64
import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()

ALERTS_WEBHOOK_URL = os.getenv("ALERTS_WEBHOOK_URL")
BASE_WEBHOOK_URL = "https://discord.com/api/webhooks"

def discord_alert(event):
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
    if ALERTS_WEBHOOK_URL is None:
        print("alerts webhook url is missing")
        return ALERTS_WEBHOOK_URL, {"content": f"alerts webhook url is missing"}

    webhook_id = request_body.get("webhook-id")
    if webhook_id is None:
        print(f"webhook id is missing: {request_body}")
        return ALERTS_WEBHOOK_URL, {"content": f"webhook id is missing: {request_body}"}
    
    webhook_token = request_body.get("webhook-token")
    if webhook_token is None:
        print(f"webhook token is missing: {request_body}")
        return ALERTS_WEBHOOK_URL, {"content": f"webhook token is missing: {request_body}"
    }

    webhook_url = f"{BASE_WEBHOOK_URL}/{webhook_id}/{webhook_token}"

    content = request_body.get("content") or "no content"
    embeds = request_body.get("embeds") or []
    attachments = request_body.get("attachments") or []

    body = {"content": content, "embeds": embeds, "attachments": attachments}
    return webhook_url, body