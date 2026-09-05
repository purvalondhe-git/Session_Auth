import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const from = location.state?.from?.pathname || "/dashboard";

  function update(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function submit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login(form.email, form.password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="auth-card">
      <h1>Welcome back</h1>
      <p className="muted">Sign in to your FocusFlow account.</p>

      {error && <div className="alert error">{error}</div>}

      <form onSubmit={submit}>
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
          required
          placeholder="Minimum 6 characters"
        />

        <button className="primary" disabled={loading}>
          {loading ? "Signing in..." : "Login"}
        </button>
      </form>

      <p className="footer-text">
        Don't have an account? <Link to="/register">Create one</Link>
      </p>
    </section>
  );
}