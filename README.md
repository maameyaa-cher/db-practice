# slab-backend

Structured FastAPI backend, containerized with Docker.



## Project Structure

```
.
├── app/                # Main application source code
│   ├── api/            # API specific modules
│   │   └── v1/         # API version 1
│   │       ├── endpoints/  # API endpoint files (routes)
│   │       │   ├── health.py
│   │       │   └── items.py #example
│   │       └── api.py      # V1 API router aggregator
│   ├── core/           # Core application logic (e.g., config)
│   │   └── config.py
│   ├── db/             # Database related modules (currently empty)
│   ├── models/         # Pydantic models (data schemas)
│   │   └── item.py
│   └── services/       # Business logic (service layer)
│       └── item_service.py
├── tests/              # Application tests (currently empty)
├── .dockerignore       # Files to ignore in Docker build
├── .env                # Local environment variables (DO NOT COMMIT)
├── .env.example        # Example environment variables
├── .gitignore          # Files to ignore in Git
├── docker-compose.yml  # Docker Compose configuration
├── Dockerfile          # Docker build instructions
├── main.py             # Main application entrypoint
└── requirements.txt    # Python dependencies
```

---

## Running with Docker

This project uses a multi-file Docker Compose setup to separate development and production environments.

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Initial Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/guptasaransh76/slab-backend.git
    cd slab-backend
    ```

2.  **Configure Your Environment**
    Copy the example environment file. This is used for all Docker environments.
    ```bash
    cp .env.example .env
    ```

### 2. Running in Development

For development, `docker-compose` automatically merges the base `docker-compose.yml` with `docker-compose.override.yml` to create a development environment with live-reloading.

```bash
docker-compose up --build
```

Your code is mounted as a volume, and the server will restart automatically when you make changes.

### 3. Running in Production

For production, you must explicitly specify the production configuration file. This runs the application using a production-grade `gunicorn` server and does not mount the source code.

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```
- `-f`: Specifies which compose files to use.
- `-d`: Runs the containers in detached mode (in the background).

### 4. Accessing the API

Once the container is running, the application will be available at `http://127.0.0.1:8000`.

- **API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check**: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)
- **Items Endpoint** (example): [http://127.0.0.1:8000/api/v1/items](http://127.0.0.1:8000/api/v1/items)

---

## Manual Setup (Alternative)

If you prefer not to use Docker, you can run the application locally.

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```