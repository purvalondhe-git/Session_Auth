import { useEffect, useState } from "react";
import api from "../services/api";

export default function Sessions() {
  const [sessions, setSessions] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  async function loadSessions() {
    try {
      const response = await api.get("/auth/sessions");

      setSessions(response.data);
      setError("");
    } catch (err) {
      const message =
        err.response?.data?.detail || "Could not load sessions";

      // Only show the error if we don't already have sessions
      setSessions((currentSessions) => {
        if (currentSessions.length === 0) {
          setError(message);
        }
        return currentSessions;
      });
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function fetchSessions() {
      try {
        const response = await api.get("/auth/sessions");

        if (!cancelled) {
          setSessions(response.data);
          setError("");
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err.response?.data?.detail ||
              "Could not load sessions"
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchSessions();

    return () => {
      cancelled = true;
    };
  }, []);

  async function logoutOne(sessionId) {
    try {
      await api.delete(
        `/auth/sessions/${encodeURIComponent(sessionId)}`
      );

      // Check whether the deleted session is the current session.
      // If it was, the backend has removed our login session.
      const currentSessionResponse = await api
        .get("/auth/me")
        .catch(() => null);

      if (!currentSessionResponse) {
        window.location.href = "/login";
        return;
      }

      await loadSessions();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Could not logout session"
      );
    }
  }

  async function logoutAll() {
    try {
      await api.post("/auth/logout-all");
      window.location.href = "/login";
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Could not logout all sessions"
      );
    }
  }

  if (loading) {
    return <div className="center">Loading sessions...</div>;
  }

  return (
    <section>
      <div className="section-heading">
        <div>
          <h1>Active Sessions</h1>
          <p className="muted">
            Review and terminate your logged-in sessions.
          </p>
        </div>

        <button className="danger" onClick={logoutAll}>
          Logout All
        </button>
      </div>

      {error && (
        <div className="alert error">
          {error}
        </div>
      )}

      {sessions.length === 0 ? (
        <div className="card">
          No active sessions found.
        </div>
      ) : (
        <div className="session-list">
          {sessions.map((session) => (
            <div
              className="session-card"
              key={session.session_id}
            >
              <div>
                <h3>Device / Browser</h3>

                <p className="device">
                  {session.device || "Unknown device"}
                </p>

                <small>
                  Created:{" "}
                  {session.created_at
                    ? new Date(
                        session.created_at
                      ).toLocaleString()
                    : "—"}
                </small>

                <br />

                <small>
                  Expires:{" "}
                  {session.expires_at
                    ? new Date(
                        session.expires_at
                      ).toLocaleString()
                    : "—"}
                </small>
              </div>

              <button
                className="secondary"
                onClick={() =>
                  logoutOne(session.session_id)
                }
              >
                Logout
              </button>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}