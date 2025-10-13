
# E-Commerce API (FastAPI) + Vite React Frontend

This repository implements a simple e-commerce backend API using FastAPI and a lightweight Vite + React frontend. It is intended as a starter/demo project and includes routes for users, products, carts and orders, plus a small SQLite database and a seeding script for development.

## Features
- FastAPI backend with SQLAlchemy (SQLite by default)
- JWT authentication
- Stripe integration placeholder (loads key from environment)
- Vite + React frontend (in `frontend/`)
- Seed script to populate demo users and products

## Tech stack
- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- Vite + React

## Repo layout
- `app/` — backend application code (routes, models, auth, DB)
- `frontend/` — React frontend (Vite)
- `requirements.txt` — Python dependencies
- `README.md` — this file

## Quick start — Backend

1. Create and activate a virtual environment

	python3 -m venv .venv
	source .venv/bin/activate

2. Install dependencies

	pip install -r requirements.txt

3. Environment variables

Create a `.env` file in the project root (this repo's `.gitignore` already excludes `.env`). The application expects the following variables for local development:

- `SECRET_KEY` — JWT secret key (required). DO NOT commit this value.
- `ALGORITHM` — JWT signing algorithm (defaults to `HS256` if not set in code).
- `STRIPE_SECRET_KEY` — (optional) Stripe secret for payments.

Example `.env` (do not commit):

	SECRET_KEY=replace-with-a-secure-random-value
	STRIPE_SECRET_KEY=sk_test_...

Note: The current codebase contains a hard-coded default `SECRET_KEY` in `app/auth/jwt_handler.py` (value: `supersecretkey`). This is insecure for production. See Security notes below for remediation steps.

4. Initialize the database

The project uses SQLite by default. Tables will be created automatically on app startup. To seed demo data run:

	python app/seed_db.py

5. Run the API server (development)


	# E-Commerce API (FastAPI) + Vite React Frontend

	This repository provides a small example e-commerce application with a FastAPI backend and a Vite + React frontend. It is intended for local development, learning, and as a starting point for small projects.

	Repository contents
	- `app/` — backend application (routes, models, auth, database)
	- `frontend/` — Vite + React frontend
	- `requirements.txt` — Python dependencies
	- `.env.example` — example environment variables (no secret values)

	Requirements
	- Python 3.10+
	- Node 18+ (or compatible) for the frontend

	Backend — Quick start (local development)

	1. Create and activate a virtual environment

	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```

	2. Install dependencies

	```bash
	pip install -r requirements.txt
	```

	3. Copy `.env.example` to `.env` and edit values (do not commit `.env`)

	```bash
	cp .env.example .env
	# edit .env and set SECRET_KEY and any optional vars
	```

	Required environment variables (development)
	- `SECRET_KEY` — a secure random string used to sign JWTs. Do NOT commit this value.
	- `ALGORITHM` — signing algorithm (default: HS256)
	- `ACCESS_TOKEN_EXPIRE_MINUTES` — token expiry in minutes (default: 30)
	- `STRIPE_SECRET_KEY` — optional Stripe secret key for payments (use test keys in dev)

	4. Initialize the database and seed demo data (SQLite is used by default)

	```bash
	python app/seed_db.py
	```

	5. Run the development server

	```bash
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
	```

	The automatic API docs are available at `http://127.0.0.1:8000/docs`.

	Frontend — Quick start

	```bash
	cd frontend
	npm install
	npm run dev
	```

	Open the frontend (typically `http://localhost:5173`) and ensure the backend is running.

	Testing

	Run backend tests from the repository root:

	```bash
	pytest
	```

	Security and push-readiness

	- Environment-driven secrets: The backend reads `SECRET_KEY`, `ALGORITHM`, and `ACCESS_TOKEN_EXPIRE_MINUTES` from environment variables. For production, set `SECRET_KEY` to a secure, randomly generated string and keep it secret.
	- `.env` files are excluded by `.gitignore`. Never commit real secret values.
	- The seed script contains demo passwords for local testing only. Replace them in production.
	- If a secret is accidentally committed to a public repository, rotate the credential immediately and remove it from history (see `git filter-repo` or BFG documentation).

	Preparing to push

	1. Ensure `.env` is in `.gitignore` and you have no secrets staged.

	2. Commit and push with a clear message:

	```bash
	git add .
	git commit -m "Prepare project for public use: environment-driven secrets and docs"
	git push origin main
	```

	If you need to remove sensitive data from history, rotate credentials first and then use a history-rewriting tool.

	Recommended improvements

	- Add CI workflows to run tests and a secrets scanner.
	- Add `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` for community projects.
	- Consider a secret manager for production deployments (Vault, AWS Secrets Manager, etc.).

	License

	This repository does not include an OSS license file. Add an appropriate license if you intend to publish the project.

	Thank you for using this project. Contributions and issues are welcome.
