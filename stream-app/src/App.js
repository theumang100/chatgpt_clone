import React, { useState } from 'react';

function App() {
  const [response, setResponse] = useState('');

  const handleGenerate = async () => {
    try {
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: 'Hello' }),
      });

      const reader = response.body.getReader();
      let chunks = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        chunks += new TextDecoder().decode(value);
        setResponse(chunks);
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <button onClick={handleGenerate}>Generate</button>
      <pre>{response}</pre>
    </div>
  );
}

export default App;
