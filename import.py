import csv
from urllib.request import urlopen

from tqdm import tqdm

from models import CommunityHub

CommunityHub.create_table(wait=True)

def handler(event, context):
    resp = urlopen("https://docs.google.com/spreadsheets/d/1uwcEbPob7EcOKBe_H-OiYEP3fITjbZH-ccpc81fMO7s/export?gid=0&format=csv&id=1uwcEbPob7EcOKBe_H-OiYEP3fITjbZH-ccpc81fMO7s")

    if resp.status == 200:
        print("ok")
        lines = [str(l, 'utf-8') for l in resp.read().splitlines()]
        c = csv.reader(lines)
        next(c)
        CommunityHub.batch_write()
        for r in tqdm(c):
            d = {
                "name": r[0],
                "homepage_url": r[2],
                "phone": r[3],
                "hub_url": r[4],
                "email": r[5],
                "date_collected": r[6],
                "notes": r[7]
            }

            record = CommunityHub(r[1], **d)
            record.save()
            # break

    else:
        print("error")

if __name__ == "__main__":
    handler(1, 2)
