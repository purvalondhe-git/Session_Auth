import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  return (
    <header className="navbar">
      <Link className="brand" to={user ? "/dashboard" : "/login"}>
        FocusFlow
      </Link>

      <nav>
        {user ? (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/sessions">Sessions</Link>
            {user.role === "admin" && <Link to="/admin">Admin</Link>}
            <button className="nav-button" onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </nav>
    </header>
  );
}