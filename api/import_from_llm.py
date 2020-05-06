import csv
from urllib.request import urlopen

from helpers import format_response, maybe_use_xray
from models import CommunityHub
from pynamodb.exceptions import DoesNotExist

maybe_use_xray()

CODES_TO_IMPORT = {
    "volunteering_url": {"LGSL": "1113", "LGIL": "8"},
    "vulnerable_url": {"LGSL": "1287", "LGIL": "8"}
}

def lambda_handler(event, context):
    resp = urlopen(
        "https://local-links-manager.publishing.service.gov.uk/data/links_to_services_provided_by_local_authorities.csv"
    )

    if resp.status == 200:
        lines = [str(l, "utf-8") for l in resp.read().splitlines()]
        c = csv.DictReader(lines)
        with CommunityHub.batch_write() as batch:
            for r in c:
                for attr, codes in CODES_TO_IMPORT.items():
                    if r["LGSL"] == codes["LGSL"] and r["LGIL"] == codes["LGIL"]:
                        try:
                            record = CommunityHub.get(r["GSS"])
                        except DoesNotExist:
                            continue

                        if attr not in record.attribute_values:
                            print("Found new url for {}: {}".format(r["GSS"], r["URL"]))
                        elif record.attribute_values[attr] != r["URL"]:
                            print("URL for {} changed. Old: {} New: {}".format(r["GSS"], record.attribute_values[attr], r["URL"]))

                        record.attribute_values[attr] = r["URL"]
                        batch.save(record)

if __name__ == "__main__":
    lambda_handler({}, {})
