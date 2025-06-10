from deepface import DeepFace
import numpy as np
import random

def softmax_emotion_selection(emotion_dict: dict) -> str:   # 좀 더 자연스러운 감정 선택을 위해
    emotions = list(emotion_dict.keys())
    scores = np.array(list(emotion_dict.values()))

    exp_scores = np.exp(scores - np.max(scores))
    probs = exp_scores / exp_scores.sum()

    return random.choices(emotions, weights=probs, k=1)[0]

def analyze_emotion(image_path: str) -> str:
    try:
        result = DeepFace.analyze(img_path=image_path, actions=["emotion"], enforce_detection=False)
        emotions = result[0]['emotion']
        selected_emotion = softmax_emotion_selection(emotions)
        return selected_emotion
    except Exception as e:
        print(f"감정 분석 실패: {e}")
        return "neutral"
