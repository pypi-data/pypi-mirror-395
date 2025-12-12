from datetime import datetime
from gmo_fx.errors import ApiError


class Response:
    response_status: int
    response_time: datetime

    def __init__(self, response: dict):
        self.response_status = response["status"]
        self.response_time = datetime.strptime(
            response["responsetime"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        if self.response_status != 0:
            err_code = response["messages"][0]["message_code"]
            message = response["messages"][0]["message_string"]
            raise ApiError(err_code, message=message)
