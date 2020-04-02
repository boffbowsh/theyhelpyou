import json
from fetch import lambda_handler

def _request_postcode(pcd):
    return json.loads(lambda_handler({"queryStringParameters": {"postcode": pcd}}, {}))

def test_not_found():
    res = lambda_handler({"queryStringParameters": {"postcode": "FOOBAR"}}, {})
    assert res["statusCode"] == "404"
    assert json.loads(res["body"]) == { "error": "Postcode not found" }
    assert res["headers"]["Content-Type"] == "application/json"

def test_full_record():
    res = _request_postcode("GU22 7QQ")
    assert res["homepage_url"] == "https://www.surreycc.gov.uk/"
    assert res["gss"] == "E10000030"
    assert res["name"] == "Surrey"
    assert res["phone"] == "0300 200 1008"
    assert res["hub_url"] == "https://www.surreycc.gov.uk/people-and-community/emergency-planning-and-community-safety/coronavirus/community-support/need-help"
    assert res["email"] == None
    assert res["date_collected"] == '31/03/2020'
    assert res["notes"] == None


def test_no_spaces():
    res = _request_postcode("GU227QQ")
    assert res["homepage_url"] == "https://www.surreycc.gov.uk/"

def test_county():
    res = _request_postcode("GU22 7QQ")
    assert res["homepage_url"] == "https://www.surreycc.gov.uk/"

def test_uta():
    res = _request_postcode("LU7 1AT")
    assert res["homepage_url"] == "https://www.centralbedfordshire.gov.uk/"

def test_cityoflondon():
    res = _request_postcode("EC2R 8AH")
    assert res["homepage_url"] == "https://www.cityoflondon.gov.uk/"

def test_london_borough():
    res = _request_postcode("KT2 5RD")
    assert res["homepage_url"] == "https://www.kingston.gov.uk/"

def test_metro_district():
    res = _request_postcode("NE1 4ST")
    assert res["homepage_url"] == "https://www.newcastle.gov.uk/"

def test_scottish_council_area():
    res = _request_postcode("G51 1EA")
    assert res["homepage_url"] == "https://www.glasgow.gov.uk/"

def test_nir_district():
    res = _request_postcode("BT4 3TT")
    assert res["homepage_url"] == "https://www.belfastcity.gov.uk/"

def test_welsh_uta():
    res = _request_postcode("CF10 1NS")
    assert res["homepage_url"] == "https://www.cardiff.gov.uk/"
