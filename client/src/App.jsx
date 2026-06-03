import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [category, setCategory] = useState("");
  const [papers, setPapers] = useState([]);

  const handleSubmit = async () => {
    const res = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    const data = await res.json();

    console.log(data);

    // FIXED HERE
    setCategory(data.prediction || "");

    setPapers(data.recommendations || []);
  };

  return (
    <div className="container">
      <div className="card">
        <h1>📄 Research Paper Classifier & Recommender</h1>

        <textarea
          placeholder="Enter paper title or abstract..."
          onChange={(e) => setText(e.target.value)}
        />

        <button onClick={handleSubmit}>Analyze</button>

        {category && (
          <>
            <h2>Category: {category}</h2>

            <h3>Recommended Papers:</h3>

            <ul>
              {papers.map((p, i) => (
                <li key={i}>{p}</li>
              ))}
            </ul>
          </>
        )}
      </div>
    </div>
  );
}

export default App;