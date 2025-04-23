import { useState } from "react";
import axios from "axios";
import './ChatBox.css';

function ChatBox() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    try {
      const res = await axios.post("http://localhost:8000/chat", { message: input });
      setResponse(res.data.response);  // Actualiza la respuesta con lo que regresa la API
    } catch (error) {
      console.error("Error al enviar el mensaje:", error);
      setResponse("Error en la comunicación con el servidor.");
    }
  };

  return (
    <div className="chatbox-wrapper">
      <div className="chatbox-container">
        <h2 className="chatbox-title">Radiant IA</h2>
  
        <div className="chatbox-messages">
          <p className="chatbox-response">
            <strong>Respuesta:</strong> {response}
          </p>
        </div>
  
        <div className="chatbox-input-area">
          <input
            className="chatbox-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribe algo..."
            aria-label="Entrada de mensaje"
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
