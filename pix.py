import discord
import io
import json
import humanize
import datetime
import time

from discord.ext import commands, tasks


class Pix(commands.Cog):
    IMG_URL = "http://chickens.marc.cx/snapshot2"
    BROOD_BORN = datetime.date(2021, 3, 29)
    CHICKS_BORN = datetime.date(2020, 7, 22)
    GIF_URL = "http://chickens.marc.cx/snapshot.webm"

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.session = self.bot.session
        self.background_check.start()
        self.channel = bot.get_channel(738479047813890078)
        self.num_brood_pix = bot.num_brood_pix if hasattr(bot, 'num_brood_pix') else 0

    @commands.command(name="gif", aliases=["clip"])
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def _gif(self, ctx: commands.Context):
        """Get a gif of the last 30 seconds of coop activity"""
        if self.channel != ctx.channel:
            return

        image = f"{self.GIF_URL}?{int(time.time())}"
        async with self.session.get(image) as resp:
            buf = io.BytesIO(await resp.read())

        await self.channel.send(
            content=f":baby_chick: **CHICKEN CLIP** :baby_chick:",
            file=discord.File(
                buf,
                f"chick_clip{datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y%m%d%H%M%S%f')}.webm",
            ),
        )

    @commands.command(name="pic", aliases=["p", "pix"])
    @commands.cooldown(1, 10.0, commands.BucketType.guild)
    async def _pic(self, ctx):
        if self.channel == ctx.channel:
            await self.send_pic(ctx.channel)

    async def send_pic(self, channel):
        async with self.session.get(self.IMG_URL) as resp:
            buf = io.BytesIO(await resp.read())

        await channel.send(
            content=":chicken: **CHICKEN STATUS** :chicken:",
            file=discord.File(
                buf,
                f"chick_pix{datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y%m%d%H%M%S%f')}.png",
            ),
        )

        self.bot.num_pix += 1
        self.num_brood_pix += 1
        self.bot.num_brood_pix = self.num_brood_pix
        with open("stuff.json", "w") as f:
            json.dump({"token": self.bot.token, "num_pix": self.bot.num_pix, "num_brood_pix": self.bot.num_brood_pix}, f)

    def cog_unload(self):
        self.background_check.cancel()

    @commands.command(name="stop", aliases=["disable"])
    async def _stop(self, ctx: commands.Context):
        if self.background_check.is_running():
            em = discord.Embed(
                title=":octagonal_sign: Chik'n pix stopped",
                description=f"By: {ctx.author.mention}",
                color=discord.Color.blurple(),
            )
            await self.channel.send(embed=em)

            self.background_check.cancel()
            await ctx.message.add_reaction("🐣")

        else:
            await ctx.message.add_reaction("🟥")  # Red square

    @commands.command(name="start", aliases=["enable"])
    async def _start(self, ctx: commands.Context):
        if self.background_check.is_running():
            await ctx.message.add_reaction("🟥")  # Red square
        else:
            self.background_check.start()
            await ctx.message.add_reaction("🐣")

    @commands.command(name="status", aliases=["stats", "info"])
    async def _status(self, ctx: commands.Context):
        _delta = datetime.date.today() - self.CHICKS_BORN
        _weeks, _days = divmod(_delta.days, 7)

        brood_delta = datetime.date.today() - self.BROOD_BORN
        brood_weeks, brood_days = divmod(brood_delta.days, 7)

        em = discord.Embed(
            title=":bar_chart::hatching_chick: Chik'n Stats", color=discord.Color.gold()
        )
        em.add_field(
            name=":egg::hatched_chick::chicken: Chicken Age",
            value=f"```{_weeks} weeks {_days} day(s)```",
        )
        em.add_field(
            name=":egg::hatched_chick::baby_chick: Chick Age",
            value=f"```{brood_weeks} weeks {brood_days} day(s)```"
        )
        em.add_field(name=":frame_photo::chicken: Total Chicken Pix", value=f"```{self.bot.num_pix}```")
        em.add_field(name=":frame_photo::baby_chick: Total Chick Pix", value=f"```{self.num_brood_pix}```")
        em.add_field(
            name=":clock1: Bot Uptime",
            value=f"```{humanize.precisedelta(datetime.datetime.now() - self.bot.start_time)}```",
        )

        await self.channel.send(embed=em)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.message.add_reaction("🟥")

        print(f"Ignoring exception in command {ctx.command}: {error}")

    @tasks.loop(seconds=10.0)
    async def background_check(self):
        current_hour = datetime.datetime.now().hour

        if current_hour != self.bot.last_hour:
            self.bot.last_hour = current_hour
            await self.send_pic(self.channel)


def setup(bot):
    bot.add_cog(Pix(bot))
