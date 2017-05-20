import requests
import json
import redis
import os
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

def search(request_id, search_query, urls):
    redis_conn = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/1"))
    redis_conn.set(request_id, '{"status":"in_progress"}')
    result_urls = []
    for url in urls:
        try:
            url_content = requests.get(url)
            page_source = url_content.text
            if search_query in page_source:
                soup = BeautifulSoup(page_source,"html.parser")
                for script in soup(["script", "style"]):
                    script.extract()
                if search_query in soup.get_text():
                    result_urls.append(url)
        except RequestException:
            print("Couldn't connect to: %s" % url)
    response_dict = {"original_query": search_query,
                "found_urls":result_urls, "status": "finished"}
    redis_conn.set(request_id, json.dumps(response_dict))
