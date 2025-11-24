# Database practice

## What's Included

- Dockerized PostgreSQL
- SQLAlchemy ORM with a shared Base
- Alembic migrations
- Basic project structure and database schema doc

## Requirements

- Python 3.10+
- Docker Desktop
- Git

### 1. Clone the repository
```bash
git clone <repo-url>
cd <project-folder>
```

### 2. Configure environment
```bash
cp .env.example .env

DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/mydatabase
```

### 3. Start Database
```bash
#launch containfer
docker-compose up -d

#verify if running
docker ps
```

### 4. Run Migrations
```bash
#apply migrations
alembic upgrade head

#create new
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Project Structure (haven't merged with actual repo or anything yet)
```bash
├── database/          # Database engine, session, and Base
├── models/            # SQLAlchemy models
├── schemas/           # Pydantic schemas
├── routes/            # FastAPI endpoints
├── alembic/           # Database migration scripts
└── docs/
    └── schema.md      # Database schema documentation
```