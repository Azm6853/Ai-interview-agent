// src/App.js
import React, { useState } from 'react';
import './styles.css';
import axios from 'axios';

const API = process.env.REACT_APP_API_BASE_URL;

function App() {
  const [stage, setStage] = useState('upload');
  const [resumeData, setResumeData] = useState(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState('');

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const res = await axios.post(`${API}/upload_resume`, formData);
    setResumeData(res.data);
    setStage('show-role');
  };

  const startInterview = async () => {
    const role = resumeData?.matched_role?.matched_role || 'Software Engineer';
    const res = await axios.post(`${API}/start_interview`, { role });
    setQuestion(res.data.question);
    setStage('interview');
  };

  const handleSubmitAnswer = async () => {
    const res = await axios.post(`${API}/ask_question`, { answer });
    if (res.data.stage === 'complete') {
      setFeedback(res.data.last_question_feedback?.feedback);
      setStage('complete');
    } else {
      setQuestion(res.data.question);
      setFeedback(res.data.last_question_feedback?.feedback);
      setAnswer('');
    }
  };

  return (
    <div className="app-container">
      <h1>AI Interview Agent</h1>

      {stage === 'upload' && (
        <div>
          <h2>Upload your resume (PDF)</h2>
          <input type="file" accept="application/pdf" onChange={handleUpload} />
        </div>
      )}

      {stage === 'show-role' && resumeData && (
        <div>
          <h2>Matched Role: {resumeData.matched_role.matched_role}</h2>
          <pre>{JSON.stringify(resumeData.parsed_resume, null, 2)}</pre>
          <button onClick={startInterview}>Start Interview</button>
        </div>
      )}

      {stage === 'interview' && (
        <div>
          <h2>Interview Stage</h2>
          <p><strong>Question:</strong> {question}</p>
          {feedback && <p className="feedback">Last Feedback: {feedback}</p>}
          <textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Type your answer here"
          />
          <button onClick={handleSubmitAnswer}>Submit Answer</button>
        </div>
      )}

      {stage === 'complete' && (
        <div>
          <h2>Interview Complete 🎉</h2>
          <p>Final Feedback: {feedback}</p>
        </div>
      )}
    </div>
  );
}

export default App;
