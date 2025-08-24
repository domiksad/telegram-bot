# Telegram Bot (Dockerized)

[![Python Version](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

A modular Python Telegram bot running inside Docker. This bot uses the `python-telegram-bot` library and is designed for easy deployment and development using Docker Compose.

## Features

- Built with Python 3.13 and `python-telegram-bot`
- Dockerized for easy deployment
- Persistent database support via Docker volumes
- Modular structure for scalable development
- Automatic code reload in development (optional)

## Prerequisites

- [Docker](https://www.docker.com/get-started) >= 24.x
- [Docker Compose](https://docs.docker.com/compose/compose-file/) >= 2.x
- Python 3.13 (for local development without Docker)

## Getting Started

### Clone the repository

```bash
git clone https://github.com/your-username/telegram-bot.git
cd telegram-bot
```

### Environment Variables

Create a `.env` file in the project root:

```dotenv
TOKEN="your_telegram_bot_token"
```

### Development with Docker

#### Build and run the bot

```bash
docker compose up --build
```

This will build the Docker image and start the bot container.

#### Watch mode (auto-reload)

```bash
docker compose up --watch
```

> Note: Requires Docker Compose with `watch` support.

### Persistent Database

The database is stored in a Docker volume (`./db:/app/db`) to ensure data is preserved across container restarts.

### Stopping the Bot

```bash
docker compose down
```

> Do **not** use `docker compose down -v` if you want to keep your database.

## Local Development (without Docker)

```bash
python -m venv venv
source venv/bin/activate  # Linux / MacOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python -m tg_bot
```

## Contributing

1. Fork the repository
2. Create a new feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## License

This project is licensed under the **Apache License 2.0**.

[Full License](LICENSE)