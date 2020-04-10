import base64
import csv
import json
import os
from urllib.request import urlopen

from helpers import format_response, maybe_use_xray
from models import CommunityHub

maybe_use_xray()

CommunityHub.create_table(wait=True)

def lambda_handler(event, context):
    if "body" not in event:
        return format_response("Unauthorized", 403)
    else:
        if event["isBase64Encoded"]:
            data = json.loads(base64.b64decode(event["body"]))
        else:
            data = json.loads(event["body"])
        if "token" not in data or data["token"] != os.environ.get("SECRET_TOKEN"):
            return format_response("Unauthorized", 403)

    resp = urlopen(
        "https://docs.google.com/spreadsheets/d/1uwcEbPob7EcOKBe_H-OiYEP3fITjbZH-ccpc81fMO7s/export?gid=0&format=csv&id=1uwcEbPob7EcOKBe_H-OiYEP3fITjbZH-ccpc81fMO7s"
    )

    if resp.status == 200:
        lines = [str(l, "utf-8") for l in resp.read().splitlines()]
        c = csv.DictReader(lines[1:])
        with CommunityHub.batch_write() as batch:
            for r in c:
                record = CommunityHub(r["gss"])
                for k, v in r.items():
                    if hasattr(CommunityHub, k):
                        record.attribute_values[k] = v

                batch.save(record)

    else:
        print("error fetching CSV {}".format(resp.status))

if __name__ == "__main__":
    lambda_handler({
        "body": json.dumps({"token": os.environ.get("SECRET_TOKEN")}),
        "isBase64Encoded": False,
    }, {})
