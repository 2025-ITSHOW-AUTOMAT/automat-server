from deepface import DeepFace

def analyze_emotion(image_path: str) -> str:
    try:
        result = DeepFace.analyze(img_path=image_path, actions=["emotion"], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        return emotion
    except Exception as e:
        print(f"감정 분석 실패: {e}")
        return "neutral"
