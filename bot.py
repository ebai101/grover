#!/usr/bin/env python3
'''
TODO:
queueing
playlist
effects
'''

import os
import dotenv
import discord
import discord.ext.commands
import spotipy
import youtube_dl

dotenv.load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client = discord.ext.commands.Bot(command_prefix="!")
sp = spotipy.Spotify(
    client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())


@client.command()
async def search(ctx, *, term):
    await play(ctx, f'ytsearch:{term}')


@client.command()
async def file(ctx: discord.ext.commands.context.Context):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    # start player
    voice.play(discord.FFmpegPCMAudio(ctx.message.attachments[0].url))


@client.command()
async def play(ctx, url):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    # start player
    audio_url = get_audio_stream(url)
    voice.play(discord.FFmpegPCMAudio(audio_url))


def get_audio_stream(term):
    if 'spotify' in term:
        track_info = sp.track(term)
        term = f'ytsearch:{track_info["artists"][0]["name"]} {track_info["name"]}'

    ydl_opts = {
        'format':
        'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'skip_download':
        True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(term, download=False)
        if 'url' not in info:
            print('searched url')
            audio_url = info['entries'][0]['url']
        else:
            print('regular url')
            audio_url = info['url']

        return audio_url


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


client.run(token)
