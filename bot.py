import json
from datetime import datetime

import aiohttp
import discord
from discord.ext import commands


class ChickenBwk(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.description = "chik'n pix"

        with open("stuff.json") as f:
            file = json.load(f)

        self.token = file["token"]
        self.num_pix = file["num_pix"]
        self.num_brood_pix = file["num_brood_pix"] if "num_brood_pix" in file else 0
        self.startup_ext = ["admin", "pix"]

        super().__init__(
            command_prefix="!",
            description=self.description,
            pm_help=None,
            case_insensitive=True,
            *args,
            **kwargs,
        )

    def run(self):
        super().run(self.token)

    async def on_ready(self):
        self.session = aiohttp.ClientSession()

        if not hasattr(self, "start_time"):
            self.start_time = datetime.now()
            self.last_hour = self.start_time.hour

        for x in self.startup_ext:
            await self.load_extension(x)

        print(f"Client logged in at {self.start_time}")
        print("".join(["-" for x in range(80)]))


if __name__ == "__main__":
    bot = ChickenBwk(intents=discord.Intents.default())
    bot.run()
