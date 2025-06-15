from typing import final
from fastapi import APIRouter, WebSocket, Request
from deepface import DeepFace
import numpy as np
import cv2
import base64
import asyncio
import os
import uuid

router = APIRouter()

emotion_color = {
    "angry": "#f04800", # 빨강
    "disgust": "#f04800", # 노랑
    "fear": "#f0AC00", # 빨강
    "happy": "#99ffbd", # 초록
    "sad": "#00C8F0", # 파랑
    "surprise": "#f0AC00", # 노랑
    "neutral": "#000000", # 검정
}

@router.websocket("/ws")
async def ws_emotion(websocket : WebSocket):
    await websocket.accept()
    last_emotion = None

    while True:
        try:
            data = await websocket.receive_text()

            img_bytes = base64.b64decode(data)
            np_arr = np.frombuffer(img_bytes, np.uint8) # 숫자 배열로 디코딩
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)
            # enforce_detection=False : 얼굴이 감지되지 않아도 에러를 발생시키지 않기 위함
            emotion = result[0]['dominant_emotion']

            if last_emotion != emotion:
                last_emotion = emotion
                color = emotion_color.get(emotion)
                await websocket.send_json({
                    "emotion" : emotion,
                    "color" : color
                })
            else:
                await websocket.send_json({
                    "emotion": emotion,
                    "color": None
                })

        except Exception as e:
            print(f"error : {e}")
            break


@router.post("/upload")
async def upload_cover(request: Request):
    data = await request.json()
    image_data = data.get("image")

    # base64 디코딩
    header, encoded = image_data.split(",", 1)
    binary_data = base64.b64decode(encoded)

    current_dir = os.path.dirname(__file__)
    save_dir = os.path.abspath(os.path.join(current_dir, "../..", "uploads/coverImage"))
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, f"{uuid.uuid4().hex[:8]}.png")

    with open(save_path, "wb") as f:
        f.write(binary_data)

    return {"message": "커버 저장 성공", "path": save_path}
