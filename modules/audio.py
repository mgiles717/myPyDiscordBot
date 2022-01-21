import discord
from discord.ext import commands
import youtube_dl


class AudioHandler(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await ctx.send("Joining")
            await voice_channel.connect()
        else:
            await ctx.send("Moving channels")
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnecting")
        self.queue.clear()

    @commands.command()
    async def play(self, ctx, url):
        await self.join(ctx)
        ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        ydl_options = {'format':'bestaudio'}
        vc = ctx.voice_client
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options, executable='ffmpeg/bin/ffmpeg.exe')
            self.queue.append(source)
            vc.play(self.queue[0])
            self.queue.pop(0)
        await ctx.send(f"Playing {url}")

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Paused")

    @commands.command()
    async def stop(self, ctx):
        #await ctx.voice_client.
        return

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Resuming")

    @commands.command()
    async def clear(self, ctx):
        self.queue.clear()
        await ctx.send("Queue cleared")

    @commands.command()
    async def skip(self, ctx):
        # Unfinished
        pass

    @commands.command()
    async def musichelp(self, ctx):
        embed = discord.Embed(title="All music commands",
                              description="A list of all available functions and how to use them.")
        embed.add_field(name='!join', value="Used to get the bot into your voice channel")
        embed.add_field(name='!disconnect', value="Disconnects the bot from your voice channel")
        embed.add_field(name='!play (url)', value="Plays the song if no song is playing, otherwise queues the song")
        embed.add_field(name='!pause', value="Pauses the song")
        embed.add_field(name='!resume', value="Resumes the song after paused")
        embed.add_field(name='!clear', value="Clears the queue")
        embed.add_field(name='!skip', value="Skips the current song")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(AudioHandler(client))
