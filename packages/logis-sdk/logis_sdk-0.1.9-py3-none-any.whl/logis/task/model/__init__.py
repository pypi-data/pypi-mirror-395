from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Iterable, Literal, TypeAlias

from pydantic import BaseModel, Field

TaskId: TypeAlias = str | int
TaskPriority: TypeAlias = str | int


class TaskStatus(Enum):
    """
    任务状态
    """

    NOT_STARTED = "not_started"
    STARTED = "started"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    FAILED = "failed"


class ITask(metaclass=ABCMeta):
    """
    任务基础抽象类
    """

    @abstractmethod
    def get_task_id(self) -> TaskId:
        pass

    @abstractmethod
    def get_priority(self) -> TaskPriority:
        """
        任务优先级
        """
        pass

    @abstractmethod
    def update_status(self, status: TaskStatus):
        """
        更新任务状态
        """
        pass

    @abstractmethod
    def is_status_at(self, status: TaskStatus) -> bool:
        """
        检查任务状态是否为指定值
        """
        pass

    @property
    def finished(self) -> bool:
        return self.is_status_at(TaskStatus.FINISHED)


TaskLike: TypeAlias = ITask | TaskId


class Task(BaseModel, ITask):
    """
    任务基础结构
    """

    id: TaskId | None = None
    parent_id: TaskId | None = None
    children_ids: Iterable[TaskId] = Field(default_factory=list)

    name: str | None = None
    type: str | None = None
    priority: TaskPriority | None = None

    repeat: int = 1
    progress: float | int = 0
    tags: Iterable[str] = Field(default_factory=set)

    created_at: int | None = None
    updated_at: int | None = None
    started_at: int | None = None
    finished_at: int | None = None
    cancelled_at: int | None = None

    status: TaskStatus | None = None
    stage: str | None = None

    remark: str | None = None

    def get_task_id(self) -> TaskId:
        return self.id

    def get_priority(self) -> TaskPriority:
        return self.priority

    def update_status(self, status: TaskStatus):
        self.status = status

    def is_status_at(self, status: TaskStatus) -> bool:
        return self.status == status
