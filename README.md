# E-Commerce API

A full-stack e-commerce solution built with FastAPI and React, featuring user authentication, product management, shopping cart functionality, and payment processing.

## Architecture

- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: React with Vite
- **Authentication**: JWT-based with secure token handling
- **Payments**: Stripe integration
- **Testing**: Comprehensive test suite with pytest

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
- `PUT /cart/update` - Update cart item
- `DELETE /cart/remove` - Remove cart item
- `POST /orders/` - Create order
- `GET /orders/` - List user orders

## License

This project is licensed under the MIT License - see the LICENSE file for details.
