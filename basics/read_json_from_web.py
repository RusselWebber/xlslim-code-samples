# Fetch JSON data from a web site
import urllib.request
import json


def fetch_json(url):
    """GET data from the url and assume the response is JSON."""

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    columns = ["userId", "id", "title", "completed"]
    result = [columns]
    for d in data:
        result.append([d[c] for c in columns])
    return result


if __name__ == "__main__":
    print(fetch_json("https://jsonplaceholder.typicode.com/todos"))
