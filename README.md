# Tic-Tac-Toe Distributed System

This project is a distributed microservices-based Tic-Tac-Toe game built using FastAPI and Flask. The game is played by two AI-based services that take turns making moves, while a main service manages the game flow and a frontend service provides a user interface.

## Architecture

The system consists of four services:

1. **Service 1: [servis_nova_igra] (Game Manager - FastAPI)**

   - Controls the game loop.
   - Sends the Tic-Tac-Toe board to player services.
   - Determines the winner and handles retries in case of failures.

2. **Service 2: [servis_igraci] (Players X and O - FastAPI)**

   - Plays as `X` or `o`.
   - Chooses moves based on simbol's strategy.

3. **Service 3: [servis_igra4. **Service 4: [servis_frontend] (Frontend - Flask)\*\*
   - Displays the game board in a web browser.
   - Streams real-time updates from Service 1.

## Features

- **Asynchronous processing** using FastAPI and aiohttp.
- **Retry mechanism** with exponential backoff in case of service failures.
- **Random failure simulation** for testing fault tolerance.
- **Event streaming** for real-time updates in the frontend.
- **Dockerized deployment** with Docker Compose.

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

### Service 2 (Player & Player O)

- **POST `/odigraj`** – Accepts the current game state and returns an updated board.

### Service 3 (Frontend)

- **GET `/`** – Serves the web interface.
- **GET `/stream`** – Streams real-time game updates.

## Organization

[Juraj Dobrila University of Pula](http://www.unipu.hr/)
[Pula Faculty of Informatics](https://fipu.unipu.hr/)
Distributed Systems, Academic Year 2024./2025.
Mentor: **Nikola Tanković** (https://fipu.unipu.hr/fipu/nikola.tankovic, nikola.tankovic@unipu.hr)
