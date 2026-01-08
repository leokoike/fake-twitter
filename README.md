# Fake Twitter API

A Twitter-like API built with FastAPI following Domain-Driven Design (DDD) architecture.

## Features

- User management (create, read, update, delete)
- Tweet management (create, read, update, delete)
- User follow/unfollow functionality
- Tweet like/unlike functionality
- Retweet functionality
- Async PostgreSQL database with SQLAlchemy
- RESTful API with FastAPI
- Docker support for easy deployment

## Project Structure

```
fake-twitter/
├── src/
│   └── fake_twitter/
│       ├── domain/              # Domain layer (entities, repositories)
│       │   ├── entities/
│       │   └── repositories/
│       ├── application/         # Application layer (use cases, DTOs)
│       │   ├── dtos/
│       │   └── use_cases/
│       └── infrastructure/      # Infrastructure layer (database, implementations)
│           ├── database/
│           ├── repositories/
│           └── api/
│               └── v1/
│                   └── routes/
├── Dockerfile
├── docker-compose.yml
├── gunicorn.conf.py
└── pyproject.toml
```

## Installation

### Local Installation

1. Install dependencies using uv:
```bash
uv sync
```

2. Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fake_twitter
```

### Docker Installation

Build the Docker image:
```bash
docker build -t fake-twitter:latest .
```

Or use Docker Compose (includes PostgreSQL):
```bash
docker-compose up -d
```

## Running the API

### With Docker Compose (Recommended)

```bash
docker-compose up -d
```

This will start both the API and PostgreSQL database. The API will be available at http://localhost:8000

To stop:
```bash
docker-compose down
```

To view logs:
```bash
docker-compose logs -f api
```

### With Docker Only

```bash
docker run -d \
  --name fake-twitter-api \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://postgres:postgres@host.docker.internal:5432/fake_twitter \
  fake-twitter:latest
```

### With Gunicorn (Production)

```bash
uv run gunicorn fake_twitter.main:app -c gunicorn.conf.py
```

### With Uvicorn (Development)

```bash
uv run uvicorn fake_twitter.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## API Endpoints

### Users

- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users/username/{username}` - Get user by username
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user
- `POST /api/v1/users/{user_id}/follow` - Follow user
- `POST /api/v1/users/{user_id}/unfollow` - Unfollow user

### Tweets

- `POST /api/v1/tweets/` - Create a new tweet
- `GET /api/v1/tweets/` - Get all tweets
- `GET /api/v1/tweets/{tweet_id}` - Get tweet by ID
- `GET /api/v1/tweets/user/{user_id}` - Get tweets by user
- `PUT /api/v1/tweets/{tweet_id}` - Update tweet
- `DELETE /api/v1/tweets/{tweet_id}` - Delete tweet
- `POST /api/v1/tweets/{tweet_id}/like` - Like tweet
- `POST /api/v1/tweets/{tweet_id}/unlike` - Unlike tweet
- `POST /api/v1/tweets/{tweet_id}/retweet` - Retweet

## Database Setup

### With Docker Compose

Migrations will need to be run manually:
```bash
docker-compose exec api uv run alembic upgrade head
```

### Local Setup

Run Alembic migrations to set up the database:
```bash
alembic upgrade head
```

## Architecture

This project follows **Domain-Driven Design (DDD)** principles:

- **Domain Layer**: Contains business entities and repository interfaces
- **Application Layer**: Contains use cases and DTOs for business logic
- **Infrastructure Layer**: Contains database models, repository implementations, FastAPI routes and HTTP handling

## Technologies

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation using Python type hints
- **Gunicorn**: WSGI HTTP server for production
- **Uvicorn**: ASGI server for async Python
- **Alembic**: Database migration tool
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container Docker applications

## Docker Commands

Build image:
```bash
docker build -t fake-twitter:latest .
```

Run container:
```bash
docker run -p 8000:8000 fake-twitter:latest
```

Start with docker-compose:
```bash
docker-compose up -d
```

Stop with docker-compose:
```bash
docker-compose down
```

View logs:
```bash
docker-compose logs -f
```

Rebuild and restart:
```bash
docker-compose up -d --build
```
