import { useState } from "react";

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
    <div style={styles.container}>
      <div style={styles.chatBox}>
        {/* Header */}
        <div style={styles.header}>
          <h1 style={styles.title}>🤖 AI Chat Assistant</h1>

          {/* Model Selection */}
          <div style={styles.buttonGroup}>
            <button
              onClick={() => setSelectedModel("ollama")}
              style={{
                ...styles.modelButton,
                ...(selectedModel === "ollama"
                  ? styles.activeButton
                  : styles.inactiveButton),
              }}
            >
              🏠 Lokalnie (Ollama)
            </button>
            <button
              onClick={() => setSelectedModel("openai")}
              style={{
                ...styles.modelButton,
                ...(selectedModel === "openai"
                  ? styles.activeButtonGreen
                  : styles.inactiveButton),
              }}
            >
              🌐 OpenAI API
            </button>
          </div>

          <div style={styles.clearButtonContainer}>
            <button onClick={clearChat} style={styles.clearButton}>
              🗑️ Wyczyść chat
            </button>
          </div>
        </div>

        {/* Chat Messages */}
        <div style={styles.messagesContainer}>
          {messages.length === 0 ? (
            <div style={styles.welcomeMessage}>
              Witaj! Zadaj mi pytanie aby rozpocząć rozmowę 💬
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                style={{
                  ...styles.messageRow,
                  justifyContent:
                    message.sender === "user" ? "flex-end" : "flex-start",
                }}
              >
                <div
                  style={{
                    ...styles.messageBubble,
                    ...(message.sender === "user"
                      ? styles.userMessage
                      : message.sender === "error"
                      ? styles.errorMessage
                      : styles.botMessage),
                  }}
                >
                  <div style={styles.messageHeader}>
                    {message.sender === "user"
                      ? "👤 Ty"
                      : message.sender === "error"
                      ? "❌ Błąd"
                      : "🤖 AI"}
                    <span style={styles.timestamp}>{message.timestamp}</span>
                  </div>
                  <div style={styles.messageText}>{message.text}</div>

                  {/* Metrics for bot messages */}
                  {message.metrics && (
                    <div style={styles.metricsContainer}>
                      <div style={styles.metricsGrid}>
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
                      <div style={styles.modelInfo}>
                        🔧 Model: {message.metrics.model_type}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}

          {isLoading && (
            <div style={styles.messageRow}>
              <div style={{ ...styles.messageBubble, ...styles.botMessage }}>
                <div style={styles.loadingContainer}>
                  <div style={styles.spinner}></div>
                  <span>AI myśli...</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div style={styles.inputArea}>
          <div style={styles.inputContainer}>
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Napisz swoje pytanie..."
              style={styles.textInput}
              rows="2"
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputText.trim()}
              style={{
                ...styles.sendButton,
                ...(isLoading || !inputText.trim()
                  ? styles.disabledButton
                  : {}),
              }}
            >
              {isLoading ? "⏳" : "🚀 Wyślij"}
            </button>
          </div>

          <div style={styles.statusText}>
            Aktualnie używasz:{" "}
            <span style={styles.statusHighlight}>
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

const styles = {
  container: {
    minHeight: "100vh",
    background:
      "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%)",
    padding: "20px",
    fontFamily: "Arial, sans-serif",
  },
  chatBox: {
    maxWidth: "800px",
    margin: "0 auto",
    backgroundColor: "rgba(255, 255, 255, 0.1)",
    backdropFilter: "blur(10px)",
    borderRadius: "20px",
    border: "1px solid rgba(255, 255, 255, 0.2)",
    boxShadow: "0 8px 32px rgba(0, 0, 0, 0.3)",
  },
  header: {
    padding: "30px",
    borderBottom: "1px solid rgba(255, 255, 255, 0.2)",
  },
  title: {
    fontSize: "2rem",
    fontWeight: "bold",
    color: "white",
    textAlign: "center",
    marginBottom: "20px",
    margin: "0 0 20px 0",
  },
  buttonGroup: {
    display: "flex",
    justifyContent: "center",
    gap: "15px",
    marginBottom: "20px",
  },
  modelButton: {
    padding: "12px 24px",
    borderRadius: "12px",
    border: "none",
    fontWeight: "bold",
    cursor: "pointer",
    transition: "all 0.3s ease",
    fontSize: "14px",
  },
  activeButton: {
    backgroundColor: "#3b82f6",
    color: "white",
    transform: "scale(1.05)",
    boxShadow: "0 4px 15px rgba(59, 130, 246, 0.4)",
  },
  activeButtonGreen: {
    backgroundColor: "#10b981",
    color: "white",
    transform: "scale(1.05)",
    boxShadow: "0 4px 15px rgba(16, 185, 129, 0.4)",
  },
  inactiveButton: {
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    color: "rgba(255, 255, 255, 0.8)",
  },
  clearButtonContainer: {
    display: "flex",
    justifyContent: "center",
  },
  clearButton: {
    padding: "8px 16px",
    backgroundColor: "rgba(239, 68, 68, 0.2)",
    color: "rgba(255, 255, 255, 0.8)",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "14px",
    transition: "background-color 0.3s ease",
  },
  messagesContainer: {
    height: "400px",
    overflowY: "auto",
    padding: "20px",
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },
  welcomeMessage: {
    textAlign: "center",
    color: "rgba(255, 255, 255, 0.6)",
    fontSize: "18px",
    marginTop: "100px",
  },
  messageRow: {
    display: "flex",
  },
  messageBubble: {
    maxWidth: "70%",
    padding: "15px",
    borderRadius: "18px",
    wordWrap: "break-word",
  },
  userMessage: {
    backgroundColor: "#3b82f6",
    color: "white",
  },
  botMessage: {
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    color: "white",
    backdropFilter: "blur(5px)",
  },
  errorMessage: {
    backgroundColor: "#ef4444",
    color: "white",
  },
  messageHeader: {
    fontSize: "12px",
    marginBottom: "5px",
    display: "flex",
    justifyContent: "space-between",
  },
  timestamp: {
    opacity: 0.7,
    fontSize: "10px",
  },
  messageText: {
    fontSize: "14px",
    lineHeight: "1.5",
  },
  metricsContainer: {
    marginTop: "10px",
    paddingTop: "10px",
    borderTop: "1px solid rgba(255, 255, 255, 0.2)",
    fontSize: "11px",
    opacity: 0.8,
  },
  metricsGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "5px",
    marginBottom: "5px",
  },
  modelInfo: {
    textAlign: "center",
  },
  loadingContainer: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
  },
  spinner: {
    width: "16px",
    height: "16px",
    border: "2px solid rgba(255, 255, 255, 0.3)",
    borderTop: "2px solid white",
    borderRadius: "50%",
    animation: "spin 1s linear infinite",
  },
  inputArea: {
    padding: "20px",
    borderTop: "1px solid rgba(255, 255, 255, 0.2)",
  },
  inputContainer: {
    display: "flex",
    gap: "15px",
    marginBottom: "10px",
  },
  textInput: {
    flex: 1,
    padding: "12px",
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    backdropFilter: "blur(5px)",
    color: "white",
    border: "1px solid rgba(255, 255, 255, 0.3)",
    borderRadius: "12px",
    resize: "none",
    fontSize: "14px",
    outline: "none",
  },
  sendButton: {
    padding: "12px 24px",
    background: "linear-gradient(45deg, #3b82f6, #8b5cf6)",
    color: "white",
    border: "none",
    borderRadius: "12px",
    cursor: "pointer",
    fontWeight: "bold",
    fontSize: "14px",
    transition: "transform 0.2s ease",
  },
  disabledButton: {
    opacity: 0.5,
    cursor: "not-allowed",
    transform: "none",
  },
  statusText: {
    textAlign: "center",
    color: "rgba(255, 255, 255, 0.6)",
    fontSize: "14px",
  },
  statusHighlight: {
    fontWeight: "bold",
    color: "white",
  },
};
