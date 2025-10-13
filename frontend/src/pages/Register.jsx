import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await axios.post("http://localhost:8000/users/register", {
        username: name,
        email,
        password
      });

      alert("Account created! Please log in.");
      navigate("/login");
    } catch (err) {
      console.error(err);
      setError("Registration failed");
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center text-gray-100 px-4">
      <form
        onSubmit={handleRegister}
        className="bg-gray-900 rounded-xl shadow-lg p-8 w-full max-w-sm"
      >
        <h1 className="text-3xl font-bold text-blue-400 text-center mb-6">
          Register
        </h1>

        {error && (
          <p className="text-red-400 text-center text-sm mb-4">{error}</p>
        )}

        <label className="block mb-2 text-sm font-medium">Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="w-full px-3 py-2 mb-4 rounded bg-gray-800 border border-gray-700 focus:outline-none focus:border-blue-500"
        />

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
          Create Account
        </button>
      </form>
    </div>
  );
}
