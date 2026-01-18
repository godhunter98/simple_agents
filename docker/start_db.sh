#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# check if docker is installed
echo ""
echo "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
  echo "Docker not found! Installing..."
  brew install --cask docker
  echo "Successfully installed Docker"
  sleep 5
else
  echo "Docker is already installed." 
fi; 



# check if docker is running
echo "🔍 Checking Docker daemon..."
if ! docker info &> /dev/null; then
  echo "🚀 Starting Docker Desktop..."
  open -a Docker

  echo "⏳ Waiting for Docker to be ready..."
  until docker info &> /dev/null; do
    sleep 2
  done
else
  echo "Docker daemon is running." 
fi; 

echo ""

docker ps

echo ""
# check if volume exists
echo "Checking if a volume exists for our db..."
if ! docker volume inspect agents_db_agents_db &> /dev/null; then
  echo "Volume agents_db_agents_db does not exist!"
  exit 1
else
  echo "Volume already exists."
fi; 

# finally start the db
echo ""
echo ""
echo "🐘 Starting Postgres via Docker Compose..."
docker compose up -d

echo "✅ Postgres is running."