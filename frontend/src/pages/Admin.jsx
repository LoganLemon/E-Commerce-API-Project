import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../api/apiClient";

export default function Admin() {
  const { user } = useAuth(); // get current user from context
  const navigate = useNavigate();

  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ name: "", description: "", price: "", quantity: "" });
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState("");

  // Redirect logic: unauthenticated → login; non-admin → home
  useEffect(() => {
    if (!user) {
      navigate("/login");
    } else if (!user.is_admin) {
      navigate("/");
    }
  }, [user, navigate]);

  // Load products if user is admin
  useEffect(() => {
    if (user?.is_admin) {
      api.get("/admin/products")
        .then(res => setProducts(res.data))
        .catch(() => setError("Failed to fetch products (admins only)"));
    }
  }, [user]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = { ...form, price: parseFloat(form.price), quantity: parseInt(form.quantity) };

    const req = editingId
      ? api.put(`/admin/products/${editingId}`, payload)
      : api.post("/admin/products", payload);

    req
      .then(res => {
        if (editingId) {
          setProducts(products.map(p => (p.id === editingId ? res.data : p)));
        } else {
          setProducts([...products, res.data]);
        }
        setForm({ name: "", description: "", price: "", quantity: "" });
        setEditingId(null);
      })
      .catch(err => {
        console.error(err);
        setError("Action failed. Make sure you are logged in as admin.");
      });
  };

  const handleEdit = (product) => {
    setEditingId(product.id);
    setForm({
      name: product.name,
      description: product.description,
      price: product.price,
      quantity: product.quantity,
    });
  };

  const handleDelete = (id) => {
    if (!window.confirm("Delete this product?")) return;
    api.delete(`/admin/products/${id}`)
      .then(() => setProducts(products.filter(p => p.id !== id)))
      .catch(() => setError("Delete failed."));
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 px-8 py-12">
      <h1 className="text-4xl font-bold text-blue-400 mb-8 text-center">
        Admin Dashboard
      </h1>

      {error && <p className="text-center text-red-400 mb-6">{error}</p>}

      <form
        onSubmit={handleSubmit}
        className="bg-gray-900 p-6 rounded-xl max-w-2xl mx-auto mb-10 shadow-lg space-y-4"
      >
        <h2 className="text-2xl font-semibold text-blue-300 mb-2">
          {editingId ? "Edit Product" : "Add New Product"}
        </h2>
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Name"
          required
          className="w-full p-2 rounded bg-gray-800 border border-gray-700 focus:border-blue-500"
        />
        <textarea
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Description"
          required
          className="w-full p-2 rounded bg-gray-800 border border-gray-700 focus:border-blue-500"
        />
        <div className="flex space-x-4">
          <input
            name="price"
            type="number"
            step="0.01"
            value={form.price}
            onChange={handleChange}
            placeholder="Price"
            required
            className="w-1/2 p-2 rounded bg-gray-800 border border-gray-700 focus:border-blue-500"
          />
          <input
            name="quantity"
            type="number"
            value={form.quantity}
            onChange={handleChange}
            placeholder="Quantity"
            required
            className="w-1/2 p-2 rounded bg-gray-800 border border-gray-700 focus:border-blue-500"
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition"
        >
          {editingId ? "Update Product" : "Add Product"}
        </button>
      </form>

      <div className="max-w-4xl mx-auto">
        {products.length === 0 ? (
          <p className="text-center text-gray-400">No products found.</p>
        ) : (
          <div className="space-y-4">
            {products.map((p) => (
              <div
                key={p.id}
                className="bg-gray-900 p-4 rounded-xl flex justify-between items-center shadow-md"
              >
                <div>
                  <h3 className="text-xl font-semibold text-blue-300">{p.name}</h3>
                  <p className="text-gray-400 text-sm">{p.description}</p>
                  <p className="text-gray-300 text-sm mt-1">
                    ${p.price.toFixed(2)} • Qty: {p.quantity}
                  </p>
                </div>
                <div className="flex space-x-3">
                  <button
                    onClick={() => handleEdit(p)}
                    className="text-yellow-400 hover:text-yellow-500 transition-colors"
                  >
                    ✏️
                  </button>
                  <button
                    onClick={() => handleDelete(p.id)}
                    className="text-red-400 hover:text-red-500 transition-colors"
                  >
                    🗑
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
