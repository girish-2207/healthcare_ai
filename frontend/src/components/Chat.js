import React, { useState } from "react";
import axios from "axios";

const BASE = "http://localhost:8000";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput]       = useState("");
  const [loading, setLoading]   = useState(false);

  const send = async () => {
    if (!input.trim()) return;
    const userMsg = { role: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post(`${BASE}/chat`, {
        user_id: "user1",
        query: input,
      });
      const botMsg = {
        role: "bot",
        text: res.data.response,
        sources: res.data.sources,
        intent: res.data.intent,
      };
      setMessages(prev => [...prev, botMsg]);
    } catch {
      setMessages(prev => [...prev, { role: "bot", text: "Error. Try again." }]);
    }
    setLoading(false);
  };

  const reset = async () => {
    await axios.post(`${BASE}/chat/reset`, { user_id: "user1" });
    setMessages([]);
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 12 }}>
        <h2>Medical Chatbot</h2>
        <button onClick={reset} style={{ padding: "6px 12px", cursor: "pointer", borderRadius: 6, border: "1px solid #ddd" }}>
          Clear
        </button>
      </div>

      <div style={{ height: 380, overflowY: "auto", border: "1px solid #eee", borderRadius: 8, padding: 12, marginBottom: 12 }}>
        {messages.length === 0 && (
          <p style={{ color: "#aaa", textAlign: "center", marginTop: 160 }}>Ask a medical question...</p>
        )}
        {messages.map((m, i) => (
          <div key={i} style={{
            marginBottom: 12,
            textAlign: m.role === "user" ? "right" : "left",
          }}>
            <span style={{
              display: "inline-block", padding: "8px 14px",
              borderRadius: 12, maxWidth: "80%",
              background: m.role === "user" ? "#3498db" : "#f0f2f5",
              color: m.role === "user" ? "white" : "#2c3e50",
              fontSize: 14, whiteSpace: "pre-wrap",
            }}>
              {m.text}
            </span>
            {m.sources && m.sources.length > 0 && (
              <div style={{ fontSize: 11, color: "#aaa", marginTop: 4 }}>
                Source: {m.sources.join(", ")}
              </div>
            )}
          </div>
        ))}
        {loading && <p style={{ color: "#aaa", fontSize: 13 }}>Thinking...</p>}
      </div>

      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && send()}
          placeholder="Type your question..."
          style={{ margin: 0 }}
        />
        <button onClick={send} className="submit" style={{ width: "auto", margin: 0, padding: "10px 20px" }}>
          Send
        </button>
      </div>
    </div>
  );
}

export default Chat;