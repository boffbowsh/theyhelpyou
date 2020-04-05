import base64
import json
import os

from helpers import format_response
from models import CommunityHub

from slack_webhook import Slack
from pynamodb.models import DoesNotExist

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# xray_recorder.configure()
# patch_all()

slack = Slack(url=os.environ.get("WEBHOOK_URL"))

def lambda_handler(event, context):
    print(event)
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

    if "gss" not in data:
        return format_response("GSS code must be supplied", 400)

    if "pcd" not in data:
        return format_response("Postcode must be supplied", 400)

    try:
        hub = CommunityHub.get(data["gss"])
    except DoesNotExist:
        return format_response("GSS code not found", 404)

    fields = [
            {
                "title": "Name",
                "value": hub.name,
                "short": True,
            },
            {
                "title": "Homepage URL",
                "value": hub.homepage_url,
                "short": True,
            },
            {
                "title": "Phone Number",
                "value": hub.phone,
                "short": True,
            },
            {
                "title": "Date Collected",
                "value": hub.date_collected,
                "short": True,
            },
            {
                "title": "Hub URL",
                "value": hub.hub_url,
                "short": False,
            },
            {
                "title": "Email",
                "value": hub.email,
                "short": True,
            },
            {
                "title": "Notes",
                "value": hub.notes,
                "short": False,
            }
        ]

    if "message" in data:
        fields.append({
            "title": "Message from user",
            "value": data["message"],
            "short": False,
        })

    msg = "Problem reported with the data for {}, from postcode {}".format(hub.name, data["pcd"])
    slack.post(
        text=msg,
        attachments=[{
            "fallback": msg,
            "text": "*Current data:*",
            "fields": fields,
        }],
    )



if __name__ == "__main__":
    lambda_handler({"body": json.dumps({"gss": "E10000030", "message": "Test from Paul"}), "isBase64Encoded": False}, {})
