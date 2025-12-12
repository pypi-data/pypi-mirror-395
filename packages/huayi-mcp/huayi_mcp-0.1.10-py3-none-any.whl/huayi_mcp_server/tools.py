import datetime

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from pydantic import Field
from typing_extensions import Annotated

from huayi_mcp_server.sdk.huajitong import Huajitong
from huayi_mcp_server.sdk.models import GetSendNumRespData, GetSendNumOutput


class ToolSet:
    def __init__(self, name: str, log_level: str, base_url: str, secret: str):
        self.mcp: FastMCP = FastMCP(name=name)
        log_level_upper = log_level.upper()
        if log_level_upper in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            self.mcp.settings.log_level = log_level_upper
        self.base_url: str = base_url
        self.secret: str = secret
        self.huajitong_client: Huajitong = Huajitong(base_url=self.base_url, secret=self.secret)

        @self.mcp.tool(
            name="查询给定用户自配送次数",
            title="查询给定用户自配送次数",
            description="查询给定用户自配送次数",
        )
        async def get_user_num_detail(  # pyright: ignore[reportUnusedFunction]
                ctx: Context[ServerSession, None],
                user_identifier: Annotated[
                    str,
                    Field(
                        title="用户标识",
                        description="用户标识, 可能是 userId 或 userPhone",
                        default=None,
                    ),
                ],
        ) -> str | tuple[Annotated[
            str, Field(title="对查询结果的解释", description="对查询用户自配送次数的数据的解释")], GetSendNumOutput]:
            """查询给定用户自配送次数"""

            await ctx.info(f"get_user_num_detail's input: {user_identifier}")

            # todo: handle error
            result: GetSendNumRespData | str = self.huajitong_client.self_send__get_send_num(
                user_identifier=user_identifier)
            if isinstance(result, str):
                return result
            if isinstance(result, GetSendNumRespData):
                output = GetSendNumOutput(
                    user_id=result.user_id,
                    user_phone=result.user_phone,
                    total_num=result.total_num,
                    member_num=result.member_num,
                    member_expire=result.member_expire,
                )
                if result.member_expire:
                    member_expires_at = datetime.datetime.fromtimestamp(result.member_expire).strftime("%Y年%m月%d日")
                    explain = f"""用户总自配送次数为 {result.total_num}, 其中会员受赠次数为 {result.member_num}, 会员受赠次数过期时间为 {member_expires_at}。"""
                    return explain, output
                explain = f"""用户总自配送次数为 {result.total_num}, 无会员赠送次数。"""
                return explain, output

            return """未能 "查询给定用户自配送次数": 内部错误"""

    def run_on_stdio(self):
        self.mcp.run(transport="stdio")

    def run_on_streamable_http(self):
        self.mcp.run(transport="streamable-http")

    def run_on_sse(self):
        self.mcp.run(transport="sse")
