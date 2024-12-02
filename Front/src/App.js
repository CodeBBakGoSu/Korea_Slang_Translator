import React, { useState } from "react";
import Header from "./components/Header";
import ConverterForm from "./components/ConverterForm";
import ResultDisplay from "./components/ResultDisplay";

const App = () => {
  const [convertedText, setConvertedText] = useState("");

  const handleConversion = (text) => {
    // 간단한 슬랭 변환 로직 (임시 예제)
    const slangDict = {
      hello: "yo",
      thanks: "thx",
      awesome: "lit",
    };

    const converted = text
      .split(" ")
      .map((word) => slangDict[word.toLowerCase()] || word)
      .join(" ");

    setConvertedText(converted);
  };

  return (
    <div className="app-container">
      <Header />
      <ConverterForm onConvert={handleConversion} />
      <ResultDisplay result={convertedText} />
    </div>
  );
};

export default App;