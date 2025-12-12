from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional

from pydantic import Field

from seekrai.types.abstract import BaseModel
from seekrai.types.files import FilePurpose, FileType


class AlignmentType(str, Enum):
    PRINCIPLE = "principle"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    RAFT = "raft"  # deprecated - use CONTEXT_DATA instead
    CONTEXT_DATA = "context_data"


class SystemPrompt(BaseModel):
    id: str
    source_id: str
    content: str
    is_custom: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SystemPromptRequest(BaseModel):
    instructions: str | None = None
    content: str | None = None


class SystemPromptCreateRequest(BaseModel):
    instructions: str


class SystemPromptUpdateRequest(BaseModel):
    content: str


class AlignmentRequest(BaseModel):
    instructions: str = Field(
        default=..., description="Task description/instructions for the alignment task"
    )
    files: List[str] = Field(
        default=..., description="List of file ids to use for alignment"
    )
    type: AlignmentType = Field(
        default=AlignmentType.PRINCIPLE,
        description="Type of alignment task (principle, chain_of_thought, or context_data)",
    )
    vector_database_id: str | None = Field(
        default=None,
        description="Optional vector database id to use for context retrieval during context_data alignment",
    )


class AlignmentEstimationRequest(BaseModel):
    files: List[str] = Field(
        default=...,
        description="List of file ids to use to generate an alignment estimate",
    )


class AlignmentEstimationResponse(BaseModel):
    input_tokens: int = Field(
        default=...,
        description="Estimated number of input tokens for the given files",
    )
    output_tokens: int = Field(
        default=...,
        description="Estimated number of output tokens for the given files",
    )


class AlignmentJobStatus(str, Enum):
    STATUS_PENDING = "pending"
    STATUS_QUEUED = "queued"
    STATUS_RUNNING = "running"
    STATUS_CANCEL_REQUESTED = "cancel_requested"
    STATUS_CANCELLED = "cancelled"
    STATUS_FAILED = "failed"
    STATUS_COMPLETED = "completed"


class AlignmentResponse(BaseModel):
    id: Optional[str] = Field(default=..., description="Alignment job ID")
    created_at: datetime | None = None
    updated_at: datetime | None = None
    status: AlignmentJobStatus | None = None
    current_step: str | None = None
    progress: str | None = None


class AlignmentOutput(BaseModel):
    id: str
    filename: str
    bytes: int | None = None
    created_at: datetime | None = None
    file_type: FileType | None = None
    purpose: FilePurpose | None = None


class AlignmentList(BaseModel):
    # object type
    object: Literal["list"] | None = None
    # list of fine-tune job objects
    data: List[AlignmentResponse] | None = None
