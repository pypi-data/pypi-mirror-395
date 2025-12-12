from typing import Literal

from pydantic import BaseModel


class Notification(BaseModel):
    title: str | None = None
    duration: float | int = -1
    content: str | None = None
    closable: bool = True
    type: Literal["info", "success", "warning", "error"] = "info"
