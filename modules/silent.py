import discord
import asyncio
import json
import random
from colorama import init
from termcolor import colored

init()

with open('./config.json', 'r') as f:
    config = json.load(f)

client = discord.Client()

ratelimits = []
ratelimit_threshold = 3

async def clear_ratelimits():
    while True:
        await asyncio.sleep(60)
        ratelimits.clear()

@client.event
async def on_ready():
    print(colored(f'[READY] > Logged in as {client.user}', 'green'))
    client.loop.create_task(clear_ratelimits())
    while 1:
        channel = client.get_channel(int(input('Discord Message Link: ').split('/')[5]))
        deleted = []

        async for m in channel.history(limit=None):
            if m.author == client.user:
                try:
                    await m.delete()
                    deleted.append(m)
                except Exception as e:
                    if isinstance(e, discord.errors.HTTPException):
                        if e.status == 429:
                            ratelimits.append(1)
                            print(colored(f"[RATELIMIT] > Hit a rate limit! Sleeping for {5 + len(ratelimits) * 5} seconds..", 'yellow'))
                            await asyncio.sleep(5 + len(ratelimits) * 5)
                            try:
                                await m.delete()
                            except:
                                continue
                            continue
                        
                    elif isinstance(e, discord.errors.Forbidden):
                        print(colored("[ERR] > Could not delete message due to permissions error.", 'red'))
                    else:
                        print(colored(f"[ERR] > Unexpected error: {e}", 'red'))

        print(colored(f"[DELETED] > Deleted {len(deleted)} message(s)", 'green'))

        if len(ratelimits) >= ratelimit_threshold:
            wait_time = random.choice([5, 10, 15, 20])
            print(colored(f"[RATELIMIT] > Exceeded ratelimit threshold. Sleeping for {wait_time} seconds.", 'yellow'))
            await asyncio.sleep(wait_time)
            ratelimits.clear()

client.run(config['token'], bot=False)