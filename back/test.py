from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

MODEL_NAME = "hongggggggggggg/korea-slang-translator-kobert"



# 모델과 토크나이저 로드
tokenizer = PreTrainedTokenizerFast.from_pretrained("hyunwoongko/kobart")
model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)

# 테스트 입력
input_text = "아 롤하는데 한타에서 졌어"
input_ids = tokenizer.encode(input_text, return_tensors="pt")
output_ids = model.generate(input_ids, max_length=50, num_beams=4, early_stopping=True)
output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("Input:", input_text)
print("Output:", output_text)