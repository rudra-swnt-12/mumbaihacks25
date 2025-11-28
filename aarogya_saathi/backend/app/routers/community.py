from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db, CommunityPost, Patient
from app.services.groq_service import GroqService
import json

router = APIRouter()
groq = GroqService()


class CreatePostRequest(BaseModel):
    phone_number: str
    content: str
    category: str = "General"


@router.get("/community/feed")
async def get_feed(db: Session = Depends(get_db)):
    """Get all safe posts, ordered by newest first."""
    return (
        db.query(CommunityPost)
        .filter(CommunityPost.is_flagged == False)
        .order_by(CommunityPost.id.desc())
        .all()
    )


@router.post("/community/post")
async def create_post(request: CreatePostRequest, db: Session = Depends(get_db)):
    user = db.query(Patient).filter_by(phone_number=request.phone_number).first()
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found. Please register via Voice first."
        )

    moderation_prompt = f"""
    Analyze this community post for a Medical App.
    POST: "{request.content}"
    
    RULES:
    1. Is it Toxic/Hate speech?
    2. Is it Medical Misinformation? (e.g. "Stop taking insulin")
    3. Is it a Cry for Help? (e.g. "I want to die")
    
    OUTPUT JSON:
    {{
        "is_safe": true/false,
        "flag_reason": "null or reason",
        "ai_reply": "null or a supportive comment"
    }}
    """

    is_flagged = False
    ai_reply = None

    try:
        chat_completion = await groq.client.chat.completions.create(
            messages=[{"role": "system", "content": moderation_prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.1,
            max_tokens=150,
            response_format={"type": "json_object"},
        )

        result = json.loads(chat_completion.choices[0].message.content)

        if not result.get("is_safe", True):
            is_flagged = True
            print(f"Mod Flag: {result.get('flag_reason')}")

        ai_reply = result.get("ai_reply")

    except Exception as e:
        print(f"Moderation Error: {e}")
        pass

    new_post = CommunityPost(
        author_id=user.id,
        author_name=user.full_name or "Anonymous",
        content=request.content,
        category=request.category,
        timestamp=datetime.now().strftime("%d %b, %I:%M %p"),
        is_flagged=is_flagged,
        ai_response=ai_reply,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "status": "posted",
        "post_id": new_post.id,
        "is_flagged": is_flagged,
        "ai_comment": ai_reply,
    }
