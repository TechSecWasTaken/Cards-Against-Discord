# Cards Against Discord/Servers

## Setup Instructions
(THESE INSTRUCTIONS ARE MADE WITH THE IDEA THAT YOU KNOW HOW TO SET UP A BOT IN THE DISCORD DEVELOPER PORTAL. 
IF NOT GO FOLLOW [THIS GUIDE.](https://discord.com/developers/docs/quick-start/getting-started))

You're going to need a few things to get this to work if you want to use this in your server.
First you're obviously going to want the **latest version of Python.**

Then, you're going to want to run this command:
```
pip install pycord
```

Now you have the Discord Python library installed. Which means you can go to the next step.
Go to your Discord Developer Portal and go to **Bot > Privileged Gateway Intents** and turn on everything under it.
This is so the bot can actually do stuff.

Now, go to the source code and go to the .env file.
You're going to want to change some variables, such as making sure that "DISCORD_TOKEN" is your bot's token.
And you want to change "OWNER_ID" with your Discord ID so you can be the only one to start the bot.

Once finished, go to where you downloaded the source code and go to your terminal.
Run these commands:
```
cd C:/directory/to/source/code
python main.py
```

If done correctly, the bot should've printed "Logged in as User#1234". (Obviously User#1234 being YOUR bot's name and tag.)

If not, then look back at the errors or send them to me and I can help instruct you.

Enjoy the bot!
