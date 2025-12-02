# Database practice

## What's Included

- Dockerized PostgreSQL
- SQLAlchemy ORM 
- Alembic migrations
- Core project structure for database models and migrations

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
#launch containter
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
app/
  core/               # Engine, session, Base, get_db
  models/             # SQLAlchemy models
  repositories/       # Data access layer
  api/                # Endpoint files (empty for now)
alembic/              # Migration environment and versions
docs/
  schema.md           # Database schema
.env.example
docker-compose.yml
alembic.ini
readme.md
```