# Unmanic auto pause
Pause unmanic while plex has active streams

## Running in Docker

### Docker run
```
docker run -d \
    -e PLEX_URL=<Local Plex URL> \
    -e PLEX_TOKEN=<Your Plex Token> \
    -e UNMANIC_URL=<Local Unmanic URL> \
    -e CHECK_INTERVAL=<Interval between checks in seconds, default 30> \
    --name unmanic-autopause \
    ghcr.io/diamkil/unmanic-autopause:main
```

### Docker-Compose
```
services:
  unmanic-autopause:
    image: ghcr.io/diamkil/unmanic-autopause:main
    container_name: unmanic-autopause
    environment:
      - PLEX_URL=<Local Plex URL>
      - PLEX_TOKEN=<Your Plex Token>
      - UNMANIC_URL=<Local Unmanic URL>
      - CHECK_INTERVAL=<Interval between checks in seconds, default 30>
```
