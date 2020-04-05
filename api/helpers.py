import json
import os

def format_response(data, status):
    return {
        "cookies": [],
        "isBase64Encoded": False,
        "statusCode": str(status),
        "body": json.dumps(data),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET",
        },
    }

def maybe_use_xray():
    if "AWS_XRAY_DAEMON_ADDRESS" in os.environ:
        from aws_xray_sdk.core import xray_recorder
        from aws_xray_sdk.core import patch_all

        xray_recorder.configure()
        patch_all()
