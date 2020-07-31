import discord
import io
import json

from datetime import datetime
from discord.ext import commands, tasks


class Pix(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.session = self.bot.session
        self.background_check.start()

    async def send_pic(self, channel):
        async with self.session.get(self.IMG_URL) as resp:
            buf = io.BytesIO(await resp.read())

        await channel.send(
            content=":baby_chick: **CHICK STATUS** :baby_chick:",
            file=discord.File(buf, "chick_pix.png"),
        )

        with open("stuff.json", "w") as f:
            json.dump({"token": self.token, "num_pix": self.num_pix}, f)

    def cog_unload(self):
        self.background_check.cancel()

    @tasks.loop(seconds=10.0)
    async def background_check(self):
        channel = self.bot.get_channel(738479047813890078)
        current_hour = datetime.now().hour

        if current_hour != self.bot.last_hour:
            self.last_hour = current_hour
            await self.send_pic(channel)


def setup(bot):
    bot.add_cog(Pix(bot))
