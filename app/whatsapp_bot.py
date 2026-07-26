from fastapi import APIRouter, Form
from fastapi.responses import Response
from app.assistant import ask
from twilio.twiml.messaging_response import MessagingResponse

router = APIRouter()

conversation_history: dict[str, list[dict]] = {}


@router.post("/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...),
):
    history = conversation_history.get(From, [])
    response = ask(Body, history)

    history.append({"role": "user", "content": Body})
    history.append({"role": "assistant", "content": response})
    conversation_history[From] = history[-20:]

    twiml = MessagingResponse()
    twiml.message(response)
    return Response(content=str(twiml), media_type="application/xml")
