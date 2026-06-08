import React, { useState, useEffect } from "react";
import axios from "axios";

const BASE = "http://localhost:8000";

function Disease() {
  const [symptoms, setSymptoms]   = useState([]);
  const [selected, setSelected]   = useState([]);
  const [result, setResult]       = useState(null);
  const [loading, setLoading]     = useState(false);
  const [search, setSearch]       = useState("");

  useEffect(() => {
    axios.get(`${BASE}/predict/symptoms`)
      .then(res => setSymptoms(res.data.symptoms))
      .catch(() => {});
  }, []);

  const toggle = (s) => {
    setSelected(prev =>
      prev.includes(s) ? prev.filter(x => x !== s) : [...prev, s]
    );
  };

  const predict = async () => {
    if (selected.length === 0) return;
    setLoading(true);
    try {
      const res = await axios.post(`${BASE}/predict/disease`, { symptoms: selected });
      setResult(res.data);
    } catch {
      setResult({ error: "Prediction failed. Try again." });
    }
    setLoading(false);
  };

  const filtered = symptoms.filter(s =>
    s.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <h2 style={{ marginBottom: 12 }}>Disease Prediction</h2>

      <input
        placeholder="Search symptoms..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />

      <div style={{ height: 200, overflowY: "auto", border: "1px solid #eee", borderRadius: 8, padding: 8, marginBottom: 10 }}>
        {filtered.map(s => (
          <label key={s} style={{ display: "block", padding: "4px 8px", cursor: "pointer", borderRadius: 4, background: selected.includes(s) ? "#dbeafe" : "transparent" }}>
            <input
              type="checkbox"
              checked={selected.includes(s)}
              onChange={() => toggle(s)}
              style={{ width: "auto", marginRight: 8 }}
            />
            {s.replace(/_/g, " ")}
          </label>
        ))}
      </div>

      <p style={{ fontSize: 13, color: "#666", marginBottom: 8 }}>
        Selected: {selected.length} symptoms
      </p>

      <button className="submit" onClick={predict} disabled={loading}>
        {loading ? "Predicting..." : "Predict Disease"}
      </button>

      {result && !result.error && (
        <div className="result">
          <strong>Top Predictions:</strong>
          {result.predictions.map((p, i) => (
            <div key={i} style={{ marginTop: 8 }}>
              <span style={{ fontWeight: "bold", color: i === 0 ? "#2ecc71" : "#555" }}>
                {i + 1}. {p.disease}
              </span>
              <span style={{ float: "right", color: "#3498db" }}>{p.confidence}%</span>
            </div>
          ))}
        </div>
      )}

      {result?.error && <div className="result error">{result.error}</div>}
    </div>
  );
}

export default Disease;