import json
import re

from helpers import format_response, maybe_use_xray
from models import CommunityHub, Postcode

from pynamodb.models import DoesNotExist

maybe_use_xray()

def get_postcode_from_event(e):
    if "queryStringParameters" in e and "postcode" in e["queryStringParameters"]:
        pcd = (
            e["queryStringParameters"]["postcode"].replace(" ", "").lstrip("/").upper()
        )
        try:
            return Postcode.get(pcd)
        except DoesNotExist:
            return None
    else:
        return None


def get_gss(pcd):
    order = [pcd.oscty, pcd.oslaua]
    for gss in order:
        if re.match(r"[EWSN]9{8}", gss):
            continue
        return gss

    return None


def lambda_handler(event, context):
    pcd = get_postcode_from_event(event)
    if not pcd:
        return format_response({"error": "Postcode not found"}, 404)

    gss = get_gss(pcd)
    if not gss:
        return format_response({"error": "No data found for postcode"}, 404)

    try:
        hub = CommunityHub.get(gss)
        return format_response(hub.attribute_values, 200)
    except DoesNotExist:
        return format_response({"error": "No data found for this area"}, 404)

if __name__ == "__main__":
    print(lambda_handler({"queryStringParameters": {"postcode": "rg120uz"}}, {}))
