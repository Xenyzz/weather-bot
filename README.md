# Weather Telegram Bot 🌤️

A Telegram bot that shows weather information with a custom-generated image for any city.

## Features
- Add multiple cities per user
- Get weather with a custom visual card (gradient background + icon)
- Delete saved cities
- Multi-user support via SQLite database

## Tech Stack
- Python 3.10+
- aiogram 3.x (Telegram Bot API)
- OpenWeatherMap API
- SQLite (many-to-many user-city relation)
- Pillow (image generation)

## Setup

1. Clone the repository
2. Install dependencies:
```
pip install aiogram python-dotenv requests pillow
```
3. Copy `.env.example` to `.env` and fill in your tokens:
```
TELEGRAM_TOKEN=your_token
API_WEATHER_KEY=your_openweathermap_key
```
4. Run:
```
python bot.py
```

## Project Structure
```
├── bot.py      # Main bot logic and handlers
├── main.py     # OpenWeatherMap API integration
├── db.py       # SQLite database setup and queries
├── draw.py     # Image generation with Pillow
```

---
Made by Nikita Sersts
