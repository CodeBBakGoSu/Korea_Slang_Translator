from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

# MODEL_NAME = "hongggggggggggg/korea-slang-translator-kobert"

# # 모델과 토크나이저 로드
# tokenizer = PreTrainedTokenizerFast.from_pretrained("hyunwoongko/kobart")
# model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)

# # 테스트 입력
# input_text = "아 롤하는데 한타에서 졌어"
# input_ids = tokenizer.encode(input_text, return_tensors="pt")
# output_ids = model.generate(input_ids, max_length=50, num_beams=4, early_stopping=True)
# output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

# print("Input:", input_text)
# print("Output:", output_text)

from transformers import PreTrainedTokenizerFast, AutoModelForSeq2SeqLM
import evaluate
from sentence_transformers import SentenceTransformer, util

# 모델 및 토크나이저 로드
model_name = "hongggggggggggg/korea-slang-translator-kobart"
tokenizer = PreTrainedTokenizerFast.from_pretrained("hyunwoongko/kobart")
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# 파일 경로
source_file = "source_texts.txt"
reference_file = "reference_texts.txt"

# 파일 읽기
with open(source_file, "r", encoding="utf-8") as f:
    source_texts = [line.strip() for line in f.readlines()]

with open(reference_file, "r", encoding="utf-8") as f:
    reference_texts = [line.strip() for line in f.readlines()]

# 데이터 정리: 동일한 길이를 보장하고, 최대 300개로 제한
max_samples = 300  # 데이터 개수를 300개로 제한
min_length = min(len(source_texts), len(reference_texts), max_samples)  # 최소 길이 계산
source_texts = source_texts[:min_length]  # 최대 300개 슬라이싱
reference_texts = reference_texts[:min_length]  # 최대 300개 슬라이싱


if not source_texts or not reference_texts:
    raise ValueError("Source or reference texts are empty. Please check the input files.")

# 번역 함수
def translate_texts(model, tokenizer, texts, max_new_tokens=50):
    translated_texts = []
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,  # 새 토큰 길이만 지정
            num_beams=4,  # beam search
            early_stopping=True
        )
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        translated_texts.append(translated_text)
    return translated_texts

# 번역 수행
# 번역 수행: 제한된 source_texts만 번역
translated_texts = translate_texts(model, tokenizer, source_texts[:min_length], max_new_tokens=50)

# 번역된 텍스트와 참조 텍스트 개수 확인
assert len(translated_texts) == len(reference_texts), "Predictions and references count mismatch."

# BLEU 평가
bleu = evaluate.load("bleu")
bleu_score = bleu.compute(predictions=translated_texts, references=[[ref] for ref in reference_texts])

# METEOR 평가
meteor = evaluate.load("meteor")
meteor_score = meteor.compute(predictions=translated_texts, references=reference_texts)

# SBERT 평가
sbert_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
ref_embeddings = sbert_model.encode(reference_texts, convert_to_tensor=True)
translated_embeddings = sbert_model.encode(translated_texts, convert_to_tensor=True)
similarities = util.cos_sim(ref_embeddings, translated_embeddings).diagonal().tolist()
avg_similarity = sum(similarities) / len(similarities)

# 결과 출력
print("BLEU 점수:", bleu_score["bleu"])
print("METEOR 점수:", meteor_score["meteor"])
print("SBERT 유사도 평균:", avg_similarity)




#uvicorn main:app --reload


# from konlpy.tag import Mecab, Hannanum, Kkma
# import jpype

# from konlpy.tag import Okt  # 형태소 분석기 임포트
# okt = Okt()
# print(okt.morphs("아 롤하고 싶다."))

# hannanum = Hannanum()
# print(hannanum.morphs("아 롤하는데 한타에서 졌어."))
# print(hannanum.morphs("내 친구 너무 귀여워"))

# print("[내,친구,너무,커여워]")
# print("[내,친구,너무,귀여워]")

#내 친구가 너무 커엽고 웃기길래 ‘이건 찐텐으로 웃긴다’고 말했어.
