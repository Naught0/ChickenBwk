import discord
import io
import json
import humanize
import datetime

from discord.ext import commands, tasks


class Pix(commands.Cog):
    IMG_URL = "http://chickens.marc.cx/snapshot"
    CHICKS_BORN = datetime.date(2020, 7, 22)

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.session = self.bot.session
        self.background_check.start()
        self.channel = bot.get_channel(738479047813890078)

    @commands.command(name="pic", aliases=["p", "pix"])
    async def _pic(self, ctx):
        if self.channel == ctx.channel:
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
            j = json.load(f)
            j["num_pix"] = self.bot.num_pix
            json.dump(j, f)

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
        em = discord.Embed(title=":bar_chart::hatching_chick: Chik'n Stats", color=discord.Color.gold())
        em.add_field(
            name=":egg::hatched_chick::chicken: Chick Age",
            value=f"```{humanize.naturaldelta(datetime.date.today() - self.CHICKS_BORN)}```"
        )
        em.add_field(
            name=":frame_photo: Total Pics",
            value=f"```{self.bot.num_pix}```"
        )
        em.add_field(
            name=":clock1: Bot Uptime",
            value=f"```{humanize.naturaldelta(datetime.datetime.now() - self.bot.start_time)}```"
        )

        await self.channel.send(embed=em)

    @tasks.loop(seconds=10.0)
    async def background_check(self):
        current_hour = datetime.datetime.now().hour

        if current_hour != self.bot.last_hour:
            self.bot.last_hour = current_hour
            await self.send_pic(self.channel)


def setup(bot):
    bot.add_cog(Pix(bot))
