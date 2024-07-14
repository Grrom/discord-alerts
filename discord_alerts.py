import base64
import json
import os
import requests

supported_channels = {
    "alerts": os.getenv("ALERTS_URL"),
    "expen-sync": os.getenv("EXPENSYNC_URL")
}


def discord_alert(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """

    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    request_body = json.loads(pubsub_message)

    url, body = get_alert(request_body)

    request = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=body,
    )
    request.raise_for_status()
    return "done"


def get_alert(request_body):
    alerts_webhook_url = supported_channels["alerts"]
    if alerts_webhook_url is None:
        return alerts_webhook_url, {"content": f"alerts webhook url is missing"}

    channel_name = request_body.get("channel-name")
    if channel_name is None:
        return alerts_webhook_url, {"content": f"attempted to send alert but channel name was not passed"}

    webhook_url = supported_channels.get(channel_name)
    if webhook_url is None:
        supported_channel_names = ", ".join(str(element) for element in supported_channels.keys())
        return alerts_webhook_url, {"content": f"attempted to send alert to unsupported channel: `{channel_name}`, channels_supported: `{supported_channel_names}`"}

    content = request_body.get("content") or "no content"
    embeds = request_body.get("embeds") or []
    attachments = request_body.get("attachments") or []

    body = {"content": content, "embeds": embeds, "attachments": attachments}
    return webhook_url, body