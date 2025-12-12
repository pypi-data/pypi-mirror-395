from pydantic import AliasChoices, BaseModel, Field

from logis.data_type.base import DEFAULT_PYDANTIC_MODEL_CONFIG
from logis.data_type.point import Point
from logis.data_type.unitable import Length, QuantifiedValue


class SpatialProps(BaseModel):
    """
    空间属性
    """

    model_config = DEFAULT_PYDANTIC_MODEL_CONFIG

    width: Length | None = Field(alias="单元格宽度", default=None)
    height: Length | None = Field(alias="层高", default=None)
    depth: Length | None = Field(
        validation_alias=AliasChoices("货架深度", "托盘货架深度"), default=None
    )
    rotation: QuantifiedValue | None = Field(
        validation_alias=AliasChoices("旋转", "rotate"), default=None
    )
    center_point: Point | None = None
