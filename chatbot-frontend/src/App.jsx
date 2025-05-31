import { useState } from "react";
import "./ChatBot.css";

export default function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [selectedModel, setSelectedModel] = useState("ollama");
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputText,
      sender: "user",
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const currentInput = inputText;
    setInputText("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: currentInput,
          model_type: selectedModel,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const botMessage = {
        id: Date.now() + 1,
        text: data.answer,
        sender: "bot",
        timestamp: new Date().toLocaleTimeString(),
        metrics: {
          vector_similarity: data.vector_similarity,
          semantic_similarity: data.semantic_similarity,
          scoreBleu: data.scoreBleu,
          scoreRouge: data.scoreRouge,
          model_type: data.model_type,
        },
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: `Błąd: ${error.message}`,
        sender: "error",
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {/* Header */}
        <div className="chat-header">
          <h1 className="chat-title">🤖 AI Chat Assistant</h1>

          {/* Model Selection */}
          <div className="button-group">
            <button
              onClick={() => setSelectedModel("ollama")}
              className={`model-button ${
                selectedModel === "ollama" ? "active-blue" : "inactive"
              }`}
            >
              🏠 Lokalnie (Ollama)
            </button>
            <button
              onClick={() => setSelectedModel("openai")}
              className={`model-button ${
                selectedModel === "openai" ? "active-green" : "inactive"
              }`}
            >
              🌐 OpenAI API
            </button>
          </div>

          <div className="clear-button-container">
            <button onClick={clearChat} className="clear-button">
              🗑️ Wyczyść chat
            </button>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="welcome-message">
              Witaj! Zadaj mi pytanie aby rozpocząć rozmowę 💬
            </div>
          ) : (
            messages.map((message) => (
              <div key={message.id} className={`message-row ${message.sender}`}>
                <div className={`message-bubble ${message.sender}`}>
                  <div className="message-header">
                    {message.sender === "user"
                      ? "👤 Ty"
                      : message.sender === "error"
                      ? "❌ Błąd"
                      : "🤖 AI"}
                    <span className="timestamp">{message.timestamp}</span>
                  </div>
                  <div className="message-text">{message.text}</div>

                  {/* Metrics for bot messages */}
                  {message.metrics && (
                    <div className="metrics-container">
                      <div className="metrics-grid">
                        <div>
                          📊 Vector:{" "}
                          {message.metrics.vector_similarity.toFixed(4)}
                        </div>
                        <div>
                          🎯 Semantic:{" "}
                          {message.metrics.semantic_similarity.toFixed(4)}
                        </div>
                        <div>
                          📝 BLEU: {message.metrics.scoreBleu.toFixed(4)}
                        </div>
                        <div>
                          📋 ROUGE: {message.metrics.scoreRouge.toFixed(4)}
                        </div>
                      </div>
                      <div className="model-info">
                        🔧 Model: {message.metrics.model_type}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}

          {isLoading && (
            <div className="message-row bot">
              <div className="message-bubble bot">
                <div className="loading-container">
                  <div className="spinner"></div>
                  <span>AI myśli...</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="input-area">
          <div className="input-container">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Napisz swoje pytanie..."
              className="text-input"
              rows="2"
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputText.trim()}
              className="send-button"
            >
              {isLoading ? "⏳" : "🚀 Wyślij"}
            </button>
          </div>

          <div className="status-text">
            Aktualnie używasz:{" "}
            <span className="status-highlight">
              {selectedModel === "ollama"
                ? "🏠 Lokalny model"
                : "🌐 OpenAI API"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
