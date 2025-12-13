from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel

from .types import Action


class ExecutionTrace(BaseModel):
    task_name: str
    status: str
    success: bool
    steps_taken: int
    reward: float
    completion_reason: str
    history: List[dict]
    final_state: dict
    final_screenshot: str


# WebSocket API Message Types
class TaskStatus(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class JobStatus(str, Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PENDING = "PENDING"


class MsgType(str, Enum):
    START_JOB = "StartJobRequest"
    START_JOB_RESP = "StartJobResponse"
    SUBMIT_ACTION = "SubmitActionRequest"
    GET_NEXT_ACTION = "GetNextActionRequest"
    TASK_COMPLETE = "TaskComplete"
    JOB_STATUS_RESP = "JobStatusResponse"
    JOB_COMPLETE = "JobComplete"
    AUTH = "Auth"
    AUTH_RESP = "AuthResp"
    CANCEL_JOB = "CancelJobRequest"


class HistoryStep(BaseModel):
    step: int
    after_screenshot: str
    agent_response: str
    raw_response: str
    action: Action
    score: float


class NextStep(BaseModel):
    number: int
    after_screenshot: str


class TaskResult(BaseModel):
    status: TaskStatus
    start_time: datetime
    end_time: datetime
    exec_id: str
    task_id: str
    task_name: str
    job_id: str
    final_score: float
    reason: str
    history: List[HistoryStep]
    recording: Optional[str] = None


class JobComplete(BaseModel):
    type: Literal[MsgType.JOB_COMPLETE]
    job_id: str
    tasks: List[TaskResult]


# Stateless API Types


class PendingTask(BaseModel):
    start_time: datetime
    task_name: str
    id: str
    exec_id: str
    prompt: str
    status: TaskStatus
    history: List[HistoryStep]
    pending_step: Optional[NextStep] = None


class FinishedTask(BaseModel):
    status: TaskStatus
    start_time: datetime
    end_time: datetime
    task_name: str
    id: str
    exec_id: str
    prompt: str
    history: List[HistoryStep]
    score: float
    recording: Optional[str] = None


class JobStatusResponse(BaseModel):
    status: JobStatus
    start_time: datetime
    end_time: datetime | None
    pending_tasks: List[PendingTask]
    finished_tasks: List[FinishedTask]


class JobMetadata(BaseModel):
    id: str
    status: JobStatus
    start_time: datetime
    end_time: datetime | None
    num_tasks: int
    num_completed_tasks: int


class JobsResponse(BaseModel):
    jobs: List[JobMetadata]


# Union type for all WebSocket messages
WebSocketMessage = Union[JobComplete,]
