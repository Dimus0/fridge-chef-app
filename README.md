# FridgeChef API

`FridgeChef` is an async FastAPI backend for fridge inventory tracking, recipe management, AI-assisted recipe generation, shopping planning, notifications, and basic operational tooling.

## Features

- JWT auth with profile endpoint
- Fridge inventory CRUD and freshness status
- Recipe CRUD, exact fridge matching, and AI recipe generation
- Shopping list CRUD with toggle flow
- Inventory overview, recipe recommendations, meal-plan suggestions
- Notification digest and audit log groundwork
- Health/readiness endpoints, environment-driven config, Docker, CI, and Alembic migrations

## Local setup

1. Copy `.env.example` to `.env` and fill in secrets.
2. Install dependencies with `uv sync`.
4. Start the API with `uv run python main.py`.

## Main endpoints

- `POST /auth/` register
- `POST /auth/login` login
- `GET /auth/me` current user
- `GET /fridge/status` grouped fridge freshness
- `GET /inventory/overview` inventory analytics
- `GET /recommendations/recipes` ranked recipe coverage
- `GET /shopping-planner/missing-items` missing ingredients by recipe
- `GET /meal-plan/daily` simple meal plan suggestion
- `GET /notifications/` expiring-product notifications
- `GET /health` and `GET /ready`

## Quality workflow

- Lint: `uv run ruff check .`
- Tests: `uv run pytest`
- CI runs lint + tests on pushes and pull requests.

