import aiohttp
import discord
import asyncio
import json
import io

from datetime import datetime
from discord.ext import commands, tasks


class ChickenBwk(commands.Bot):
    IMG_URL = "http://chickens.marc.cx/snapshot"

    def __init__(self, *args, **kwargs):
        self.description = "chik'n pix"

        with open("stuff.json") as f:
            file = json.load(f)

        self.token = file["token"]
        self.num_pix = file["num_pix"]

        super().__init__(
            command_prefix="!",
            description=self.description,
            pm_help=None,
            case_insensitive=True,
            *args,
            **kwargs,
        )
        self.session = aiohttp.ClientSession(loop=self.loop)

    def run(self):
        super().run(self.token)

    async def send_pic(self, channel):
        async with self.session.get(self.IMG_URL) as resp:
            buf = io.BytesIO(await resp.read())

        self.num_pix += 1

        await channel.send(
            content=":rotating_light: :rotating_light: :rotating_light: :baby_chick: **CHICK ALART** :baby_chick: :rotating_light: :rotating_light: :rotating_light:",
            file=discord.File(buf, "chick_pix.png"),
        )

        with open("stuff.json", "w") as f:
            json.dump({"token": self.token, "num_pix": self.num_pix}, f)

    @tasks.loop(seconds=10.0)
    async def background_check(self):
        channel = self.get_channel(738479047813890078)
        current_hour = datetime.now().hour

        if current_hour != self.last_hour:
            self.last_hour == current_hour
            await self.send_pic(channel)

    async def on_ready(self):
        if not hasattr(self, "start_time"):
            self.start_time = datetime.now()
            self.last_hour = self.start_time.hour

        print(f"Client logged in at {self.start_time}")
        print("".join(["-" for x in range(80)]))

        await self.wait_until_ready()
        channel = self.get_channel(738479047813890078)
        await self.send_pic(channel)
        await self.background_check.start()


if __name__ == "__main__":
    bot = ChickenBwk()
    bot.run()
