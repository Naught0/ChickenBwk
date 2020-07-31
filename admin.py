from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['r'], hidden=True)
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, extension_name: str):
        """ Reloads an extension """
        self.bot.reload_extension(extension_name)
        

def setup(bot):
    bot.add_cog(Admin(bot))
