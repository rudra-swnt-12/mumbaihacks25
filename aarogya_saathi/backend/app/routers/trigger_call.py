from fastapi import APIRouter
from fastapi import Body
from fastapi.responses import JSONResponse
from app.services.twilio_service import TwilioService

router = APIRouter(prefix="/call", tags=["call"])


@router.post("/trigger")
async def trigger_call(phone: str = Body(..., embed=True)):
    """
    Trigger a phone call to the provided number using TwilioService.

    Request body: { "phone": "+91XXXXXXXXXX" }
    """
    service = TwilioService()
    sid = service.make_call(phone)
    if sid is None:
        return JSONResponse(status_code=500, content={"status": "error", "message": "Call failed"})
    if sid == "simulated_sid":
        return {"status": "ok", "mode": "simulated", "sid": sid}
    return {"status": "ok", "sid": sid}
