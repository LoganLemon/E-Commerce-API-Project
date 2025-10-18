# E-Commerce API

A full-stack e-commerce solution built with FastAPI and React, featuring user authentication, product management, shopping cart functionality, and payment processing.

## Architecture

- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: React with Vite
- **Authentication**: JWT-based with secure token handling
- **Payments**: Stripe integration

## Features

### Core Functionality
- User registration and authentication
- Product catalog with search and filtering
- Shopping cart management
- Order processing and tracking
- Payment processing via Stripe
- Admin dashboard for product management

### Technical Features
- RESTful API design
- Database migrations and seeding
- Environment-based configuration
- Comprehensive error handling
- API documentation with Swagger/OpenAPI
- CORS support for frontend integration
- **Comprehensive test suite** with 86+ tests
- **CI/CD pipeline** with GitHub Actions
- **Test coverage** for all endpoints and functionality

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Backend Setup

1. **Clone and setup environment**
   ```bash
   git clone <repository-url>
   cd E-Commerce-API-Project
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database**
   ```bash
   python app/seed_db.py
   ```

5. **Start development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

## Testing

### Running Tests

The project includes a comprehensive test suite with **86+ tests** covering all functionality:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_auth.py -v
python -m pytest tests/test_products.py -v
python -m pytest tests/test_cart.py -v
python -m pytest tests/test_orders.py -v
python -m pytest tests/test_admin.py -v
python -m pytest tests/test_users.py -v

# Run tests with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Quick test run
python -m pytest tests/ -q
```

### Test Coverage

- **Authentication**: User registration, login, JWT validation
- **Products**: CRUD operations, authorization, validation
- **Shopping Cart**: Add/remove items, quantity updates, isolation
- **Orders**: Checkout process, Stripe integration, stock validation
- **Admin**: Product management, authorization, data validation
- **Users**: Profile management, security, edge cases

### CI/CD

Tests run automatically on every push and pull request via GitHub Actions:
- **Automated testing** on all branches
- **Prevents broken code** from merging
- **Fast feedback** for developers
- **Professional development workflow**

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | JWT signing key | Yes | - |
| `ALGORITHM` | JWT algorithm | No | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | No | 30 |
| `STRIPE_SECRET_KEY` | Stripe API key | No | - |
| `DATABASE_URL` | Database connection | No | sqlite:///./app.db |

### API Documentation

Once the backend is running, interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh` - Token refresh

### Products
- `GET /products/` - List products
- `GET /products/{id}` - Get product details
- `POST /products/` - Create product (admin)
- `PUT /products/{id}` - Update product (admin)
- `DELETE /products/{id}` - Delete product (admin)

### Cart & Orders
- `GET /cart/` - Get user cart
- `POST /cart/add` - Add item to cart
- `DELETE /cart/{product_id}` - Remove cart item
- `POST /orders/checkout` - Create order
- `GET /orders/success` - Payment success
- `GET /orders/cancel` - Payment cancel

### Admin
- `GET /admin/products` - List all products (admin)
- `POST /admin/products` - Create product (admin)
- `PUT /admin/products/{id}` - Update product (admin)
- `DELETE /admin/products/{id}` - Delete product (admin)

## Development

### Project Structure
```
├── app/                    # FastAPI application
│   ├── auth/              # Authentication logic
│   ├── routes/             # API endpoints
│   ├── models.py          # Database models
│   ├── schemas.py          # Pydantic schemas
│   └── database.py         # Database configuration
├── tests/                  # Test suite (86+ tests)
├── frontend/               # React application
├── .github/workflows/      # CI/CD pipeline
└── requirements.txt        # Python dependencies
```

### Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Run tests**: `python -m pytest tests/ -v`
4. **Commit changes**: `git commit -m 'Add amazing feature'`
5. **Push to branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

## License

This project is licensed under the MIT License - see the LICENSE file for details.
