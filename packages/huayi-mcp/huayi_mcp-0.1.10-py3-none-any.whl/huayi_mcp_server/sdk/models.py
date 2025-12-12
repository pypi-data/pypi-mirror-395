from pydantic import BaseModel, Field


class GetSendNumRespData(BaseModel):
    user_id: str = Field(
        title="用户Id",
        alias="user_id",
        description="用户标识 用户ID userId",
    )
    user_phone: str = Field(
        title="用户手机号码",
        alias="user_phone",
        description="用户手机号码 可作为用户标识 userPhone",
    )
    total_num: int = Field(
        title="自配送总次数",
        alias="total_num",
        description="自配送总次数",
    )
    free_num: int = Field(
        title="免费赠送的自配送次数",
        alias="free_num",
        description="免费赠送的自配送次数",
    )
    member_num: int = Field(
        title="赠予会员的自配送次数",
        alias="member_num",
        description="赠予会员的自配送次数",
    )
    member_expire: int = Field(
        title="会员到期时间",
        alias="member_expire",
        description="会员到期时间,也即赠予会员的自配送次数到期时间",
    )
    buy_num: int = Field(
        title="用户购买的自配送次数",
        alias="buy_num",
        description="用户购买的自配送次数",
    )


class GetSendNumOutput(BaseModel):
    user_id: str = Field(
        title="用户Id",
        alias="user_id",
        description="用户标识 用户ID userId",
    )
    user_phone: str = Field(
        title="用户手机号码",
        alias="user_phone",
        description="用户手机号码 可作为用户标识 userPhone",
    )
    total_num: int = Field(
        title="自配送总次数",
        alias="total_num",
        description="自配送总次数",
    )
    member_num: int = Field(
        title="赠予会员的自配送次数",
        alias="member_num",
        description="赠予会员的自配送次数",
    )
    member_expire: int = Field(
        title="会员到期时间",
        alias="member_expire",
        description="会员到期时间,也即赠予会员的自配送次数到期时间",
    )

