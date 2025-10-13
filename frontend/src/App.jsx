import { useEffect, useState } from "react";
import { useAuth } from "./context/AuthContext";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from "react-router-dom";
import Home from "./pages/Home";
import Cart from "./pages/Cart";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Admin from "./pages/Admin"

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-gray-900 text-white px-6 py-4 shadow-md flex justify-between items-center sticky top-0 z-50">
      <div
        className="text-2xl font-bold text-blue-400 cursor-pointer"
        onClick={() => navigate("/")}
      >
        E-Commerce
      </div>

      <div className="flex space-x-6">
        <Link to="/" className="hover:text-blue-400 transition-colors">
          Home
        </Link>
        <Link to="/cart" className="hover:text-blue-400 transition-colors">
          Cart
        </Link>

        {user?.is_admin && (
          <Link to="/admin" className="hover:text-blue-400 transition-colors">
            Admin
          </Link>
        )}

        {!user ? (
          <>
            <Link to="/login" className="hover:text-blue-400 transition-colors">
              Login
            </Link>
            <Link
              to="/register"
              className="hover:text-blue-400 transition-colors"
            >
              Register
            </Link>
          </>
        ) : (
          <button
            onClick={handleLogout}
            className="text-red-400 hover:text-red-500 transition-colors"
          >
            Logout
          </button>
        )}
      </div>
    </nav>
  );
}


export default function App() {
  return (
    <Router>
      <Navbar />
      <div className="min-h-screen bg-gray-950 text-gray-100">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </div>
    </Router>
  );
}
