# Fetch JSON data from a web site
import urllib.request
import json


def fetch_json(url):
    """GET data from the url and assume the response is JSON."""

    with urllib.request.urlopen(url) as response:
        data = response.read()
    return json.loads(data)


if __name__ == "__main__":
    print(fetch_json("https://jsonplaceholder.typicode.com/todos"))
