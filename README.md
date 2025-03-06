# Tic-Tac-Toe Distributed System

This project is a distributed microservices-based Tic-Tac-Toe game built using FastAPI and Flask. The game is played by two AI-based services that take turns making moves, while a main service manages the game flow and a frontend service provides a user interface.

## Architecture

The system consists of four services:

1. **Service 1 (Game Manager - FastAPI)**

   - Controls the game loop.
   - Sends the Tic-Tac-Toe board to player services.
   - Determines the winner and handles retries in case of failures.

2. **Service 2 (Player X - FastAPI)**

   - Plays as `X`.
   - Chooses moves based on random strategy or the first available position.

3. **Service 3 (Player O - FastAPI)**

   - Plays as `O`.
   - Chooses moves based on random strategy or the first available position.

4. **Service 4 (Frontend - Flask)**
   - Displays the game board in a web browser.
   - Streams real-time updates from Service 1.

## Features

- **Asynchronous processing** using FastAPI and aiohttp.
- **Retry mechanism** with exponential backoff in case of service failures.
- **Random failure simulation** for testing fault tolerance.
- **Event streaming** for real-time updates in the frontend.
- **Dockerized deployment** with Docker Compose.
- **CI/CD pipeline** using GitHub Actions, Docker Hub, and Render for automated deployments.

## Requirements

- Python 3.9+
- Docker & Docker Compose
- FastAPI
- Flask
- aiohttp
- requests

## Installation & Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/tic-tac-toe-microservices.git
   cd tic-tac-toe-microservices
   ```
2. Start all services using Docker Compose:
   ```sh
   docker-compose up --build
   ```
3. Access the frontend in a browser:
   ```
   http://localhost:8004
   ```
4. Start a new game via:
   ```sh
   curl -X POST http://localhost:8001/start
   ```

## API Endpoints

### Service 1 (Game Manager)

- **POST `/start`** – Starts the game and streams updates.

### Service 2 (Player X) & Service 3 (Player O)

- **POST `/odigraj`** – Accepts the current game state and returns an updated board.

### Service 4 (Frontend)

- **GET `/`** – Serves the web interface.
- **GET `/stream`** – Streams real-time game updates.

## Deployment

Each service is deployed separately using GitHub Actions:

1. Code changes trigger an **automated build**.
2. The Docker image is **pushed to Docker Hub**.
3. Render **redeploys the updated service** automatically.

## TODO

- Improve AI logic for smarter gameplay.
- Implement user vs AI mode.
- Add unit tests for better reliability.

## Organization

[Juraj Dobrila University of Pula](http://www.unipu.hr/)
[Pula Faculty of Informatics](https://fipu.unipu.hr/)
Distributed Systems, Academic Year 2024./2025.
Mentor: **Nikola Tanković** (https://fipu.unipu.hr/fipu/nikola.tankovic, nikola.tankovic@unipu.hr)
