from __future__ import annotations

from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

InteriorExterior = Literal["INT", "EXT", "INT/EXT", "EXT/INT", "UNKNOWN"]
RecommendationCategory = Literal["frame", "lighting_color", "lens", "movement", "texture"]


class InputFormat(str, Enum):
    AUTO = "auto"
    FOUNTAIN = "fountain"
    PLAIN_TEXT = "plain_text"


class EvidenceSpan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    start: int = Field(ge=0)
    end: int = Field(gt=0)
    text: str
    kind: Literal["trigger", "context"] = "trigger"


class Scene(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    ordinal: int = Field(ge=1)
    heading: str
    interior_exterior: InteriorExterior
    location: str
    time_of_day: str | None = None
    text: str
    source_span: EvidenceSpan


class Recommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: RecommendationCategory
    value: str
    rationale: str
    evidence: list[EvidenceSpan] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    alternatives: list[str] = Field(default_factory=list)
    origin: Literal["deterministic", "model"] = "deterministic"


class SceneAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    scene: Scene
    signals: list[str]
    recommendations: list[Recommendation]


class AnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tenant_id: UUID
    project_id: UUID
    screenplay_text: str = Field(max_length=500_000)
    input_format: InputFormat = InputFormat.AUTO

    @field_validator("screenplay_text")
    @classmethod
    def reject_blank_screenplay(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("screenplay text must not be blank")
        return value


class AnalysisResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal["1.0"] = "1.0"
    run_id: UUID = Field(default_factory=uuid4)
    tenant_id: UUID
    project_id: UUID
    provider: str
    provider_version: str
    scenes: list[SceneAnalysis]
    warnings: list[str] = Field(default_factory=list)
