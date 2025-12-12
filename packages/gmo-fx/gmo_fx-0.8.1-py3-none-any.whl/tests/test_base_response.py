import pytest
from gmo_fx.errors import ApiError
from gmo_fx.api.response import Response
from datetime import datetime


class TestBaseResponse:
    convert_response_testdata = [
        (0, datetime(2001, 12, 12)),
        (0, datetime(2010, 3, 1)),
        (0, datetime(2020, 5, 20)),
    ]

    @pytest.mark.parametrize("status, time", convert_response_testdata)
    def test_convert_response(
        self,
        status: int,
        time: datetime,
    ):
        data = {
            "status": status,
            "responsetime": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        response = Response(data)
        assert response.response_status == status
        assert response.response_time == time

    error_codes = [
        143,
        148,
        189,
        200,
        201,
        254,
        414,
        423,
        512,
        542,
        595,
        635,
        759,
        760,
        761,
        769,
        786,
        5003,
        5008,
        5009,
        5010,
        5011,
        5012,
        5014,
        5106,
        5114,
        5122,
        5123,
        5125,
        5126,
        5130,
        5132,
        5201,
        5202,
        5204,
        5206,
        5207,
        5208,
        5209,
        5210,
        5211,
        5213,
        5214,
        5218,
        5219,
        5220,
        5221,
        5222,
        5223,
        5224,
        5225,
        5226,
        5227,
        5228,
        5229,
    ]

    def create_error_data(self, error_code: str, message: str) -> dict:
        return {
            "status": 1,
            "messages": [
                {
                    "message_code": error_code,
                    "message_string": message,
                }
            ],
            "responsetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

    def test_should_return_error_status_is_not_0(self) -> None:
        with pytest.raises(ApiError) as e:
            Response(
                {
                    "status": 1,
                    "messages": [
                        {
                            "message_code": "ERR-5011",
                            "message_string": "API-key format invalid.",
                        }
                    ],
                    "responsetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                }
            )

    @pytest.mark.parametrize("error_code", error_codes)
    def test_error_code_test(self, error_code) -> None:
        with pytest.raises(ApiError) as e:
            data = self.create_error_data(
                f"ERR-{error_code}", "API-key format invalid."
            )
            Response(data)
        assert e.value.error_code == f"ERR-{error_code}"
