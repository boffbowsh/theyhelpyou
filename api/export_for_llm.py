from helpers import format_response, maybe_use_xray
from models import CommunityHub

maybe_use_xray()

def lambda_handler(event, context):
    if "queryStringParameters" not in event or "type" not in event["queryStringParameters"]:
        return format_response({"error": "type must be one of 'shielding', 'vulnerable', or 'volunteering'"}, 400)

    if event["queryStringParameters"]["type"] not in ["shielding", "vulnerable", "volunteering"]:
        return format_response({"error": "type must be one of 'shielding', 'vulnerable', or 'volunteering'"}, 400)

    filters = []
    if "nation" in event["queryStringParameters"]:
        if event["queryStringParameters"]["nation"] not in ["E", "N", "S", "W"]:
            return format_response({"error": "nation must be one of 'E', 'N', 'S' or 'W'"}, 400)
        else:
            filters.append(CommunityHub.gss.startswith(event["queryStringParameters"]["nation"]))

    results = {}
    for item in CommunityHub.scan(*filters):
        results[item.gss] = item.hub_url

    return format_response(results, 200)

if __name__ == "__main__":
    print(lambda_handler(
        {"queryStringParameters": {
            "type": "shielding",
            "nation": "E",
        }},
        {}
    ))
