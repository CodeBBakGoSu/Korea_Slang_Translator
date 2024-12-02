from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# FastAPI 앱 초기화
app = FastAPI()

# Hugging Face 모델 로드
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

# 요청 데이터 스키마 정의
class TranslationRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Slang Translator API!"}

@app.post("/translate")
def translate(request: TranslationRequest):
    try:
        # 번역 실행
        result = translator(request.text)
        return {"translated_text": result[0]["translation_text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))