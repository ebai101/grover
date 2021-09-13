#!/usr/bin/env python3

'''
TODO:
spotify support
effects
'''

from __future__ import unicode_literals
import discord
from discord.ext import commands
import youtube_dl
import os
from dotenv import load_dotenv

client = commands.Bot(command_prefix="!")

@client.command()
async def play(ctx, url : str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'skip_download': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        # print(info['url'])
        voice.play(discord.FFmpegPCMAudio(info['url']))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client.run(token)
