__doc__ = """
指标模块
"""


from abc import ABC, abstractmethod
from typing import List, TypeVar

from logis.util.io_util import AsyncWriteBuffer, WriteBuffer, WriteBufferConfig
from logis.util.lambda_util import invoke


class MetricModel(ABC):
    """
    指标模型
    """

    @classmethod
    @abstractmethod
    def get_measurement(
        cls, prefix: str | None = None, suffix: str | None = None, sep: str = ""
    ) -> str:
        """
        获取指标名称
        """
        pass

    def to_influxdb_point(self, measurement: str | None = None):
        """
        转换为InfluxDB点
        """
        raise NotImplementedError("to_influxdb_point")


MetricModelType = TypeVar("MetricModelType", bound=MetricModel)


class IMetricCollector(ABC):
    """
    指标收集器
    """

    def __init__(self, write_buffer: WriteBuffer | None = None, **kwargs):
        super().__init__(**kwargs)
        self._buffer = write_buffer or AsyncWriteBuffer(
            WriteBufferConfig(batch_size=100, flush_interval=10, handler=self.submit)
        )
        invoke(self._buffer.start)

    @abstractmethod
    def submit[A](self, metrics: List[A]):
        """
        提交指标
        """
        pass

    def collect[A](self, metric: A):
        """
        缓冲指标
        """
        invoke(self._buffer.put, metric)

    def flush(self, flush_all: bool = False, **kwargs):
        """
        刷新指标
        """
        invoke(self._buffer.flush, flush_all=flush_all, **kwargs)
