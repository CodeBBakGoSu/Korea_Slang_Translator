import React, { useState } from "react";
import ResultDisplay from "./ResultDisplay"; // ResultDisplay 임포트

const TranslationComponent = () => {
  const [inputText, setInputText] = useState("");
  const [convertedText, setConvertedText] = useState("");

  // handleTranslation 함수 정의

  const handleTranslate = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/translate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText }),
      });
  
      if (response.ok) {
        const data = await response.json();
        setResponseData(data); // 전체 JSON 저장
      } else {
        console.error("Failed to fetch translation");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <h1>Slang Translator</h1>
      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)} // 입력 변화 처리
        placeholder="Enter text to translate"
      />
      <button onClick={handleTranslation}>Translate</button> {/* 이벤트 연결 */}
      {/* ResultDisplay 컴포넌트로 convertedText 전달 */}
      <ResultDisplay text={setResponseData} />
    </div>
  );
};

export default TranslationComponent;