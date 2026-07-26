import json
import threading
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.assistant import ask
from app.discord_bot import run_bot
from app.whatsapp_bot import router as whatsapp_router

app = FastAPI(title="Assistente IA")

app.include_router(whatsapp_router)

active_connections: list[WebSocket] = []
conversation_history: dict[str, list[dict]] = {}


@app.get("/", response_class=HTMLResponse)
async def web_chat():
    with open("app/static/index.html") as f:
        return f.read()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    user_id = f"ws_{id(websocket)}"
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            user_message = msg.get("message", "")
            history = conversation_history.get(user_id, [])
            response = ask(user_message, history)
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": response})
            conversation_history[user_id] = history[-20:]
            await websocket.send_json({"type": "response", "content": response})
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@app.post("/api/ask")
async def api_ask(message: str, user_id: str = "default"):
    history = conversation_history.get(user_id, [])
    response = ask(message, history)
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})
    conversation_history[user_id] = history[-20:]
    return {"response": response}


def start_discord_bot():
    thread = threading.Thread(target=run_bot, daemon=True)
    thread.start()


@app.on_event("startup")
async def startup():
    start_discord_bot()
