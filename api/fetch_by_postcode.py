import boto3
import json
import re

from models import CommunityHub, Postcode

from pynamodb.models import DoesNotExist


def get_postcode_from_event(e):
    if "queryStringParameters" in e and "postcode" in e["queryStringParameters"]:
        pcd = e["queryStringParameters"]["postcode"].replace(' ', '').lstrip('/').upper()
        try:
            return Postcode.get(pcd)
        except DoesNotExist:
            return None
    else:
        return None

def get_gss(pcd):
    order = [pcd.oscty, pcd.oslaua]
    for gss in order:
        if re.match(r'[EWSN]9{8}', gss):
            continue
        return gss

    return None

def format_response(data, status):
    return {
            "cookies": [],
            "isBase64Encoded": False,
            "statusCode": str(status),
            "body": json.dumps(data),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*',
                "Access-Control-Allow-Methods": "OPTIONS,GET"
            }
        }

def lambda_handler(event, context):
    pcd = get_postcode_from_event(event)
    if not pcd:
        return format_response({"error": "Postcode not found"}, 404)

    gss = get_gss(pcd)
    if not gss:
        return format_response({"error": "No data found for postcode"}, 404)

    try:
        hub = CommunityHub.get(gss)
        return format_response(hub.attributes(), 200)
    except DoesNotExist:
        return format_response({"error": "No data found for this area"}, 404)
