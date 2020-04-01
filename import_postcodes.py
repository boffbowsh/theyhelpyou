import csv
import sys

import models

import pynamodb
from retrying import retry
from tqdm import tqdm

@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
def persist_record(record):
    try:
        record.save()
    except pynamodb.exceptions.PutError as e:
        print("Error", e)
        raise e

models.Postcode.create_table()

fn = sys.argv[1]
print(fn)
lines = len(open(fn, "r").readlines())

with open(fn, "r") as f:
    c = csv.DictReader(f)
    next(c)

    with models.Postcode.batch_write() as batch:
        for r in tqdm(c, total=lines):
            if r["doterm"] != "":
                continue

            pcd = r["pcd"].replace(' ', '')
            r["lng"] = r["long"]

            for k in ["doterm", "dointr", "pcd", "pcd2", "pcds", "long"]:
                del r[k]

            record = models.Postcode(pcd, **r)
            persist_record(record)
