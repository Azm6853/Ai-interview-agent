// src/App.js
import React, { useState } from 'react';

const API_URL = "https://ai-interview-agent-q22m.onrender.com";

export default function App() {
  const [file, setFile] = useState(null);
  const [parsedData, setParsedData] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [stage, setStage] = useState("");
  const [feedback, setFeedback] = useState("");
  const [interviewStarted, setInterviewStarted] = useState(false);

  const handleFileUpload = async () => {
    if (!file) return alert("Please select a PDF resume.");
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_URL}/upload_resume`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setParsedData(data);
    alert("Resume uploaded and parsed. Matched role: " + data.matched_role.matched_role);
  };

  const startInterview = async () => {
    const res = await fetch(`${API_URL}/start_interview`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role: parsedData?.matched_role.matched_role || "Software Engineer" }),
    });
    const data = await res.json();
    setInterviewStarted(true);
    setQuestion(data.question);
    setStage(data.stage);
    setFeedback("");
  };

  const askNext = async () => {
    const res = await fetch(`${API_URL}/ask_question`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answer }),
    });
    const data = await res.json();
    setQuestion(data.question || "");
    setStage(data.stage);
    setFeedback(data.last_question_feedback?.feedback || "");
    setAnswer("");

    if (data.stage === "complete") {
      alert("Interview complete!");
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>AI Interview Agent</h1>

      <div>
        <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleFileUpload}>Upload Resume</button>
      </div>

      {parsedData && !interviewStarted && (
        <div style={{ marginTop: "1rem" }}>
          <p><strong>Matched Role:</strong> {parsedData?.matched_role?.matched_role}</p>
          <button onClick={startInterview}>Start Interview</button>
        </div>
      )}

      {interviewStarted && (
        <div style={{ marginTop: "2rem" }}>
          <p><strong>Stage:</strong> {stage}</p>
          <p><strong>Question:</strong> {question}</p>

          <textarea
            rows="4"
            style={{ width: "100%" }}
            placeholder="Your answer..."
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />

          <button onClick={askNext} style={{ marginTop: "1rem" }}>Submit Answer</button>

          {feedback && (
            <div style={{ marginTop: "1rem", background: "#f0f0f0", padding: "1rem" }}>
              <p><strong>Feedback:</strong> {feedback}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

