# Local testing

The page hits the online API, but you need to be serving the page from a local
`http://` URL rather than a `file://` URL for the CORS permissions to work. The
simplest way is using Python's built-in HTTP server:

```bash
$ cd site # this directory
$ python -m SimpleHTTPServer
```

Then visit http://0.0.0.0:8000/index.html


# TODO

 - Copyright? Any other licence?
