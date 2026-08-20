# Scalable Container Architecture

A multi-tier Dockerized application deployed on AWS with an Application Load
Balancer, Auto Scaling Group, and CloudWatch monitoring, with a CI/CD
pipeline in GitHub Actions that builds and pushes new images on every push.

> This README will be finished once the AWS deployment is live and tested —
> the sections below are placeholders for real numbers, not made-up stats.

## Architecture

- **Web tier** (`web/`) — Flask app, serves requests, calls the backend tier.
- **Backend tier** (`backend/`) — Flask app, internal-only service on the
  Docker network.
- **CI/CD** — GitHub Actions builds both images on push to `main` and pushes
  them to Docker Hub.
- **Compute** — EC2 instances in an Auto Scaling Group (min 2 / max 4),
  provisioned via a Launch Template whose user data pulls and runs the
  latest images.
- **Load balancing** — an Application Load Balancer distributes traffic
  across instances and health-checks `/health` on the web tier.
- **Monitoring** — CloudWatch alarms on CPU utilization drive scale-out /
  scale-in policies.

## Scope

TODO after deployment: 2-3 sentences on what this project covers and
deliberately does not cover (e.g. no custom VPC/subnetting yet, no HTTPS/
custom domain, no database tier).

## Requirements

TODO after deployment: bullet list of what was needed to run this
(AWS Free Tier account, Docker Hub account, GitHub repo with Actions
enabled, IAM permissions used, etc).

## Results / efficiency

TODO after testing — record real, measured numbers, not estimates:
- Response time before/after ALB + Auto Scaling (measure with `curl -w`
  or a simple load test)
- What happened when an instance was manually terminated (recovery time)
- Any CPU-based scaling event observed during a load test

## Local development

```bash
docker compose up --build
curl http://localhost/
curl http://localhost/health
```

## Deployment

See `scripts/user-data.sh` for the EC2 Launch Template user data. Full
setup steps for the ALB, ASG, and CloudWatch alarms are documented
separately during setup.
