# Server for Search in URLs

Running in heroku : http://fathomless-tundra-65369.herokuapp.com

## Run locally

`$ foreman start`

## Sample usage.

```bash
$ curl -X POST -d '{"query":"HTTPServer", "urls":["http://stackoverflow.com/questions/16069816/getting-python-error-from-cant-read-var-mail-bio", "https://gist.github.com/huyng/814831"]}' -H 'Content-Type: application/json' http://fathomless-tundra-65369.herokuapp.com
{"found_urls": ["https://gist.github.com/huyng/814831"], "original_query": "HTTPServer"}%
```

# TODO

- Benchmarks
- Scaling
- Redis configs
- DB for url caching ?
