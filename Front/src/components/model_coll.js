export const fetchTranslation = async (text) => {
    console.log("Model_coll 이벤트 호출됨, 입력:", text);
    try {
      const response = await fetch("http://127.0.0.1:8000/translate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log("번역 결과:", data);
        return data; // 결과 반환
      } else {
        console.error("번역 요청 실패");
      }
    } catch (error) {
      console.error("에러 발생:", error);
    }
  };