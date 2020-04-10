import base64
import json
import os

from helpers import format_response, maybe_use_xray
from models import CommunityHub

from slack_webhook import Slack
from pynamodb.models import DoesNotExist

maybe_use_xray()

slack = Slack(url=os.environ.get("WEBHOOK_URL"))

def lambda_handler(event, context):
    if "body" not in event:
        return format_response("Body not supplied", 400)

    try:
        if event["isBase64Encoded"]:
            data = json.loads(base64.b64decode(event["body"]))
        else:
            data = json.loads(event["body"])
    except:
        raise
        return format_response("Body must be JSON", 400)

    if "token" not in data or data["token"] != os.environ.get("SECRET_TOKEN"):
        return format_response("Unauthorized", 403)

    if "gss" not in data:
        return format_response("GSS code must be supplied", 400)

    if "key" not in data:
        return format_response("Attribute must be supplied", 400)

    if "val" not in data:
        return format_response("Value must be supplied", 400)

    try:
        hub = CommunityHub.get(data["gss"])
    except DoesNotExist:
        return format_response("GSS code not found", 404)

    if data["key"] in hub.attribute_values:
        old_value = hub.attribute_values[data["key"]]
    else:
        old_value = ""

    hub.attribute_values[data["key"]] = data["val"]
    hub.save()

    slack_fields = [
            {
                "title": "GSS",
                "value": data["gss"],
                "short": True,
            },
            {
                "title": "Attribute",
                "value": data["key"],
                "short": True,
            },
            {
                "title": "Was",
                "value": old_value,
                "short": True,
            },
            {
                "title": "Now",
                "value": hub.attribute_values[data["key"]],
                "short": True,
            },
    ]

    msg = "Data updated for {}".format(hub.name)
    slack.post(
        text=msg,
        attachments=[{
            "fallback": msg,
            "fields": slack_fields,
        }],
    )


if __name__ == "__main__":
    print(lambda_handler({
        "body": json.dumps({
            "token": os.environ.get("SECRET_TOKEN"),
            "gss": "E09000015",
            "key": "notes",
            "val": "Online form",
        }),
        "isBase64Encoded": False,
    }, {}))
