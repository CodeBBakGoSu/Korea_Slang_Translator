import React from "react";

const ResultDisplay = ({ result }) => {
  return (
    <div className="result-display">
      <h2>Converted Text:</h2>
      <p>{result || "Your converted text will appear here."}</p>
    </div>
  );
};

export default ResultDisplay;