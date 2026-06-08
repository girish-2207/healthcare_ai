import React, { useState } from "react";
import Chat from "./components/Chat";
import Disease from "./components/Disease";
import Xray from "./components/Xray";
import Medicine from "./components/Medicine";
import "./App.css";

function App() {
  const [tab, setTab] = useState("chat");

  return (
    <div className="app">
      <h1>Healthcare AI</h1>
      <div className="tabs">
        <button onClick={() => setTab("chat")}     className={tab === "chat"     ? "active" : ""}>Chatbot</button>
        <button onClick={() => setTab("disease")}  className={tab === "disease"  ? "active" : ""}>Disease</button>
        <button onClick={() => setTab("xray")}     className={tab === "xray"     ? "active" : ""}>X-Ray</button>
        <button onClick={() => setTab("medicine")} className={tab === "medicine" ? "active" : ""}>Medicine</button>
      </div>
      <div className="content">
        {tab === "chat"     && <Chat />}
        {tab === "disease"  && <Disease />}
        {tab === "xray"     && <Xray />}
        {tab === "medicine" && <Medicine />}
      </div>
    </div>
  );
}

export default App;