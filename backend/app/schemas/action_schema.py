from pydantic import BaseModel, Field


class Evidence(BaseModel):
    text: str
    source: str | None = None
    page: int | None = None


class ActionItem(BaseModel):
    action: str
    deadline: str | None = None
    responsible_party: str | None = None
    required_documents: list[str] = Field(default_factory=list)
    consequence: str | None = None
    evidence: Evidence


class ActionExtractionResult(BaseModel):
    actions: list[ActionItem] = Field(default_factory=list)
    eligibility_conditions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)