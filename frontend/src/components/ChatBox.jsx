import { useState, useRef, useEffect } from "react";
import axios from "axios";
import './ChatBox.css';

function ChatBox() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newUserMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, newUserMessage]);
    setInput("");

    try {
      const res = await axios.post("http://localhost:8000/chat", { message: input });
      const aiMessage = { sender: "ai", text: res.data.response };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = {
        sender: "ai",
        text: "Ocurrió un error al comunicarse con Radiant AI.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  // Función que se ejecuta al presionar una tecla
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); // Prevenir el comportamiento por defecto de la tecla Enter (como un salto de línea)
      sendMessage(); // Llamamos a la función de envío del mensaje
    }
  };

  return (
    <div className="chatbox-wrapper">
      <div className="chatbox-container">
        <h2 className="chatbox-title">Radiant IA</h2>

        <div className="chatbox-messages">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chatbox-message-wrapper ${msg.sender === "user" ? "user" : "ai"}`}
            >
              <img
                src={msg.sender === "user" ? "/user.png" : "/radiant.png"}
                alt={msg.sender === "user" ? "Usuario" : "Radiant AI"}
                className="chatbox-avatar"
              />
              <p className="chatbox-message">{msg.text}</p>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>

        <div className="chatbox-input-area">
          <input
            className="chatbox-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown} // Añadimos el evento onKeyDown
            placeholder="Escribe algo..."
          />
          <button className="chatbox-button" onClick={sendMessage}>
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatBox;
