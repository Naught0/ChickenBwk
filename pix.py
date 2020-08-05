import discord
import io
import json

from datetime import datetime
from discord.ext import commands, tasks


class Pix(commands.Cog):
    IMG_URL = "http://chickens.marc.cx/snapshot"

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.session = self.bot.session
        self.background_check.start()

    @commands.command(name="pic", aliases=['p', 'pix'])
    async def _pic(self, ctx):
        if self.bot.get_channel(738479047813890078) == ctx.channel:
            await self.send_pic(ctx.channel)

    async def send_pic(self, channel):
        async with self.session.get(self.IMG_URL) as resp:
            buf = io.BytesIO(await resp.read())

        await channel.send(
            content=":baby_chick: **CHICK STATUS** :baby_chick:",
            file=discord.File(buf, "chick_pix.png"),
        )

        self.bot.num_pix += 1
        with open("stuff.json", "w") as f:
            json.dump({"token": self.bot.token, "num_pix": self.bot.num_pix}, f)

    def cog_unload(self):
        self.background_check.cancel()

    @commands.command(name='stop', aliases=['disable'])
    async def _stop(self, ctx):
        self.background_check.cancel()
    
    @commands.command(name='start', aliases=['enable'])
    async def _start(self, ctx):
        self.background_check.start()

    @tasks.loop(seconds=10.0)
    async def background_check(self):
        channel = self.bot.get_channel(738479047813890078)
        current_hour = datetime.now().hour

        if current_hour != self.bot.last_hour:
            self.bot.last_hour = current_hour
            await self.send_pic(channel)


def setup(bot):
    bot.add_cog(Pix(bot))
