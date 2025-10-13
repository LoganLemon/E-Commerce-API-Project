import { useEffect, useState } from "react";
import api from "../api/apiClient"

export default function Home() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    api
      .get("http://localhost:8000/products")
      .then((res) => setProducts(res.data))
      .catch((err) => console.error("Error fetching products:", err));
  }, []);

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 px-8 py-12">
      <h1 className="text-4xl font-bold text-blue-400 text-center mb-10">
        🛍️  Products
      </h1>

      {products.length === 0 ? (
        <p className="text-center text-gray-400">No products available.</p>
      ) : (
        <div className="grid gap-8 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {products.map((p) => (
            <div
              key={p.id}
              className="bg-gray-900 rounded-2xl p-6 shadow-md hover:shadow-blue-600/30 hover:-translate-y-1 transition-all duration-300"
            >
              <img
                src={`https://picsum.photos/seed/${p.id}/400/250`}
                alt={p.name}
                className="rounded-lg mb-4 w-full h-48 object-cover"
              />
              <h2 className="text-xl font-semibold mb-2">{p.name}</h2>
              <p className="text-gray-400 text-sm mb-4 line-clamp-3">
                {p.description}
              </p>
              <p className="text-lg font-bold text-blue-400 mb-4">
                ${p.price.toFixed(2)}
              </p>
              <button
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition-colors"
                onClick={() =>
                  api
                    .post("http://localhost:8000/cart/add", {
                      product_id: p.id,
                      quantity: 1,
                    })
                    .then(() => alert(`${p.name} added to cart!`))
                    .catch((err) => console.error(err))
                }
              >
                Add to Cart
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
