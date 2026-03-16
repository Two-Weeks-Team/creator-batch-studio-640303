from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from models import SessionLocal, Batch, Hook, Shot, Lane, PublishItem
from ai_service import call_inference

router = APIRouter()

# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------
class PlanRequest(BaseModel):
    query: str = Field(..., description="Video idea supplied by the user")
    preferences: Any = Field(default_factory=list, description="Selected platforms e.g., ['TikTok','Reels']")

class HookOut(BaseModel):
    platform: str
    text: str

class ShotOut(BaseModel):
    order: int
    description: str

class LaneOut(BaseModel):
    platform: str
    duration: str
    hook_text: str

class PublishItemOut(BaseModel):
    order: int
    description: str

class BatchDetail(BaseModel):
    id: int
    batch_name: str
    idea: str
    created_at: str
    hooks: List[HookOut]
    shots: List[ShotOut]
    lanes: List[LaneOut]
    publish_items: List[PublishItemOut]

class InsightsRequest(BaseModel):
    batch_id: int = Field(..., description="ID of the batch to analyse")
    context: Optional[str] = Field(None, description="Additional context for the AI")

# ---------------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------------------------
# Business Endpoints
# ---------------------------------------------------------------------------
@router.post("/plan")
async def generate_plan(request: PlanRequest, db: SessionLocal = Depends(get_db)):
    """Generate a full production batch using the LLM and store it."""
    # Build messages for the LLM; keep it concise for demo
    messages = [
        {"role": "system", "content": "You are an assistant that creates short‑form video production plans. Return JSON with keys: batch_name, idea, hooks (list of {platform, text}), shot_list (ordered descriptions), repurpose_lanes (list of {platform, duration, hook}), publish_queue (ordered strings)."},
        {"role": "user", "content": f"Idea: {request.query}\nPlatforms: {', '.join(request.preferences) if request.preferences else 'TikTok, Reels, Shorts'}"},
    ]
    ai_response = await call_inference(messages)
    # Expecting a dict; fallback already handled inside call_inference
    data = ai_response if isinstance(ai_response, dict) else {}
    if not data.get("batch_name"):
        raise HTTPException(status_code=500, detail="AI failed to produce a valid batch")
    # Persist batch and related entities
    new_batch = Batch(batch_name=data["batch_name"], idea=data["idea"])
    db.add(new_batch)
    db.flush()  # obtain batch.id
    # Hooks
    for h in data.get("hooks", []):
        db.add(Hook(batch_id=new_batch.id, platform=h.get("platform", ""), text=h.get("text", "")))
    # Shots (assume ordered list)
    for idx, s in enumerate(data.get("shot_list", []), start=1):
        db.add(Shot(batch_id=new_batch.id, description=s, order=idx))
    # Lanes
    for lane in data.get("repurpose_lanes", []):
        db.add(
            Lane(
                batch_id=new_batch.id,
                platform=lane.get("platform", ""),
                duration=lane.get("duration", ""),
                hook_text=lane.get("hook", "") or lane.get("hook_text", ""),
            )
        )
    # Publish queue
    for idx, item in enumerate(data.get("publish_queue", []), start=1):
        db.add(PublishItem(batch_id=new_batch.id, description=item, order=idx))
    db.commit()
    return {"batch_id": new_batch.id, "status": "created"}

@router.post("/insights")
async def get_insights(req: InsightsRequest, db: SessionLocal = Depends(get_db)):
    """Ask the LLM for strategic insights about a saved batch."""
    batch = db.query(Batch).filter(Batch.id == req.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    # Gather brief textual summary
    summary = f"Batch '{batch.batch_name}' for idea: {batch.idea}. Platforms: {', '.join([h.platform for h in batch.hooks])}."
    messages = [
        {"role": "system", "content": "You are a marketing strategist for short‑form video creators. Provide JSON with keys: insights (list of strings), next_actions (list), highlights (list)."},
        {"role": "user", "content": f"{summary}\nAdditional context: {req.context or 'none'}"},
    ]
    ai_response = await call_inference(messages)
    return ai_response

@router.get("/batches")
async def list_batches(db: SessionLocal = Depends(get_db)):
    batches = db.query(Batch).order_by(Batch.created_at.desc()).all()
    return [{"id": b.id, "batch_name": b.batch_name, "idea": b.idea, "created_at": b.created_at.isoformat()} for b in batches]

@router.get("/batches/{batch_id}")
async def get_batch(batch_id: int, db: SessionLocal = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    # Assemble detailed view
    return BatchDetail(
        id=batch.id,
        batch_name=batch.batch_name,
        idea=batch.idea,
        created_at=batch.created_at.isoformat(),
        hooks=[HookOut(platform=h.platform, text=h.text) for h in batch.hooks],
        shots=[ShotOut(order=s.order, description=s.description) for s in sorted(batch.shots, key=lambda x: x.order)],
        lanes=[LaneOut(platform=l.platform, duration=l.duration, hook_text=l.hook_text) for l in batch.lanes],
        publish_items=[PublishItemOut(order=p.order, description=p.description) for p in sorted(batch.publish_items, key=lambda x: x.order)],
    ).model_dump()

@router.post("/batches/{batch_id}/export")
async def export_checklist(batch_id: int, db: SessionLocal = Depends(get_db)):
    """Return a simple markdown checklist for the given batch."""
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    lines = [
        f"# {batch.batch_name} – Shoot‑Day Checklist",
        f"_Idea_: {batch.idea}\n",
        "## Hooks",
    ]
    for h in batch.hooks:
        lines.append(f"- [{h.platform}] {h.text}")
    lines.append("\n## Shot List (ordered)")
    for s in sorted(batch.shots, key=lambda x: x.order):
        lines.append(f"{s.order}. {s.description}")
    lines.append("\n## Publish Queue")
    for p in sorted(batch.publish_items, key=lambda x: x.order):
        lines.append(f"- {p.description}")
    markdown = "\n".join(lines)
    return {"markdown": markdown}
