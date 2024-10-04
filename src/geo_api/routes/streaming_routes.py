import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..configuration import MANAGER
from ..gpt_connection import chat_with_gpt
from ..models import Message
from ..schemas import MessageSchema

ws_router = APIRouter()


@ws_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await MANAGER.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            msg = Message.create(user_id=client_id, content=data)
            # await MANAGER.send_personal_message(f"You wrote: {data}", websocket)
            msg_ = MessageSchema(user_id=client_id, content=data,
                                 timestamp=msg.timestamp)
            await MANAGER.broadcast(msg_.to_json())
    except WebSocketDisconnect:
        MANAGER.disconnect(websocket)
        msg_ = MessageSchema(user_id=client_id, content="left the chat",
                             timestamp=datetime.datetime.now())
        await MANAGER.broadcast(msg_.to_json())


@ws_router.websocket("/gpt/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await MANAGER.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            gpt_name = f'gpt-client-{client_id}'
            msg = Message.create(user_id=client_id, content=data)
            gpt_response = chat_with_gpt(msg.content)
            # await MANAGER.send_personal_message(f"You wrote: {data}", websocket)
            msg_gpt = Message.create(user_id=gpt_name, content=gpt_response)
            msg_ = MessageSchema(user_id=gpt_name,
                                 content=gpt_response,
                                 timestamp=msg_gpt.timestamp)
            await MANAGER.broadcast(msg_.to_json())
    except WebSocketDisconnect:
        MANAGER.disconnect(websocket)
        msg_ = MessageSchema(user_id=client_id, content="left the chat",
                             timestamp=datetime.datetime.now())
        await MANAGER.broadcast(msg_.to_json())

