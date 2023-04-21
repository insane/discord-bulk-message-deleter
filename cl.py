import discord
import asyncio
import json
import random
from termcolor import colored

# Load bot token from config file
with open('config.json', 'r') as f:
    config = json.load(f)

client = discord.Client()

ratelimits = {}
ratelimit_threshold = 3

# Background task to clear the ratelimits table
async def clear_ratelimits():
    while True:
        await asyncio.sleep(60)
        ratelimits.clear()

@client.event
async def on_ready():
    print(colored(f'[READY] > Logged in as {client.user}', 'green'))
    client.loop.create_task(clear_ratelimits())

@client.event
async def on_message(message):
    if message.content.strip().lower() == 'cl':
        await message.delete()

        deleted = []

        async for m in message.channel.history(limit=None, before=message):
            if m.author == client.user:
                try:
                    await m.delete()
                    deleted.append(m)
                except discord.errors.HTTPException as e:
                    if e.status == 429:
                        ratelimits[message.author.id] = ratelimits.get(message.author.id, 0) + 1
                        wait_time = 5 + ratelimits[message.author.id] * 5
                        print(colored(f"[RATELIMIT] > Hit a rate limit! Sleeping for {wait_time} seconds...", 'yellow'))
                        await asyncio.sleep(wait_time)
                        try:
                            await m.delete()
                        except:
                            continue
                    else:
                        print(colored(f"[ERR] > Unexpected error: {e}", 'red'))
                except discord.errors.Forbidden:
                    print(colored("[ERR] > Could not delete message due to permissions error.", 'red'))
                except Exception as e:
                    print(colored(f"[ERR] > Unexpected error: {e}", 'red'))

        print(colored(f"[DELETED] > Deleted {len(deleted)} message(s)", 'green'))

        if ratelimits.get(message.author.id, 0) >= ratelimit_threshold:
            wait_time = random.choice([5, 10, 15, 20])
            print(colored(f"[RATELIMIT] > Exceeded ratelimit threshold. Sleeping for {wait_time} seconds.", 'yellow'))
            await asyncio.sleep(wait_time)
            ratelimits.pop(message.author.id, None)

# Start the bot
client.run(config['token'], bot=False)
