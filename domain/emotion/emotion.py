from typing import final

import cv2
from deepface import DeepFace

RED: final = '#FF0000'
BLUE: final = '#0000FF'
YELLOW: final = '#FFFF00'
BLACK: final = '#000000'

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cv2.waitKey(33) < 0 :
    ret, frame = capture.read()

    result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
    # enforce_detection=False : 얼굴이 감지되지 않아도 에러를 발생시키지 않기 위함
    if result[0]['dominant_emotion'] == 'happy' :
        print(RED)
    elif result[0]['dominant_emotion'] == 'fear' :
        print(BLUE)
    elif result[0]['dominant_emotion'] == 'sad' :
        print(YELLOW)
    else :
        print(BLACK)

    cv2.imshow("VideoFrame", frame)



capture.release()
cv2.destroyAllWindows()