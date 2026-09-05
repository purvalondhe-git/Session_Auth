import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <section>
      <div className="hero">
        <div>
          <span className="badge">Authenticated</span>
          <h1>Welcome, {user.name} 👋</h1>
          <p className="muted">Your session is active and protected by the backend session cookie.</p>
        </div>
      </div>

      <div className="grid">
        <div className="card">
          <h3>Account</h3>
          <p><strong>Name:</strong> {user.name}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Role:</strong> {user.role}</p>
        </div>

        <div className="card">
          <h3>Session Security</h3>
          <p>Your session ID is stored in an HTTP-only cookie, so JavaScript does not read the session ID.</p>
          <Link className="primary-link" to="/sessions">Manage Sessions →</Link>
        </div>
      </div>
    </section>
  );
}