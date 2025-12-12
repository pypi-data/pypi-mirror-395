import time
from datetime import timezone, datetime
from typing import Optional

from pydantic import BaseModel


class HttpLogRecord(BaseModel):
    client: str
    method: str
    url: str
    scheme: str
    host: str
    port: int
    path: str
    query_string: str
    http_version: str

    # Request
    request_headers: Optional[dict] = None
    request_body: Optional[bytes] = None

    # Response
    response_status: Optional[int] = None
    response_headers: Optional[dict] = None
    response_body: Optional[bytes] = None

    # 必填, 时间, 格式按照 iso format
    request_time: Optional[str] = None
    response_time: Optional[str] = None
    request_timestamp: Optional[float] = None
    response_timestamp: Optional[float] = None
    duration: Optional[float] = None

    def set_request_time(self, timestamp: float = None):
        timestamp = timestamp or time.time()
        self.request_time = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
        self.request_timestamp = timestamp

    def set_response_time(self, timestamp: float = None):
        timestamp = timestamp or time.time()
        self.response_time = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
        self.response_timestamp = timestamp

    def cal_duration(self):
        self.duration = self.response_timestamp - self.request_timestamp

    def set_request_response_time(self,
                                  request_timestamp: float,
                                  response_timestamp: float):
        self.set_request_time(request_timestamp)
        self.set_response_time(response_timestamp)
        self.cal_duration()

    def set_response(self, response):
        self.response_status = getattr(response, "status_code", 0)
        self.response_headers = dict(getattr(response, "headers", {}))
        self.response_body = getattr(response, "content", None) or getattr(self, "body", b"")
