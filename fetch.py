import boto3
import json
import re

from models import CommunityHub, Postcode

from pynamodb.models import DoesNotExist


def get_postcode_from_event(e):
    if "queryStringParameters" in e and "postcode" in e["queryStringParameters"]:
        pcd = e["queryStringParameters"]["postcode"].replace(' ', '').lstrip('/')
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

def format_hub(hub):
    d = {
            "gss": hub.gss,
            "name": hub.name,
            "homepage_url": hub.homepage_url,
            "email": hub.email,
            "hub_url": hub.hub_url,
            "phone": hub.phone,
            "date_collected": hub.date_collected,
            "notes": hub.notes
        }
    print(d)
    return d

def lambda_handler(event, context):
    print(event)
    pcd = get_postcode_from_event(event)
    if not pcd:
        return {
            "cookies": [],
            "isBase64Encoded": False,
            "statusCode": "404",
            "body": '{ "error": "Postcode not found" }',
            "headers": {
                "Content-Type": "application/json"
            }
        }

    gss = get_gss(pcd)
    if not gss:
        return {
            "cookies": [],
            "isBase64Encoded": False,
            "statusCode": "404",
            "body": '{ "error": "No data found for postcode" }',
            "headers": {
                "Content-Type": "application/json"
            }
        }

    try:
        hub = CommunityHub.get(gss)
        return json.dumps(format_hub(hub))
    except DoesNotExist:
        return {
            "isBase64Encoded": False,
            "statusCode": "404",
            "body": '{ "error": "No data found for this area" }',
            "headers": {
                "Content-Type": "application/json"
            }
        }


if __name__ == "__main__":
    e = {
        "path": "/GU22 7TBs",
        "httpMethod": "POST",
        "isBase64Encoded": True,
        "queryStringParameters": {
            "foo": "bar"
        },
        "multiValueQueryStringParameters": {
            "foo": [
            "bar"
            ]
        },
        "pathParameters": {
            "proxy": "/GU22 7TB"
        },
        "stageVariables": {
            "baz": "qux"
        },
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "max-age=0",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Host": "1234567890.execute-api.eu-west-2.amazonaws.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Custom User Agent String",
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "multiValueHeaders": {
            "Accept": [
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            ],
            "Accept-Encoding": [
            "gzip, deflate, sdch"
            ],
            "Accept-Language": [
            "en-US,en;q=0.8"
            ],
            "Cache-Control": [
            "max-age=0"
            ],
            "CloudFront-Forwarded-Proto": [
            "https"
            ],
            "CloudFront-Is-Desktop-Viewer": [
            "true"
            ],
            "CloudFront-Is-Mobile-Viewer": [
            "false"
            ],
            "CloudFront-Is-SmartTV-Viewer": [
            "false"
            ],
            "CloudFront-Is-Tablet-Viewer": [
            "false"
            ],
            "CloudFront-Viewer-Country": [
            "US"
            ],
            "Host": [
            "0123456789.execute-api.eu-west-2.amazonaws.com"
            ],
            "Upgrade-Insecure-Requests": [
            "1"
            ],
            "User-Agent": [
            "Custom User Agent String"
            ],
            "Via": [
            "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)"
            ],
            "X-Amz-Cf-Id": [
            "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA=="
            ],
            "X-Forwarded-For": [
            "127.0.0.1, 127.0.0.2"
            ],
            "X-Forwarded-Port": [
            "443"
            ],
            "X-Forwarded-Proto": [
            "https"
            ]
        },
        "requestContext": {
            "accountId": "123456789012",
            "resourceId": "123456",
            "stage": "prod",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "requestTime": "09/Apr/2015:12:34:56 +0000",
            "requestTimeEpoch": 1428582896000,
            "identity": {
            "cognitoIdentityPoolId": None,
            "accountId": None,
            "cognitoIdentityId": None,
            "caller": None,
            "accessKey": None,
            "sourceIp": "127.0.0.1",
            "cognitoAuthenticationType": None,
            "cognitoAuthenticationProvider": None,
            "userArn": None,
            "userAgent": "Custom User Agent String",
            "user": None
            },
            "path": "/prod/GU22 7TB",
            "resourcePath": "/{proxy+}",
            "httpMethod": "GET",
            "apiId": "1234567890",
            "protocol": "HTTP/1.1"
        }
    }

    print(lambda_handler(e, None))
