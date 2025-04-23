import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import './Login.css';

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState(""); // Estado para mostrar errores
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMessage(""); // Limpiar mensaje de error anterior

    try {
      const res = await axios.post("http://localhost:8000/login", {
        email,
        password,
      });

      if (res.data.success) {
        navigate("/chat");
      }
    } catch (error) {
      if (error.response && error.response.status === 401) {
        setErrorMessage("Credenciales inválidas");
      } else {
        setErrorMessage("Error al conectar con el servidor");
      }
    }
  };

  return (
    <main className="login-page" role="main">
      <section className="login-container" aria-label="Formulario de inicio de sesión">
        <h2 className="login-title">Login</h2>

        <form onSubmit={handleLogin} className="login-form" noValidate>
          <div className="form-group">
            <label htmlFor="email">Correo electrónico</label>
            <input
              id="email"
              type="email"
              placeholder="ejemplo@correo.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              aria-label="Correo electrónico"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              aria-label="Contraseña"
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

          <button type="submit" className="login-button">Iniciar Sesión</button>
        </form>

        <div className="register-link">
          <p>¿No tienes cuenta? <Link to="/register">Crear cuenta</Link></p>
        </div>
      </section>
    </main>
  );
}

export default Login;
