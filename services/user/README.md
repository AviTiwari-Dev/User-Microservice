
# Project run commands

## Set location
Set-Location "D:\Development\Python\project010"

## Build Service
docker build -f .\services\user\Dockerfile --target prod -t user-service:local .

## Run Container
docker run --rm `
  --name user-service `
  -p 8080:8080 `
  --env-file .env `
  user-service:local

## Run complete services
docker compose up -d --build

## Open Swgger UI
http://localhost:8080/documentation/Swagger

## Check Logs
docker compose logs --no-color postgres
docker compose up -d postgres; docker inspect user-postgres --format '{{.State.ExitCode}} {{.State.Status}} {{.State.Error}}'; docker logs --tail 100 user-postgres

## Close services
docker compose down -v; docker compose up -d postgres; docker compose ps
