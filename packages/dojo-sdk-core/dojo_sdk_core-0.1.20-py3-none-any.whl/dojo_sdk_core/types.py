from enum import Enum
from typing import List, Union

from pydantic import BaseModel

"""Type definitions for Dojo."""


class ActionType(str, Enum):
    KEY = "key"
    CLICK = "click"
    RIGHT_CLICK = "right_click"
    SCROLL = "scroll"
    TYPE = "type"
    DOUBLE_CLICK = "double_click"
    DRAG = "drag"
    MOVE_TO = "move_to"
    PRESS = "press"
    HOTKEY = "hotkey"
    MIDDLE_CLICK = "middle_click"
    DONE = "done"
    WAIT = "wait"


class KeyAction(BaseModel):
    type: ActionType = ActionType.KEY
    key: str


class ClickAction(BaseModel):
    type: ActionType = ActionType.CLICK
    x: int
    y: int


class RightClickAction(BaseModel):
    type: ActionType = ActionType.RIGHT_CLICK
    x: int
    y: int


class ScrollAction(BaseModel):
    type: ActionType = ActionType.SCROLL
    direction: str = "up"
    amount: int = 100


class TypeAction(BaseModel):
    type: ActionType = ActionType.TYPE
    text: str


class DoubleClickAction(BaseModel):
    type: ActionType = ActionType.DOUBLE_CLICK
    x: int
    y: int


class DragAction(BaseModel):
    type: ActionType = ActionType.DRAG
    from_x: int
    from_y: int
    to_x: int
    to_y: int
    duration: float = 1.0


class MoveToAction(BaseModel):
    type: ActionType = ActionType.MOVE_TO
    x: int
    y: int
    duration: float = 0.0


class PressAction(BaseModel):
    type: ActionType = ActionType.PRESS
    key: str


class HotkeyAction(BaseModel):
    type: ActionType = ActionType.HOTKEY
    keys: List[str]


class MiddleClickAction(BaseModel):
    type: ActionType = ActionType.MIDDLE_CLICK
    x: int
    y: int


class DoneAction(BaseModel):
    type: ActionType = ActionType.DONE


class WaitAction(BaseModel):
    type: ActionType = ActionType.WAIT
    seconds: int = 1


Action = Union[
    KeyAction,
    ClickAction,
    RightClickAction,
    ScrollAction,
    TypeAction,
    DoubleClickAction,
    DragAction,
    MoveToAction,
    PressAction,
    HotkeyAction,
    MiddleClickAction,
    DoneAction,
    WaitAction,
]


class Score(BaseModel):
    task_name: str
    score: float
    status: str
    success: bool
    steps_taken: int
    reward: float
    completion_reason: str
