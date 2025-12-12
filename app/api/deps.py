import time
import uuid
from contextlib import contextmanager

from fastapi import Request


@contextmanager
def latency_tracker():
    start = time.perf_counter()
    try:
        yield lambda: (time.perf_counter() - start) * 1000
    finally:
        ...


def get_request_meta():
    request_id = str(uuid.uuid4())
    return request_id
