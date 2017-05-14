import requests
import json
import redis
import os

def search(request_id, search_query, urls):
    redis_conn = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/1"))
    redis_conn.set(request_id, '{"status":"in_progress"}')
    result_urls = []
    for url in urls:
        url_content = requests.get(url)
        if search_query in url_content.text:
            result_urls.append(url)
    response_dict = {"original_query": search_query,
                "found_urls":result_urls, "status": "finished"}
    redis_conn.set(request_id, json.dumps(response_dict))
