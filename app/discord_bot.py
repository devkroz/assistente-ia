import discord
from discord.ext import commands
from app.assistant import ask
from app.config import settings

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

conversation_history: dict[int, list[dict]] = {}


@bot.event
async def on_ready():
    print(f"Discord bot logged in as {bot.user}")


@bot.command(name="ask")
async def ask_command(ctx: commands.Context, *, message: str):
    history = conversation_history.get(ctx.author.id, [])
    response = ask(message, history)
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})
    conversation_history[ctx.author.id] = history[-20:]

    await ctx.reply(response[:2000])


@bot.command(name="clear")
async def clear_history(ctx: commands.Context):
    conversation_history.pop(ctx.author.id, None)
    await ctx.reply("História limpa.")


def run_bot():
    if settings.discord_bot_token:
        bot.run(settings.discord_bot_token)
