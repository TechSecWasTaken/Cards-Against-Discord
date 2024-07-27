import discord
import os
import asyncio
import random
from discord.ext import tasks

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot = discord.Bot(intents=discord.Intents.all())

thread_id = None
messages = []
old_prompt = ""
hourLength = 3
winner = None

@bot.event
async def on_ready():
    print(f"Signed in as {bot.user}")

@bot.event
async def on_message(ctx):
    if thread_id != None:
        if ctx.channel.id == thread_id:
            await ctx.add_reaction("🩷")
            messages.append(ctx.id)
            print(f"{ctx.content} {messages}")

@tasks.loop(seconds=5.0)
async def hold(ctx):
    print("started")
    global thread_id
    global old_prompt
    
    blackCards = open('blackcards.txt').read().splitlines()
    prompt = random.choice(blackCards)

    while prompt == old_prompt:
        prompt = random.choice(blackCards)

    msg = await ctx.send(prompt)
    thread = await msg.create_thread(name="Game Responses")
    thread_id = thread.id

    await asyncio.sleep(hourLength * 3600)

    global messages
    global winner

    print("Timer ended")
    for msg in messages:
        if winner == None: 
            winner = msg
            print(winner)
        
        if bot.get_message(msg).reactions[0].count > bot.get_message(winner).reactions[0].count:
            print(winner)
            winner = msg
        else:
            print("loser")
            pass

    thread_id = None
    messages = []

    if not winner == None:
        await ctx.send(f'The winner is: <@{bot.get_message(winner).author.id}>!\n\nAnd their message was:\n"{bot.get_message(winner).content}"')
    else:
        await ctx.send(f'There was no winner.')

    winner = None

@hold.before_loop
async def before_timer():
    print("wait...")
    await bot.wait_until_ready()

@bot.slash_command()
async def start(ctx):
    if ctx.author.id == 891102358858244096:
        hold.start(ctx=ctx)

bot.run(DISCORD_TOKEN)
