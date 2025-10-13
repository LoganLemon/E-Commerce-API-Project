import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login, user } = useAuth(); // ✅ Safe hook usage inside component
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // ✅ Redirect if already logged in
  useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, [user, navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await axios.post("http://localhost:8000/users/login", {
        email,
        password,
      });

      const token = res.data.access_token;

      // Fetch user profile
      const me = await axios.get("http://localhost:8000/users/me", {
        headers: { Authorization: `Bearer ${token}` },
      });

      // ✅ Update context and localStorage
      login(me.data, token);

      alert("Login successful!");
      navigate("/");
    } catch (err) {
      console.error(err);
      setError("Invalid email or password");
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center text-gray-100 px-4">
      <form
        onSubmit={handleLogin}
        className="bg-gray-900 rounded-xl shadow-lg p-8 w-full max-w-sm"
      >
        <h1 className="text-3xl font-bold text-blue-400 text-center mb-6">
          Login
        </h1>

        {error && (
          <p className="text-red-400 text-center text-sm mb-4">{error}</p>
        )}

        <label className="block mb-2 text-sm font-medium">Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-3 py-2 mb-4 rounded bg-gray-800 border border-gray-700 focus:outline-none focus:border-blue-500"
        />

        <label className="block mb-2 text-sm font-medium">Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full px-3 py-2 mb-6 rounded bg-gray-800 border border-gray-700 focus:outline-none focus:border-blue-500"
        />

        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition-colors"
        >
          Sign In
        </button>

        <p className="text-center text-sm text-gray-400 mt-4">
          Don’t have an account?{" "}
          <a
            href="/register"
            className="text-blue-400 hover:text-blue-500 underline"
          >
            Register
          </a>
        </p>
      </form>
    </div>
  );
}
