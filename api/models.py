from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class Postcode(Model):
    class Meta:
        table_name = "postcode_to_gss"
        read_capacity_units = 5
        write_capacity_units = 5
        region = "eu-west-2"

    pcd = UnicodeAttribute(hash_key=True)
    oscty = UnicodeAttribute(null=True)
    ced = UnicodeAttribute(null=True)
    oslaua = UnicodeAttribute(null=True)
    osward = UnicodeAttribute(null=True)
    parish = UnicodeAttribute(null=True)
    usertype = UnicodeAttribute(null=True)
    oseast1m = UnicodeAttribute(null=True)
    osnrth1m = UnicodeAttribute(null=True)
    osgrdind = UnicodeAttribute(null=True)
    oshlthau = UnicodeAttribute(null=True)
    nhser = UnicodeAttribute(null=True)
    ctry = UnicodeAttribute(null=True)
    rgn = UnicodeAttribute(null=True)
    streg = UnicodeAttribute(null=True)
    pcon = UnicodeAttribute(null=True)
    eer = UnicodeAttribute(null=True)
    teclec = UnicodeAttribute(null=True)
    ttwa = UnicodeAttribute(null=True)
    pct = UnicodeAttribute(null=True)
    nuts = UnicodeAttribute(null=True)
    statsward = UnicodeAttribute(null=True)
    oa01 = UnicodeAttribute(null=True)
    casward = UnicodeAttribute(null=True)
    park = UnicodeAttribute(null=True)
    lsoa01 = UnicodeAttribute(null=True)
    msoa01 = UnicodeAttribute(null=True)
    ur01ind = UnicodeAttribute(null=True)
    oac01 = UnicodeAttribute(null=True)
    oa11 = UnicodeAttribute(null=True)
    lsoa11 = UnicodeAttribute(null=True)
    msoa11 = UnicodeAttribute(null=True)
    wz11 = UnicodeAttribute(null=True)
    ccg = UnicodeAttribute(null=True)
    bua11 = UnicodeAttribute(null=True)
    buasd11 = UnicodeAttribute(null=True)
    ru11ind = UnicodeAttribute(null=True)
    oac11 = UnicodeAttribute(null=True)
    lat = UnicodeAttribute(null=True)
    lng = UnicodeAttribute(null=True)
    lep1 = UnicodeAttribute(null=True)
    lep2 = UnicodeAttribute(null=True)
    pfa = UnicodeAttribute(null=True)
    imd = UnicodeAttribute(null=True)
    calncv = UnicodeAttribute(null=True)
    stp = UnicodeAttribute(null=True)


class CommunityHub(Model):
    class Meta:
        table_name = "community_response_hubs"
        read_capacity_units = 5
        write_capacity_units = 25
        region = "eu-west-2"

    gss = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    homepage_url = UnicodeAttribute()
    phone = UnicodeAttribute(null=True)
    hub_url = UnicodeAttribute(null=True)
    email = UnicodeAttribute(null=True)
    date_collected = UnicodeAttribute(null=True)
    notes = UnicodeAttribute(null=True)
    public_notes = UnicodeAttribute(null=True)
    shielding_url = UnicodeAttribute(null=True)
    vulnerable_url = UnicodeAttribute(null=True)
    volunteering_url = UnicodeAttribute(null=True)
    volunteering_phone = UnicodeAttribute(null=True)
