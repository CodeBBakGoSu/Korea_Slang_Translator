import React, { useState } from "react";

const ConverterForm = ({ onConvert }) => {
  const [inputText, setInputText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onConvert(inputText);
  };

  return (
    <form className="converter-form" onSubmit={handleSubmit}>
      <textarea
        placeholder="번역하고 싶은 문장을 입력하시오"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      <button type="submit">Convert</button>
    </form>
  );
};

export default ConverterForm;