# Rare Truth Bot (v2)

## Features
- Monitors RUNE/USDT price via DexScreener API
- Sends alerts via Telegram:
  - 📡 Watch zone proximity
  - 🚨 Trigger zone hit
- Can be extended with RSI or other indicators later

## Setup
1. Set up a Telegram Bot using BotFather.
2. Create a `.env` file based on `.env.example`
3. Deploy to Railway.

## Environment Variables
- `TELEGRAM_TOKEN`: Your bot token
- `CHAT_ID`: Your Telegram user or group ID

## Extend Later
- Add RSI or stochastic logic
- Log alerts and trade actions to Google Sheets
- Auto report back to a local LLM or run logic via webhook
