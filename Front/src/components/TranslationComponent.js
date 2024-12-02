import React from "react";
import { useNavigate } from "react-router-dom"; // useNavigate 추가
import ConverterForm from "./ConverterForm";
import { fetchTranslation } from "./model_coll"; // fetchTranslation 가져오기

const TranslationComponent = () => {
  const navigate = useNavigate(); // useNavigate 훅 사용

  const modelCollEvent = async (text) => {
    console.log("Model_coll 이벤트 호출됨, 입력:", text);

    try {
      const result = await fetchTranslation(text); // fetchTranslation 호출
      console.log("모델 호출 결과:", result);

      // Result 페이지로 이동하며 데이터를 전달
      navigate("/result", { state: { response: result } });
    } catch (error) {
      console.error("Error during translation:", error);
    }
  };

  return (
    <div>
      <h1>Slang Translator</h1>
      <ConverterForm onConvert={modelCollEvent} /> {/* 이벤트 연결 */}
    </div>
  );
};

export default TranslationComponent;