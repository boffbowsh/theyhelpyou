import csv
from urllib.request import urlopen

from models import CommunityHub

CommunityHub.create_table(wait=True)


def lambda_handler(event, context):
    resp = urlopen(
        "https://docs.google.com/spreadsheets/d/1uwcEbPob7EcOKBe_H-OiYEP3fITjbZH-ccpc81fMO7s/export?gid=0&format=csv&id=1uwcEbPob7EcOKBe_H-OiYEP3fITjbZH-ccpc81fMO7s"
    )

    if resp.status == 200:
        lines = [str(l, "utf-8") for l in resp.read().splitlines()]
        c = csv.reader(lines)
        next(c)
        CommunityHub.batch_write()
        for r in c:
            d = {
                "name": r[0],
                "homepage_url": r[2],
                "phone": r[3],
                "hub_url": r[4],
                "email": r[5],
                "date_collected": r[6],
                "notes": r[7],
            }

            record = CommunityHub(r[1], **d)
            record.save()

    else:
        print("error fetching CSV {}".format(resp.status))
