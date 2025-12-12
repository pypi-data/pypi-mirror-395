from abc import ABC, abstractmethod
from datetime import timedelta
from typing import List
from uuid import uuid4

import pandas
from pydantic import BaseModel

from logis.data_type import DEFAULT_PYDANTIC_MODEL_CONFIG

from .order import *


class WavePickingConfig(BaseModel):
    """
    波次拣选配置
    """

    # 批次大小
    batch_size: int | None = None
    # 时间窗口
    time_interval: timedelta | None = None
    # 指定各个时间段
    time_index: pandas.DatetimeIndex | None = None

    model_config = DEFAULT_PYDANTIC_MODEL_CONFIG


class WavePickingStrategy(ABC):
    """
    分波次拣选策略
    """

    @abstractmethod
    def split(self, orders: List[IOrder], config: WavePickingConfig) -> List[IOrder]:
        pass

    def _generate_wave_id(self, waves: List[List[IOrder]]) -> str | int | None:
        """
        生成波次ID,默认是uuid4
        """
        if not waves:
            return None
        for i, wave in enumerate(waves):
            wave_id = str(uuid4())
            for od in wave:
                od.set_wave_id(wave_id)
