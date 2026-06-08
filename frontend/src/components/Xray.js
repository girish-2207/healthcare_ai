import React, { useState } from "react";
import axios from "axios";

const BASE = "http://localhost:8000";

function Xray() {
  const [file, setFile]       = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult]   = useState(null);
  const [loading, setLoading] = useState(false);

  const onFile = (e) => {
    const f = e.target.files[0];
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
  };

  const classify = async () => {
    if (!file) return;
    setLoading(true);
    const form = new FormData();
    form.append("file", file);
    try {
      const res = await axios.post(`${BASE}/predict/xray`, form);
      setResult(res.data);
    } catch {
      setResult({ error: "Classification failed. Try again." });
    }
    setLoading(false);
  };

  return (
    <div>
      <h2 style={{ marginBottom: 12 }}>Chest X-Ray Analysis</h2>

      <input type="file" accept="image/*" onChange={onFile} />

      {preview && (
        <img
          src={preview} alt="xray"
          style={{ width: "100%", maxHeight: 300, objectFit: "contain", margin: "12px 0", borderRadius: 8, border: "1px solid #eee" }}
        />
      )}

      <button className="submit" onClick={classify} disabled={loading || !file}>
        {loading ? "Analyzing..." : "Analyze X-Ray"}
      </button>

      {result && !result.error && (
        <div className="result">
          <strong>Result: </strong>
          <span style={{ color: result.result === "NORMAL" ? "#2ecc71" : "#e74c3c", fontWeight: "bold" }}>
            {result.result}
          </span>
          <span style={{ float: "right" }}>{result.confidence}% confidence</span>
          <div style={{ marginTop: 12 }}>
            <strong>All scores:</strong>
            {Object.entries(result.all_scores).map(([k, v]) => (
              <div key={k} style={{ display: "flex", justifyContent: "space-between", marginTop: 4 }}>
                <span>{k}</span>
                <span>{v}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {result?.error && <div className="result error">{result.error}</div>}
    </div>
  );
}

export default Xray;