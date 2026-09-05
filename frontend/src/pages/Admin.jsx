import { useEffect, useState } from "react";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function Admin() {
  const { user } = useAuth();
  const [users, setUsers] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (user?.role !== "admin") return;

    Promise.all([
      api.get("/admin/users"),
      api.get("/admin/sessions")
    ])
      .then(([usersResponse, sessionsResponse]) => {
        setUsers(usersResponse.data);
        setSessions(sessionsResponse.data);
      })
      .catch((err) => {
        setError(err.response?.data?.detail || "Admin data could not be loaded");
      });
  }, [user]);

  if (user?.role !== "admin") {
    return <div className="card">Access denied. Admin role required.</div>;
  }

  return (
    <section>
      <h1>Admin Panel</h1>
      <p className="muted">System users and sessions.</p>

      {error && <div className="alert error">{error}</div>}

      <div className="grid">
        <div className="card">
          <h2>Users ({users.length})</h2>
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>Name</th><th>Email</th><th>Role</th></tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr key={u.id}>
                    <td>{u.name}</td>
                    <td>{u.email}</td>
                    <td>{u.role}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <h2>Sessions ({sessions.length})</h2>
          <div className="table-wrap">
            <table>
              <thead>
                <tr><th>User ID</th><th>Device</th><th>Expires</th></tr>
              </thead>
              <tbody>
                {sessions.map((s) => (
                  <tr key={s.session_id}>
                    <td>{s.user_id}</td>
                    <td>{s.device}</td>
                    <td>{s.expires_at ? new Date(s.expires_at).toLocaleString() : "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}