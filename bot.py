import os
import discord
import asyncio
import requests
import pandas as pd
import pandas_ta as ta
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

BYBIT_API_URL = 'https://api.bybit.com/v5/market/kline'

intents = discord.Intents.default()
intents.message_content = True


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = None

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.check_rsi())

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def fetch_kline_data(self):
        params = {
            'category': 'spot',
            'symbol': 'SOLUSDT',
            'interval': '60',  # 1H time frame
            'limit': 200
        }
        response = requests.get(BYBIT_API_URL, params=params)
        data = response.json()
        return data['result']['list']

    def calculate_rsi(self, data):
        df = pd.DataFrame(data, columns=['start', 'open', 'high', 'low', 'close', 'volume', 'end'])
        df['close'] = df['close'].astype(float)
        rsi = ta.rsi(df['close'], length=14)  # RSI period of 14 - as asked in mail
        return rsi.iloc[-1]

    async def check_rsi(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID)

        while not self.is_closed():
            data = await self.fetch_kline_data()
            rsi = self.calculate_rsi(data)

            if rsi > 70:
                await channel.send(f'RSI Alert: RSI is above 70 (Current RSI: {rsi:.2f})')
            elif rsi < 30:
                await channel.send(f'RSI Alert: RSI is below 30 (Current RSI: {rsi:.2f})')
            else:
                await channel.send(f'RSI Check: RSI is {rsi:.2f}')

            await asyncio.sleep(3600)  # Check every hour


client = MyClient(intents=intents)

asyncio.run(client.start(DISCORD_TOKEN))
