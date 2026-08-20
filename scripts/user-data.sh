#!/bin/bash
# EC2 Launch Template "User data" script (Amazon Linux 2 AMI)
# Replace YOUR_DOCKERHUB_USERNAME below before pasting this into the launch template.

yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user
systemctl enable docker

DOCKERHUB_USER="YOUR_DOCKERHUB_USERNAME"

# Shared network so the containers can reach each other by name
docker network create app-net

# Backend tier (internal only, not published to the host)
docker run -d --name backend --network app-net --restart unless-stopped \
  "$DOCKERHUB_USER/scalable-backend:latest"

# Web tier (published on port 80, this is what the ALB targets)
docker run -d --name web --network app-net -p 80:5000 --restart unless-stopped \
  -e BACKEND_URL=http://backend:5001 \
  "$DOCKERHUB_USER/scalable-web:latest"
