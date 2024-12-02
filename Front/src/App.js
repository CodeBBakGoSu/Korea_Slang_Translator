import React, { useState } from "react";
import Header from "./components/Header"; // 헤더 컴포넌트
import ConverterForm from "./components/ConverterForm"; // 사용자 입력 폼
import { fetchTranslation } from "./components/model_coll"; // API 요청 로직

const App = () => {
  // 상태 관리: 변환된 텍스트, 은어 분석, 로딩 상태 추가
  const [convertedText, setConvertedText] = useState(""); // 변환된 텍스트
  const [slangAnalysis, setSlangAnalysis] = useState([]); // 은어 분석 데이터
  const [loading, setLoading] = useState(false); // 로딩 상태
  const [error, setError] = useState(null); // 에러 메시지

  const handleConversion = async (text) => {
    setLoading(true); // 요청 시작 시 로딩 상태 활성화
    setError(null); // 이전 오류 초기화

    try {
      const response = await fetchTranslation(text); // 백엔드에서 변환된 텍스트 가져오기
      setConvertedText(response.translated_sentences[0] || ""); // 변환된 텍스트 저장
      setSlangAnalysis(response.slang_analysis || []); // 은어 분석 데이터 저장
    } catch (err) {
      console.error("Error during conversion:", err);
      setError("변환 요청에 실패했습니다. 다시 시도해주세요."); // 에러 메시지 설정
    } finally {
      setLoading(false); // 요청 완료 후 로딩 상태 비활성화
    }
  };

  return (
    <div className="app-container">
      <Header /> {/* 헤더 */}
      <ConverterForm onConvert={handleConversion} /> {/* 텍스트 입력 */}
      {loading && <p>변환 중입니다...</p>} {/* 로딩 메시지 */}
      {error && <p className="error-message">{error}</p>} {/* 에러 메시지 */}

      {/* 변환된 텍스트 결과 표시 */}
      {convertedText && (
        <div>
          <h2>표준어로 변환된 문장:</h2>
          <p>{convertedText}</p> {/* 번역된 문장 표시 */}
        </div>
      )}

      {/* 은어 분석 결과 표시 */}
      {slangAnalysis.length > 0 && (
        <div>
          <h2>은어 정보:</h2>
          {slangAnalysis.map((slang, index) => (
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
      )}
    </div>
  );
};

export default App;