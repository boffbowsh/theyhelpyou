from helpers import format_response, maybe_use_xray
from models import CommunityHub

maybe_use_xray()

def lambda_handler(event, context):
    if "queryStringParameters" not in event or "type" not in event["queryStringParameters"] or \
        event["queryStringParameters"]["type"] not in ["shielding", "vulnerable", "volunteering"]:
        return format_response({"error": "type must be one of 'shielding', 'vulnerable', or 'volunteering'"}, 400)

    results = {}
    for item in CommunityHub.scan():
        results[item.gss] = item.hub_url

    return format_response(results, 200)

if __name__ == "__main__":
    print(lambda_handler(
        {"queryStringParameters": {
            "type": "shielding",
        }},
        {}
    ))
