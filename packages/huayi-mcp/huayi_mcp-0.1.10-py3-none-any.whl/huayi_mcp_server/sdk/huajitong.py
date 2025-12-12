import logging
from functools import wraps
from typing import Any, Dict

import httpx

from huayi_mcp_server.sdk import SDK
from huayi_mcp_server.sdk.models import GetSendNumRespData
from huayi_mcp_server.sdk.sign import sign


class Huajitong(SDK):
    @staticmethod
    def check_credentials(func):
        """检查 base_url 和 token 是否有效的装饰器"""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.base_url:
                return "base_url not provided"

            if not self.secret:
                return "secret not provided"
            return func(self, *args, **kwargs)

        return wrapper

    @check_credentials
    def self_send__get_send_num(self, user_identifier: str) -> str | GetSendNumRespData:
        url = self.base_url + "/v2/api/self-send/get-send-num"
        values = {"value": user_identifier}
        signed_str = sign(self.secret, values)
        values["sign"] = signed_str

        response = httpx.post(url, headers=self.headers, json=values)
        if response.status_code != 200:
            return f"response {response.status_code}"

        json_data: Dict[str, Any] = response.json()
        logging.debug("get_user_num_detail response content:", json_data)

        if json_data.get("code") != 200:
            code: int | None = json_data.get("code")
            msg: str | None = json_data.get("msg")
            return f"response {code}: {msg}"

        data = json_data.get("data")
        return GetSendNumRespData.model_validate(data)
