import discord
from discord.ui import Button, View

class TestButton:
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database

        @self.bot.event
        async def on_interaction(interaction: discord.Interaction):
            if interaction.type == discord.InteractionType.component:
                if interaction.custom_id == "test_button":
                    await interaction.response.send_message("Button clicked!", ephemeral=True)

# To use in a command, create a view with button
# view = View()
# button = Button(label="Click me", custom_id="test_button")
# view.add_item(button)
# await ctx.send("Test", view=view)