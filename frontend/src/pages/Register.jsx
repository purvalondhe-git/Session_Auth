import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function update(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function submit(e) {
    e.preventDefault();
    setMessage("");
    setError("");

    if (form.password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    setLoading(true);
    try {
      const result = await register(form.name, form.email, form.password);
      setMessage(result.message || "Registration successful");
      setTimeout(() => navigate("/login"), 800);
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="auth-card">
      <h1>Create account</h1>
      <p className="muted">Register for FocusFlow.</p>

      {error && <div className="alert error">{error}</div>}
      {message && <div className="alert success">{message}</div>}

      <form onSubmit={submit}>
        <label>Name</label>
        <input
          name="name"
          value={form.name}
          onChange={update}
          required
          placeholder="Your name"
        />

        <label>Email</label>
        <input
          name="email"
          type="email"
          value={form.email}
          onChange={update}
          required
          placeholder="you@example.com"
        />

        <label>Password</label>
        <input
          name="password"
          type="password"
          value={form.password}
          onChange={update}
          minLength="6"
          required
          placeholder="At least 6 characters"
        />

        <button className="primary" disabled={loading}>
          {loading ? "Creating..." : "Register"}
        </button>
      </form>

      <p className="footer-text">
        Already registered? <Link to="/login">Login</Link>
      </p>
    </section>
  );
}