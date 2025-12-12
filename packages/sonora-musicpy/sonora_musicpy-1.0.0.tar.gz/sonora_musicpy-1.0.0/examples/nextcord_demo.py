"""Minimal Nextcord bot example for Sonora."""

import os
import nextcord
from nextcord.ext import commands
from sonora import SonoraClient

# Load environment variables
LAVALINK_HOST = os.getenv("LAVALINK_HOST", "127.0.0.1")
LAVALINK_PORT = int(os.getenv("LAVALINK_PORT", "2333"))
LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD", "youshallnotpass")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Create bot
bot = commands.Bot(command_prefix='!')

# Create Sonora client
sonora = SonoraClient(
    lavalink_nodes=[{
        "host": LAVALINK_HOST,
        "port": LAVALINK_PORT,
        "password": LAVALINK_PASSWORD
    }],
    node_pooling=True,
    reconnect_policy={"max_retries": 5, "backoff": "exponential"}
)

@bot.event
async def on_ready():
    await sonora.start()
    print(f'Logged in as {bot.user}')

@bot.command()
async def join(ctx):
    """Join the voice channel."""
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        player = await sonora.get_player(ctx.guild.id)
        await ctx.send("Joined voice channel!")
    else:
        await ctx.send("You need to be in a voice channel!")

@bot.command()
async def play(ctx, *, query):
    """Play a track."""
    player = await sonora.get_player(ctx.guild.id)
    # For demo, assume query is a direct URL or search
    track = await sonora.load_track(query)
    if track:
        await player.play(track)
        await ctx.send(f"Now playing: {track.title}")
    else:
        await ctx.send("Track not found!")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Please set DISCORD_TOKEN environment variable")
        exit(1)
    bot.run(DISCORD_TOKEN)