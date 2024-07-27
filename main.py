import discord
import os
import re
import asyncio
import random
from discord.ext import tasks

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot = discord.Bot(intents=discord.Intents.all())

interactions = discord.Interaction

thread_id = None
messages = []
old_prompt = ""
hourLength = 3
winner = None
pingRoleID = int(re.search(r'\d+', os.getenv("ROLE_ID")).group())
ownerID = int(re.search(r'\d+', os.getenv("OWNER_ID")).group())
channel_id = 0

@bot.event
async def on_ready():
    print(f"Signed in as {bot.user}")

@bot.event
async def on_message_delete(ctx):
    for msg in range(len(messages) - 1):
        if messages[msg] == ctx.id:
            messages.pop(msg)

@bot.event
async def on_message(ctx):
    if thread_id != None:
        if ctx.channel.id == thread_id:
            await ctx.add_reaction("🩷")
            messages.append(ctx.id)
            print(f"{ctx.content} {messages}")

@tasks.loop(seconds=5.0)
async def hold(ctx):
    global thread_id
    global old_prompt
    global pingRoleID

    print("NEW GAME")
    
    blackCards = open('blackcards.txt').read().splitlines()
    prompt = random.choice(blackCards)
    while prompt == old_prompt:
        prompt = random.choice(blackCards)

    if pingRoleID > 0:
        msg = await ctx.send(f"<@&{pingRoleID}>\n"+prompt)
    else:
        msg = await ctx.send(prompt)
        
    thread = await msg.create_thread(name="Game Responses")
    thread_id = thread.id
    await thread.edit(
        slowmode_delay = (21600)
    )

    await asyncio.sleep(hourLength * 3600)

    global messages
    global winner

    print("Timer ended")
    for msg in messages:
        if winner == None: 
            winner = msg
            print(winner)

        if bot.get_message(msg) != None:
            if bot.get_message(msg).reactions[0].count > bot.get_message(winner).reactions[0].count:
                print(winner + " cur winner")
                winner = msg
            else:
                print("loser")
                pass
        else:
            print(f"{msg} doesn't exist.")

    thread_id = None
    messages = []

    channel = channel_id # Caching channel id.

    if not winner == None:
        await ctx.send(f'The winner is: <@{bot.get_message(winner).author.id}>!\n\nAnd their message was:\n"{bot.get_message(winner).content}"')
    else:
        await ctx.send(f'There was no winner.')

    await thread.edit(
        archived = True,
        locked = True,
        slowmode_delay = (21600)
    )

    winner = None

@hold.before_loop
async def before_timer():
    print("wait...")
    await bot.wait_until_ready()

@bot.slash_command(name="start")
async def start(ctx):
    if ctx.author.id == int(ownerID):
        await ctx.respond("Bot started!")
        hold.start(ctx=ctx)
        channel_id = bot.get_channel(ctx.channel.id)

@bot.slash_command(name="howtoplay")
async def howtoplay(ctx):
    embed = discord.Embed(
        title="How to Play!",
        description="How the bot works!",
        color = discord.Color.blurple()
    )

    embed.set_author(
        name="NotTechSec",
        icon_url="https://cdn.discordapp.com/avatars/891102358858244096/099fc08c380ceb0c610f1dded273d343?size=1024",
        url="https://twitter.com/NotTechSec" # fuck X. It's twitter.
    )

    embed.add_field(
        name="Rules",
        value=f"Every {hourLength} hours the bot will send a message, and the message will contain a prompt. Your job is to go to the 'Game Responses' thread and come up with a funny answer! Funniest answers win. How can you vote for a funny answer? React to the pink heart!",
        inline=True
    )

    embed.set_footer(text="Programmed by NotTechSec on Twitter!")

    user = await bot.fetch_user(ctx.author.id)
    await user.send(embed=embed)
    await ctx.respond("Rules sent in DMs!")

bot.run(DISCORD_TOKEN)
