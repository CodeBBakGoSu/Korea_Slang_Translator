from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
from rank_bm25 import BM25Okapi
import logging

# FastAPI 앱 초기화
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 앱 URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 모델 로드
MODEL_NAME = "hongggggggggggg/korea-slang-translator-kobert"
MODEL_DIR = "/Users/hong-gihyeon/.cache/huggingface/hub/models--hongggggggggggg--korea-slang-translator-kobert/snapshots/cca99825468668b21a8d6de2c86a664ec1b4627a"
tokenizer = PreTrainedTokenizerFast.from_pretrained("hyunwoongko/kobart")
model = BartForConditionalGeneration.from_pretrained(MODEL_DIR, local_files_only=True)

# SQLite 데이터베이스 연결 설정
DB_PATH = "/Users/hong-gihyeon/Desktop/Data_Slang/Back/word_info.db"

def find_transformed_words(input_text: str, result_text: str) -> list:
    """
    입력 문장과 결과 문장을 비교하여 변환된 단어를 찾습니다.
    """
    input_words = set(input_text.split())
    result_words = set(result_text.split())
    transformed_words = list(input_words - result_words)  # 결과 문장에 없는 단어
    return transformed_words

import logging

# 로깅 설정: DEBUG 이상 수준으로 로그 출력
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn")

def bm25_match_candidates(transformed_words, slang_dictionary):
    slang_words = list(slang_dictionary.keys())
    bm25 = BM25Okapi([word.split() for word in slang_words])  # 은어 단어를 토큰화하여 BM25에 입력

    results = []
    for word in transformed_words:
        print(f"Searching for: {word}")  # 로그 대신 print로 확인
        logger.info(f"Searching for: {word}")  # 검색하는 단어 로그 출력
        scores = bm25.get_scores(word.split())  # 변환된 단어의 유사도 점수 계산
        max_index = scores.argmax()  # 가장 높은 점수의 단어 인덱스
        print(f"Scores: {scores}")  # 점수 확인
        logger.info(f"Scores: {scores}")  # 점수 로그 출력
        
        if scores[max_index] > 0:  # 유사도가 0보다 큰 경우에만 추가
            matched_slang = slang_words[max_index]
            meaning = slang_dictionary[matched_slang]
            bm25_score = scores[max_index]
            
            # 결과 로그 출력
            print(f"Matched Slang: {matched_slang}, Meaning: {meaning}, BM25 Score: {bm25_score}")  # 결과 확인
            logger.info(f"Matched Slang: {matched_slang}, Meaning: {meaning}, BM25 Score: {bm25_score}")
            
            results.append({
                "original_word": word,
                "matched_slang": matched_slang,
                "meaning": meaning,
                "bm25_score": bm25_score
            })

    return results

# 요청 데이터 스키마 정의
class TranslationRequest(BaseModel):
    text: str  # 한 문단 전체 텍스트

def fetch_slang_from_db():
    """
    데이터베이스에서 은어 단어를 조회하여 딕셔너리로 반환합니다.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT Word, WordDefine FROM WordInfo")
    slang_dictionary = {row[0].lower(): row[1] for row in cursor.fetchall()}
    conn.close()
    return slang_dictionary

def split_into_sentences(text: str) -> list:
    """
    텍스트를 문장 단위로 분리합니다.
    간단한 마침표 기준으로 문장을 나눕니다.
    """
    return [sentence.strip() for sentence in text.split('.') if sentence.strip()]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Slang Translator API!"}

@app.post("/translate")
def translate_and_analyze(request: TranslationRequest):
    """
    번역 API: 입력된 문단을 문장 단위로 분리하고,
    각 문장을 한국어 모델로 변환하며, 은어 단어를 분석하여 결과 반환
    """
    try:
        # 문단 -> 문장 리스트
        sentences = split_into_sentences(request.text)

        # 데이터베이스에서 은어 단어 로드
        slang_dictionary = fetch_slang_from_db()

        translated_sentences = []
        slang_used = []

        # BM25 준비
        slang_words = list(slang_dictionary.keys())
        bm25 = BM25Okapi([word.split() for word in slang_words])  # 은어 단어 토큰화

        for sentence in sentences:
            # 문장 토크나이즈
            input_ids = tokenizer.encode(sentence, return_tensors="pt")

            # 모델 추론
            output_ids = model.generate(input_ids, max_length=50, num_beams=4, early_stopping=True)

            # 생성된 텍스트 디코딩
            translated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            translated_sentences.append(translated_text)

            # 입력 문장과 번역 결과 비교
            transformed_words = find_transformed_words(sentence, translated_text)

            # BM25로 은어 후보 찾기
            for word in transformed_words:
                scores = bm25.get_scores(word.split())  # 변환된 단어의 유사도 점수 계산
                max_index = scores.argmax()  # 가장 높은 점수의 인덱스
                if scores[max_index] > 0:  # 유사도가 0보다 큰 경우에만 추가
                    slang_used.append({
                        "word": word,
                        "matched_slang": slang_words[max_index],
                        "meaning": slang_dictionary[slang_words[max_index]],
                        "bm25_score": scores[max_index]
                    })

        return {
            "input_text": request.text,
            "translated_sentences": translated_sentences,
            "slang_analysis": slang_used,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# uvicorn main:app --reload