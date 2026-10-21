# Deployment

## Docker (local)

```bash
OPENAI_API_KEY=your-real-key docker compose up --build
```

`docker-compose.yml` runs two containers:
- `api` — this app, built from the `Dockerfile` (Python 3.12-slim, installs
  `requirements.txt`, runs `uvicorn`). Exposed on host port `8001` (container port 8000).
- `db` — `postgres:16-alpine`, exposed on host port `5540`, with a healthcheck so `api` waits
  for Postgres to actually accept connections before starting.

`DATABASE_URL` is set inside `docker-compose.yml` to point at the `db` service by its Docker
network name (`db:5432`) — this is different from the `DATABASE_URL` in `.env.example`, which is
for running the app directly on the host (`localhost:5432`). `OPENAI_API_KEY` still comes
from your shell environment (or a `.env` file next to `docker-compose.yml`, which Docker Compose
reads automatically) — never hardcoded in the compose file.

## Why Docker, no Kubernetes

This is a single service with a single database — Kubernetes' value (rolling deploys across
many replicas, self-healing across a cluster, service discovery at scale) doesn't apply to one
container. Docker Compose is the right-sized tool here; reaching for Kubernetes on a
single-container portfolio API would be solving a scaling problem that doesn't exist yet.

## Deploying beyond local Docker

The same `Dockerfile` is what a platform like Railway or Render would build for a live deploy —
point either at this repo, set `DATABASE_URL` (their managed Postgres) and `OPENAI_API_KEY`
as environment variables in their dashboard, and they build and run the same image.
