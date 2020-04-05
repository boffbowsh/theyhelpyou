# TheyHelpYou

TheyHelpYou is a project to help vulnerable, shielding and self-isolating people
to find their local Community Hub and get help.

It is the inspiration, design and code of [@boffbowsh][], [@Rossehkins][] and [@RTO][].

With lots of help crowd-sourcing the data from [@CreaFarrar][], [@Doccykins],
and many others.

## How you can help

If you would like to help, the most important thing you can do is:

* STAY HOME.
* PROTECT THE NHS.
* SAVE LIVES.

If you have time to spare you can contribute by reviewing and commenting where
you find out of date information in [this spreadsheet][sheet].

For example, perhaps the Community Hub page has been updated and the URL has
changed.

## Using the data

The data is available via an API, currently with no restrictions.

### Postcode lookup endpoint

`GET https://www.theyhelpyou.co.uk/api/postcode?postcode=$postcode`

Example request: `GET https://www.theyhelpyou.co.uk/api/postcode?postcode=SW1A1AA`

Response:
```json
{
  "gss": "E09000033",
  "name": "Westminster",
  "homepage_url": "https://www.westminster.gov.uk/",
  "email": "westminsterconnects@westminster.gov.uk",
  "hub_url": "https://www.westminster.gov.uk/coronavirus-how-you-can-help",
  "phone": "020 7641 1222",
  "date_collected": "31/03/2020",
  "notes": null
}
```

## Hacking on the code

### Frontend

Nothing fancy here right now, just a flat HTML file with jQuery and Handlebars,
and the tiniest bit of CSS. Anything that's in the `site/` directory will get
uploaded to S3. The cache max-age is 10 while we're developing, but will be 60
or 300 when properly live.

Because of CORS, if you want to run the code locally and hit the live API,
you'll need to serve it from a local web server. The simplest way is using Python's built-in HTTP server:

```bash
$ cd site
$ python -m SimpleHTTPServer
```

Then visit http://0.0.0.0:8000/index.html

### Backend

The backend runs as 3 simple Python 3.7 Lambda functions, stored in the `api/`
directory. There's no Serverless framework or similar involved, just a `make`
task that uploads a ZIP containing all the funcitons and their dependencies to
S3 and updates the Lambda definitions.

The data is imported from the spreadsheet into a DynamoDB table keyed by GSS
code. We look this up from another table which maps postcodes to GSS code. This
needs updating when we start supporting per-district hubs for councils like East
Sussex.

### Testing

Run `make test` to run the tests.


## License

Code is [MIT Licensed](./LICENSE.md)

Data is [CC-BY-SA 4.0 Licensed](https://creativecommons.org/licenses/by-sa/4.0/)


[@boffbowsh]: https://twitter.com/boffbowsh
[@RTO]: https://twitter.com/RTO
[@Rossehkins]: https://twitter.com/Rossehkins
[@CreaFarrar]: https://twitter.com/CreaFarrar
[@Doccykins]: https://twitter.com/Doccykins

[sheet]: https://docs.google.com/spreadsheets/d/1uwcEbPob7EcOKBe_H-OiYEP3fITjbZH-ccpc81fMO7s/edit#gid=1418426695
