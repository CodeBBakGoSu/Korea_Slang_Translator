const ResultDisplay = ({ data }) => {
    if (!data) {
      return <p>No data available</p>;
    }
  
    return (
      <div>
        <h2>Translated Text:</h2>
        <p>{data.translated_text}</p>
        <h3>Slang Analysis:</h3>
        <ul>
          {data.slang_analysis.map((item, index) => (
            <li key={index}>
              <strong>{item.word}</strong>: {item.meaning}
            </li>
          ))}
        </ul>
      </div>
    );
  };
  
  export default ResultDisplay;