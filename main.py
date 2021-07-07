import os
import re
import json
#import nacl
import discord
import traceback
import validators
import youtube_dl
from discord.ext import commands
from youtube_search import YoutubeSearch

#EDM BOT Command = -
client = commands.Bot(command_prefix="-")

#On Ready
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  activity = discord.Activity(type=discord.ActivityType.playing, name="-commands")
  await client.change_presence(status=discord.Status.online, activity=activity)

# Command
@client.command()
async def join(ctx):
    if not ctx.author.voice:
        return await ctx.send('You are not in a voice channel.')
    channel = ctx.message.author.voice.channel
    voice = ctx.voice_client
    if voice and voice.is_connected():
        song_there = os.path.isfile("song.mp3")
        if song_there:
            os.remove("song.mp3")
        await voice.move_to(channel)
        await ctx.send(f'Moved to {channel}')
    else:
        voice = await channel.connect()
        song_there = os.path.isfile("song.mp3")
        if song_there:
            os.remove("song.mp3")
        await ctx.send(f'Connected to {channel}')


# Play
@client.command()
async def play(ctx, *, search: str):
    valid = validators.url(search)
    print(valid)
    # If Valid URL
    if valid == True:
        print("Url is valid")
        url = search
        # Json
        yt = YoutubeSearch(url, max_results=1).to_json()
        yt_id = str(json.loads(yt)['videos'][0]['id'])
    # If Song Name (Invalid URL)
    else:
        newsearch = search.replace(" ", "")
        print("Invalid url")
        # Json
        yt = YoutubeSearch(newsearch, max_results=1).to_json()
        yt_id = str(json.loads(yt)['videos'][0]['id'])
        # Creating URL
        url = 'https://www.youtube.com/watch?v=' + yt_id

    # Getting Details From JSON
    title = json.loads(yt)['videos'][0]['title']
    duration = json.loads(yt)['videos'][0]['duration']
    channel = json.loads(yt)['videos'][0]['channel']

    # Embed Details
    embedVar = discord.Embed(title=title, description=url, color=0x00ff00)
    embedVar.set_thumbnail(url=json.loads(yt)['videos'][0]['thumbnails'][0])
    embedVar.add_field(name="Channel", value=" ".join(re.findall('[A-Z][a-z]*', channel)), inline=False)
    embedVar.add_field(name="Song Duration", value=duration, inline=False)
    await ctx.channel.send(embed=embedVar)
    # Quality
    ydl_opts = {'format': 'beataudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}

    # If Already Playing
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    ytdl = youtube_dl.YoutubeDL(ydl_opts)
    info = ytdl.extract_info(url, download=False)
    asrc = discord.FFmpegOpusAudio(info['formats'][0]['url'],
                                   before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
    voice.play(asrc)


# Leave
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        await ctx.voice_client.disconnect()
        channel = ctx.message.author.voice.channel
        await ctx.send(f'Disconnected to {channel}')
    else:
        await ctx.send('You have to be connected to the same voice channel to disconnect me.')

#Pause
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")

#Resume
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

#Stop
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

#Commands Starts Here -->

# -play

#@client.command()
#async def play(ctx,*, search:str):
  #valid=validators.url(search)
  #print(valid)
  
 #If str = URL
  #if valid==True:
    #print("Url is valid")
    #url = search
    #voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  #Download Format
    #ydl_opts = {'format': 'bestaudio/best','postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192',}],}
  #Json
    #yt = YoutubeSearch(url, max_results=1).to_json()
    #yt_id = str(json.loads(yt)['videos'][0]['id'])
  #Getting Details From JSON
    #title = json.loads(yt)['videos'][0]['title']
    #duration = json.loads(yt)['videos'][0]['duration']
    #channel = json.loads(yt)['videos'][0]['channel']
  #Embed Details
    #embedVar = discord.Embed(title=title, description=url, color=0x00ff00)
    #embedVar.set_thumbnail(url=json.loads(yt)['videos'][0]['thumbnails'][0])
    #embedVar.add_field(name="Channel", value=" ".join(re.findall('[A-Z][a-z]*', channel)), inline=False)
    #embedVar.add_field(name="Song Duration", value=duration, inline=False)
    #await ctx.channel.send(embed=embedVar)
 
#If str = Song Name (Invalid URL)
  #else:
    #voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    #newsearch = search.replace(" ", "")
    #print("Invalid url")
  #Download Format
    #ydl_opts = {'format': 'beataudio/best','postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]}
  #Json
    #yt = YoutubeSearch(newsearch, max_results=1).to_json()
    #yt_id = str(json.loads(yt)['videos'][0]['id'])
  #Creating URL
    #url = 'https://www.youtube.com/watch?v='+yt_id
  #Getting Details From JSON
    #title = json.loads(yt)['videos'][0]['title']
    #duration = json.loads(yt)['videos'][0]['duration']
    #channel = json.loads(yt)['videos'][0]['channel']
  #Embed Details
    #embedVar = discord.Embed(title=title, description=url, color=0x00ff00)
    #embedVar.set_thumbnail(url=json.loads(yt)['videos'][0]['thumbnails'][0])
    #embedVar.add_field(name="Channel", value=" ".join(re.findall('[A-Z][a-z]*', channel)), inline=False)
    #embedVar.add_field(name="Song Duration", value=duration, inline=False)
    #await ctx.channel.send(embed=embedVar)

#Download Song
  #with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #ydl.download([url])
#If already a Song is Playing
  #if voice.is_playing():
    #voice.stop()
  #song_there = os.path.isfile("song.mp3")
  #if song_there:
    #os.remove("song.mp3")
#Change Suffix
  #for file in os.listdir("./"):
    #if file.endswith(".mp3"):
      #os.rename(file, "song.mp3")
  #voice.play(discord.FFmpegPCMAudio("song.mp3"))

# -command     
   
@client.command()
async def commands(ctx):
    embedVar=discord.Embed(title='EDM Command Lists', description= 'If you have any questions or encounter issues, please contact here:\n https://github.com/belelaritra/EDM\n', color=0x00ff00)
    embedVar.add_field(name="-join", value="To add in Voice Channel", inline=False)
    embedVar.add_field(name="-play _<url or song name>_", value="To Play a Song", inline=False)
    embedVar.add_field(name="-pausse", value="To pause a Song", inline=False)
    embedVar.add_field(name="-resume", value="To resume a paused Song", inline=False)
    embedVar.add_field(name="-stop", value="To Stop a Song", inline=False)
    embedVar.add_field(name="-leave", value="To Leave the Voice Channel", inline=False)
    await ctx.channel.send(embed=embedVar)
    
# Change 'TOKEN' with 'YOUR_TOKEN'
client.run('TOKEN')
