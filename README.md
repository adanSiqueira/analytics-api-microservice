<div align="center"><h1>analytics-api-microsservice</h1></div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.132.0-009688?logo=fastapi\&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.x-E92063?logo=pydantic\&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-0.0.37-4B8BBE)
![TimescaleDB](https://img.shields.io/badge/TimescaleDB-Time--Series-CC2927)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker\&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-25.1.0-499848)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.41.0-222222)

</div>

---

## Overview

**analytics-api-microsservice** is a production-ready **FastAPI-based time-series analytics microservice** designed to:

* Ingest structured web traffic events
* Persist them in a TimescaleDB hypertable
* Expose aggregated analytical insights via HTTP endpoints

The service is containerized with Docker and architected for:

* Scalability
* Clean routing separation
* Database abstraction
* Time-series performance optimization

---

## 🏗 Project Structure

```
.
├── compose.yaml
├── Dockerfile
├── requirements.txt
├── notebooks/
│   └── notebook.ipynb
└── src/
    ├── main.py
    └── api/
        ├── db/
        │   ├── config.py
        │   └── session.py
        └── events/
            ├── __init__.py
            ├── models.py
            └── routing.py
```

### Structure Breakdown

* **compose.yaml** → Development orchestration with Docker Compose
* **Dockerfile** → Production-ready container image
* **notebooks/** → Query prototyping & aggregation experiments
* **src/main.py** → FastAPI application entry point + lifespan management
* **src/api/db/** → Database configuration & session management
* **src/api/events/models.py** → TimescaleDB hypertable models
* **src/api/events/routing.py** → Event ingestion & aggregation endpoints

---

## Tech Stack

* **FastAPI** — High-performance ASGI framework
* **Pydantic v2** — Data validation & serialization
* **SQLModel / SQLAlchemy 2.0** — ORM layer
* **TimescaleDB** — Time-series optimized PostgreSQL extension
* **Gunicorn + Uvicorn** — Production ASGI server stack
* **Docker & Docker Compose** — Containerized deployment

---

## Architecture Overview

```
Client (Frontend / Backend)
        │
        ▼
POST /api/events/     →  Event Ingestion
        │
        ▼
TimescaleDB Hypertable
        │
        ▼
GET /api/events/      →  Aggregated Analytics
```

### Design Principles

* Event-driven ingestion
* Time-bucket aggregation
* Retention policy enforcement
* Service-level database abstraction
* Microservice-ready structure

---

## ⚙️ Development Setup

### 1️⃣ Build & Run with Docker Compose

```bash
docker compose up --build
```

API will be available at:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

---

### 2️⃣ Local Python Development (Optional)

Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run with Uvicorn:

```bash
uvicorn src.main:app --reload
```

---

## Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql://user:password@db:5432/analytics
DB_TIMEZONE=UTC
```

If `DATABASE_URL` is not set, the application will fail to start.

---

## Database Design

### Event Model (Hypertable)

The `EventModel` extends `TimescaleModel`, enabling:

* Automatic hypertable creation
* Daily chunk partitioning
* Automatic retention

```python
__chunk_time_interval__ = "INTERVAL 1 day"
__drop_after__ = "INTERVAL 3 months"
```

### Stored Fields

* `page`
* `user_agent`
* `ip_address`
* `referrer`
* `session_id`
* `duration`
* `created_at` (inherited from TimescaleModel)

---

## API Design

The API follows a modular architecture:

```
src/
 └── api/
      └── events/
           ├── models.py
           └── routing.py
```

### Endpoints

---

### 🔹 POST `/api/events/`

Ingests a web traffic event.

#### Example Request

```json
{
  "page": "/pricing",
  "user_agent": "Mozilla/5.0",
  "ip_address": "192.168.0.1",
  "referrer": "google.com",
  "session_id": "abc123",
  "duration": 12
}
```

---

### 🔹 GET `/api/events/`

Returns aggregated analytics grouped by:

* Time bucket (default: 1 day)
* Page
* Operating system (derived from user agent)

#### Query Parameters

| Parameter | Type | Description          |
| --------- | ---- | -------------------- |
| duration  | str  | Time bucket interval |
| pages     | list | Pages to filter      |

#### Example

```
GET /api/events/?pages=/pricing&pages=/about
```

#### Example Response

```json
[
  {
    "bucket": "2026-03-03T00:00:00",
    "page": "/pricing",
    "count": 254
  }
]
```

---

### 🔹 GET `/api/events/{event_id}`

Returns raw stored event.

---

### 🔹 GET `/health`

Health check endpoint:

```json
{
  "status": "ok"
}
```

---

## Aggregation Strategy

The service uses TimescaleDB's `time_bucket` function for efficient grouping:

* Daily aggregation by default
* Grouped by page and OS
* Average session duration
* Event count

This allows scalable analytics even with millions of events.

---

## Why Use an Analytics Microservice?

Using an analytics microservice instead of allowing multiple services to query the database directly provides several architectural advantages. It enforces a clear separation of concerns by isolating analytics logic from the main application’s business logic, ensuring each service has a well-defined responsibility. It improves security by preventing external services from accessing the database directly, centralizing and controlling data access through a dedicated API layer. It also consolidates aggregation rules—such as time bucketing and grouping—into a single location, avoiding duplication and inconsistency across the system. Finally, it enhances scalability, since the analytics workload can scale independently from the core application, allowing each component to grow according to its own performance demands.


### Ready for:

* Kafka ingestion pipeline
* Async event processing
* Redis caching layer
* Materialized views
* Read replicas

---

## Production Considerations

* Gunicorn worker tuning
* Connection pooling
* Reverse proxy support (NGINX / Traefik)
* Horizontal scaling support
* Read replicas for heavy aggregation workloads
* Rate limiting for analytics endpoints
* Monitoring & metrics integration

---

## Working on Features

* [x] Database integration (TimescaleDB)
* [x] Event ingestion pipeline
* [x] Analytics aggregation endpoints
* [ ] Authentication & Authorization
* [ ] Observability (structured logging + metrics)
* [ ] Rate limiting
* [ ] CI/CD integration
* [ ] OpenAPI versioning strategy
* [ ] Caching layer (Redis)

---
