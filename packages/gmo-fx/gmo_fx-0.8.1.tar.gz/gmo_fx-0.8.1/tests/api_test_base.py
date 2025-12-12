from abc import ABC
from typing import Any, Callable, Optional, Union
import pytest
import json
from unittest.mock import MagicMock
from datetime import datetime


class ApiTestBase(ABC):

    def create_response(
        self,
        data: Optional[Union[dict, list]] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        response = MagicMock()
        response.status_code = status_code
        json_data = {
            "status": 0,
            "data": data,
            "responsetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        response.json.return_value = json_data
        response.text = text or json.dumps(json_data)
        return response

    def check_404_error(self, request_mock: MagicMock, target: Callable[[], Any]):
        request_mock.return_value = self.create_response(
            status_code=404,
            text="Not Found",
        )
        with pytest.raises(RuntimeError):
            target()
