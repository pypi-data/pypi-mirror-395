from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import Field

from seekrai.types.abstract import BaseModel


class InfluentialFinetuningDataResponse(BaseModel):
    results: List[Dict[str, Any]] = Field(
        ..., description="List of influential training data results"
    )
    version: str = Field(..., description="Version of the explainability service")


class InfluentialFinetuningDataRequest(BaseModel):
    question: str = Field(..., description="Question from user")
    system_prompt: Optional[str] = Field(
        None,
        description="System prompt for the user's question.",
    )
    answer: Optional[str] = Field(
        None,
        description="Answer of the finetuned model to the question; if None, the answer is retrieved from the finetuned model",
    )
