import React, { useState } from "react";
import axios from "axios";

const BASE = "http://localhost:8000";

const DISEASES = ["Typhoid", "Diabetes", "Pneumonia", "Malaria", "Tuberculosis"];

function Medicine() {
  const [disease, setDisease] = useState("");
  const [result, setResult]   = useState(null);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    if (!disease) return;
    setLoading(true);
    try {
      const res = await axios.get(`${BASE}/medicine/${disease}`);
      setResult(res.data);
    } catch {
      setResult({ error: "Search failed. Try again." });
    }
    setLoading(false);
  };

  return (
    <div>
      <h2 style={{ marginBottom: 12 }}>Medicine Recommendation</h2>

      <select value={disease} onChange={e => setDisease(e.target.value)}>
        <option value="">Select a disease</option>
        {DISEASES.map(d => <option key={d} value={d}>{d}</option>)}
      </select>

      <button className="submit" onClick={search} disabled={loading || !disease}>
        {loading ? "Searching..." : "Get Medicines"}
      </button>

      {result && !result.error && (
        <div className="result">
          <strong>Medicines for {result.disease}:</strong>
          {result.medicines.length === 0 ? (
            <p style={{ marginTop: 8, color: "#aaa" }}>No medicines found.</p>
          ) : (
            result.medicines.map((m, i) => (
              <div key={i} style={{ marginTop: 12, padding: 10, background: "#fff", borderRadius: 8, border: "1px solid #eee" }}>
                <div style={{ fontWeight: "bold", color: "#2c3e50" }}>{m.medicine}</div>
                <div style={{ fontSize: 13, color: "#555", marginTop: 4 }}>Dosage: {m.dosage}</div>
                <div style={{ fontSize: 13, color: "#e74c3c", marginTop: 2 }}>Side effects: {m.side_effects}</div>
              </div>
            ))
          )}
          <p style={{ fontSize: 12, color: "#aaa", marginTop: 12 }}>{result.message}</p>
        </div>
      )}

      {result?.error && <div className="result error">{result.error}</div>}
    </div>
  );
}

export default Medicine;