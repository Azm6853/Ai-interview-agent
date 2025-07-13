// src/api.js

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://ai-interview-agent-q22m.onrender.com';

export async function uploadResume(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload_resume`, {
    method: "POST",
    body: formData
  });

  return await response.json();
}

export async function startInterview(role) {
  const response = await fetch(`${API_BASE_URL}/start_interview`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role })
  });

  return await response.json();
}

export async function askNextQuestion(answer) {
  const response = await fetch(`${API_BASE_URL}/ask_question`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answer })
  });

  return await response.json();
}

