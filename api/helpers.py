import json

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
