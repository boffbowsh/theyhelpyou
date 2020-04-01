from fetch import lambda_handler

def _request_postcode(pcd):
    return lambda_handler({"path": "/{}".format(pcd)}, {})

def test_not_found():
    res = _request_postcode("FOOBAR")
    assert res["statusCode"] == 404
    assert res["body"] == { "error": "Postcode not found" }
    assert res["headers"]["Content-Type"] == "application/json"

def test_full_record():
    res = _request_postcode("GU22 7QQ")
    assert res["statusCode"] == 200
    assert res["headers"]["Content-Type"] == "application/json"
    assert res["body"]["homepage_url"] == "https://www.surreycc.gov.uk/"
    assert res["body"]["gss"] == "E10000030"
    assert res["body"]["name"] == "Surrey"
    assert res["body"]["phone"] == "0300 200 1008"
    assert res["body"]["hub_url"] == "https://www.surreycc.gov.uk/people-and-community/emergency-planning-and-community-safety/coronavirus/community-support/need-help"
    assert res["body"]["email"] == None
    assert res["body"]["date_collected"] == None
    assert res["body"]["notes"] == None


def test_no_spaces():
    res = _request_postcode("GU227QQ")
    assert res["statusCode"] == 200
    assert res["headers"]["Content-Type"] == "application/json"
    assert res["body"]["homepage_url"] == "https://www.surreycc.gov.uk/"

def test_county():
    res = _request_postcode("GU22 7QQ")
    assert res["statusCode"] == 200
    assert res["headers"]["Content-Type"] == "application/json"
    assert res["body"]["homepage_url"] == "https://www.surreycc.gov.uk/"

def test_uta():
    res = _request_postcode("LU7 1AT")
    assert res["statusCode"] == 200
    assert res["headers"]["Content-Type"] == "application/json"
    assert res["body"]["homepage_url"] == "http://www.centralbedfordshire.gov.uk/"

def test_cityoflondon():
    res = _request_postcode("EC2R 8AH")
    assert res["statusCode"] == 200
    assert res["headers"]["Content-Type"] == "application/json"
    assert res["body"]["homepage_url"] == "https://www.cityoflondon.gov.uk/"

def test_london_borough():
    res = _request_postcode("KT2 5RD")
    assert res["statusCode"] == 200
    assert res["headers"]["Content-Type"] == "application/json"
    assert res["body"]["homepage_url"] == "https://www.kingston.gov.uk/"

def test_metro_district():
    res = _request_postcode("NE1 4ST")
    assert res["statusCode"] == 200
    assert res["headers"]["Content-Type"] == "application/json"
    assert res["body"]["homepage_url"] == "https://www.newcastle.gov.uk/"

def test_scottish_council_area():
    res = _request_postcode("G51 1EA")
    assert res["statusCode"] == 200
    assert res["headers"]["Content-Type"] == "application/json"
    assert res["body"]["homepage_url"] == "https://www.glasgow.gov.uk/"

def test_nir_district():
    res = _request_postcode("BT4 3TT")
    assert res["statusCode"] == 200
    assert res["headers"]["Content-Type"] == "application/json"
    assert res["body"]["homepage_url"] == "https://www.belfastcity.gov.uk/"

def test_welsh_uta():
    res = _request_postcode("CF10 1NS")
    assert res["statusCode"] == 200
    assert res["headers"]["Content-Type"] == "application/json"
    assert res["body"]["homepage_url"] == "https://www.cardiff.gov.uk/"
