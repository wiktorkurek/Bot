# Discord RSI Bot

This Discord bot fetches the spot K-line data for the SOL/USDT pair from Bybit, calculates the RSI, and sends a message to a Discord channel if the RSI value is over 70 or below 30. The bot runs inside a Docker container.

## Requirements

- Docker
- Python 3.12.4

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/wiktorkurek/Bot.git
   cd Bot

2. Create a .env file with your Discord bot token and channel ID:
   ```sh 
   DISCORD_TOKEN=your_discord_token
   CHANNEL_ID=your_channel_id

3. Build and run the Docker container:
   ```sh
   docker build -t discord-rsi-bot .
   docker run --env-file .env discord-rsi-bot
   
## Potential bugs:
- Few days ago on pandas_ta library there was a bug issued by someone that numpy doesn't support the version of pandas_ta library.
Because of that, I have changed te squeeze_pro.py file in the pandas_ta library and made a modified_squeeze_pro.py file in home directory.