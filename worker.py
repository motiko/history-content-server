import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redistogo_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redistogo_conn = redis.from_url(redistogo_url)

if __name__ == '__main__':
    with Connection(redistogo_conn):
        worker = Worker(map(Queue, listen))
        worker.work()
