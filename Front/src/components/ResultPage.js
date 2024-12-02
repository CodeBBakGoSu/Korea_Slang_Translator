import React from "react";
import { useLocation } from "react-router-dom"; // useLocation 훅 사용

const ResultPage = () => {
  const location = useLocation(); // 전달된 데이터 받기
  const { response } = location.state || {}; // 응답 데이터 구조 분해
  const { translated_sentences, slang_analysis } = response || {};

  return (
    <div>
      <h1>Translation Result</h1>
      <div>
        <h2>Translated Sentences:</h2>
        <p>{translated_sentences?.join(" ")}</p> {/* 번역된 문장 표시 */}
      </div>
      <div>
        <h2>Slang Analysis:</h2>
        {slang_analysis?.map((slang, index) => (
          <div key={index}>
            <p>
              <strong>Word:</strong> {slang.word}
            </p>
            <p>
              <strong>Matched Slang:</strong> {slang.matched_slang}
            </p>
            <p>
              <strong>Meaning:</strong> {slang.meaning}
            </p>
            <p>
              <strong>BM25 Score:</strong> {slang.bm25_score}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResultPage;