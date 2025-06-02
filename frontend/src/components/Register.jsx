import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Register.css';

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setErrorMessage("");
  
    try {
      const response = await axios.post("http://localhost:8000/register", {
        email,
        password,
      });
  
      if (response.data.message === "Usuario registrado exitosamente") {
        console.log("Cuenta creada con éxito");
        navigate("/");
      }
    } catch (error) {
      console.error("Error al registrar:", error);
      setErrorMessage("Error al registrar el usuario: " + (error.response?.data?.detail || "Error desconocido"));
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <h2>Crear cuenta</h2>
        <form onSubmit={handleRegister}>
          <div>
            <label htmlFor="email">Correo electrónico</label>
            <input
              type="email"
              id="email"
              placeholder="ejemplo@correo.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <br />
          <div>
            <label htmlFor="password">Contraseña</label>
            <input
              type="password"
              id="password"
              placeholder="*********"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {/* Mensaje de error con fondo rojo */}
          {errorMessage && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {errorMessage}
            </div>
          )}

          <button type="submit">Crear cuenta</button>
        </form>
      </div>
    </div>
  );
}

export default Register;
