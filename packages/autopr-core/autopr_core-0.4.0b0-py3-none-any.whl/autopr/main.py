from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from loguru import logger

from autopr.llm import llm
from autopr import generator
from autopr import analysis
from autopr import reviewer

app = FastAPI(title="AutoPR - Minimal MVP")


class GenerateRequest(BaseModel):
    diff: str = Field(..., example="+ def add(a, b):\n+     return a + b")
    commits: List[str] = Field(..., example=["feat: add helper for math"])
    issue: Optional[str] = Field(None, example="#123")


class ReviewRequest(BaseModel):
    diff: str = Field(..., example="print(\"debug\")\n# TODO: fix")



class GenerateResponse(BaseModel):
    title: str
    what_changed: str
    why: str
    files_impacted: List[str]
    tests: str
    risk_level: str
    rollback_plan: str


class ReviewFinding(BaseModel):
    type: str
    message: str
    severity: Optional[str]


class ReviewResponse(BaseModel):
    summary: str
    findings: List[ReviewFinding]
    confidence: float = Field(..., ge=0.0, le=1.0)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse, summary="Generate PR", response_description="Auto-generated PR description")
def generate_pr(req: GenerateRequest):
    """Generate a structured PR description from diff, commits and optional issue link.

    This endpoint uses the configured LLM provider (or the stub in dev) to return a JSON object
    describing the PR title, what changed, why it changed, impacted files, tests, risk level and rollback plan.
    """
    logger.info("Generating PR summary...")
    desc = generator.generate_pr_from(req.diff, req.commits, req.issue)
    # Ensure we return a shape matching the model - if provider returns a 'raw' fallback, adapt it
    if isinstance(desc, dict) and "title" in desc:
        return {k: desc.get(k, "") for k in GenerateResponse.__fields__.keys()}
    # minimal fallback
    return GenerateResponse(
        title=str(desc.get("title", "Auto PR")) if isinstance(desc, dict) else str(desc),
        what_changed=desc.get("what_changed", "") if isinstance(desc, dict) else "",
        why=desc.get("why", "") if isinstance(desc, dict) else "",
        files_impacted=desc.get("files_impacted", []) if isinstance(desc, dict) else [],
        tests=desc.get("tests", "") if isinstance(desc, dict) else "",
        risk_level=desc.get("risk_level", "unknown") if isinstance(desc, dict) else "unknown",
        rollback_plan=desc.get("rollback_plan", "") if isinstance(desc, dict) else "",
    )


@app.post("/review", response_model=ReviewResponse, summary="Review PR", response_description="AI-assisted code review findings")
def review_pr(req: ReviewRequest):
    """Analyze a diff and return review findings and a confidence score.

    The review output includes a brief summary, list of findings, each optionally annotated with a severity, and an overall confidence.
    """
    logger.info("Reviewing PR code...")
    out = reviewer.review_pr(req.diff)
    return out
