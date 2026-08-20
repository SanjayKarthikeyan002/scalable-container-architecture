# Scalable Container Architecture

A multi-tier Dockerized application with a Flask web service and a separate
Flask backend service, communicating over an isolated Docker network, with
a CI/CD pipeline in GitHub Actions that automatically builds and pushes new
container images on every push to `main`.

## Architecture

- **Web tier** (`web/`) — Flask app that serves requests and calls the
  backend tier over the internal Docker network.
- **Backend tier** (`backend/`) — Flask app exposing a health endpoint and a
  small data endpoint, not directly reachable from outside the network.
- **Local orchestration** — `docker-compose.yml` builds and runs both
  services together, wiring them onto a shared network by service name.
- **CI/CD** — `.github/workflows/deploy.yml` builds both Docker images on
  every push to `main` and pushes them to Docker Hub, authenticated via
  GitHub Actions secrets.

## Scope

This project focuses on the application and pipeline layer: a working
multi-tier containerized app, clean service-to-service networking, and an
automated build/push pipeline. It includes deployment scripts
(`scripts/user-data.sh`) written for an AWS EC2 + Auto Scaling Group +
Application Load Balancer setup, intended as a reference for how this would
be deployed and scaled in production — those AWS resources are not
currently running.

## Requirements

- Docker and Docker Compose
- A Docker Hub account (for the CI/CD pipeline to push images to)
- GitHub Actions enabled on the repo, with `DOCKERHUB_USERNAME` and
  `DOCKERHUB_TOKEN` set as repository secrets

## What's been tested

- Both services build and run together locally via `docker compose up --build`,
  with the web tier successfully reaching the backend tier's `/health`
  endpoint over the Docker network.
- The GitHub Actions pipeline builds and pushes both images on every push to
  `main`, completing in under 30 seconds.

## Local development

```bash
docker compose up --build
curl http://localhost/
curl http://localhost/health
```

## Deployment (reference)

`scripts/user-data.sh` shows the EC2 Launch Template user data used to pull
and run these images with Docker on an Amazon Linux 2 instance, as part of
a design that also includes an Application Load Balancer and Auto Scaling
Group for horizontal scaling and CloudWatch-based scaling policies.