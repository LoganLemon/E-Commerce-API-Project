import { useEffect, useState } from "react";
import api from "../api/apiClient";

export default function Cart() {
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch cart items
  useEffect(() => {
    api
      .get("http://localhost:8000/cart")
      .then((res) => {
        setCart(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching cart:", err);
        setError("Failed to load cart.");
        setLoading(false);
      });
  }, []);

  const checkout = () => {
    api
      .post("http://localhost:8000/orders/checkout")
      .then((res) => {
        if (res.data.checkout_url) {
          window.location.href = res.data.checkout_url; // Redirect to Stripe
        } else {
          alert("Checkout URL not found");
        }
      })
      .catch((err) => {
        console.error(err);
        alert("Error starting checkout");
      });
  };

  if (loading) {
    return <p className="text-center text-gray-400 mt-10">Loading cart...</p>;
  }

  if (error) {
    return <p className="text-center text-red-400 mt-10">{error}</p>;
  }

  const total = cart.reduce(
    (sum, item) => sum + item.product.price * item.quantity,
    0
  );

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 px-8 py-12">
      <h1 className="text-4xl font-bold text-blue-400 text-center mb-10">
        🛒 Your Cart
      </h1>

      {cart.length === 0 ? (
        <p className="text-center text-gray-400">Your cart is empty.</p>
      ) : (
        <div className="max-w-3xl mx-auto space-y-4">
            {cart.map((item) => (
            <div
                key={item.id}
                className="bg-gray-900 rounded-xl p-5 flex justify-between items-center shadow-md"
            >
                <div className="flex items-center space-x-4">
                <img
                    src={`https://picsum.photos/seed/${item.product.id}/100/100`}
                    alt={item.product.name}
                    className="rounded-lg w-20 h-20 object-cover"
                />
                <div>
                    <h2 className="text-lg font-semibold">{item.product.name}</h2>
                    <p className="text-gray-400 text-sm">
                    ${item.product.price.toFixed(2)} × {item.quantity}
                    </p>
                </div>
                </div>

                <div className="flex items-center space-x-4">
                <p className="text-blue-400 font-bold">
                    ${(item.product.price * item.quantity).toFixed(2)}
                </p>
                <button
                onClick={() =>
                    api
                    .delete(`/cart/${item.product.id}`)
                    .then(() => setCart((prev) => prev.filter((i) => i.id !== item.id)))
                    .catch((err) => console.error(err))
                }
                className="text-red-400 hover:text-red-500 transition-colors"
                title="Remove from cart"
                >
                🗑
                </button>
                </div>
            </div>
            ))}

          <div className="flex justify-between items-center border-t border-gray-800 pt-6 mt-6">
            <p className="text-xl font-semibold">Total:</p>
            <p className="text-2xl font-bold text-blue-400">
              ${total.toFixed(2)}
            </p>
          </div>

          <button
            onClick={checkout}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-semibold text-lg transition"
          >
            Proceed to Checkout
          </button>
        </div>
      )}
    </div>
  );
}
