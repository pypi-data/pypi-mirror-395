import discord
from discord import app_commands
from discord.ext import commands

class Ping:
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database
        self.name = "ping"
        self.description = "Check bot latency"
        self.aliases = ["pong"]
        self.permissions = []  # List of permissions required
        self.cooldown = 5  # Seconds

        # Prefix command
        self.prefix_command = commands.command(name=self.name, aliases=self.aliases, help=self.description)(
            self.run_prefix
        )

        # Slash command
        self.slash_command = app_commands.Command(
            name=self.name,
            description=self.description,
            callback=self.run_slash
        )

    async def run_prefix(self, ctx):
        # Check permissions
        if self.permissions and not all(getattr(ctx.author.guild_permissions, perm, False) for perm in self.permissions):
            return await ctx.send("You don't have permission to use this command.")

        # Check cooldown
        from utils import cooldown_manager
        key = f"{ctx.author.id}_{self.name}"
        if not await cooldown_manager.check_cooldown(key, self.cooldown):
            return await ctx.send("Command on cooldown.")

        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(title="Pong!", description=f"Latency: {latency}ms", color=0x00ff00)
        await ctx.send(embed=embed)

    async def run_slash(self, interaction: discord.Interaction):
        # Similar checks
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(title="Pong!", description=f"Latency: {latency}ms", color=0x00ff00)
        await interaction.response.send_message(embed=embed)