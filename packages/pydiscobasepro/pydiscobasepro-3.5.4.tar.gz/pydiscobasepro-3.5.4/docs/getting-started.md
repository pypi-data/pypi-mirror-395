---
layout: default
title: Getting Started
nav_order: 2
---

# Getting Started with PyDiscoBasePro

## Prerequisites

- Python 3.11 or higher
- A Discord bot token (from [Discord Developer Portal](https://discord.com/developers/applications))
- MongoDB instance (local or cloud)

## Installation

```bash
pip install pydiscobasepro
```

## Create Your First Bot

```bash
pydisco create MyFirstBot
cd MyFirstBot
pip install -r requirements.txt
```

## Configuration

Edit `config/config.json`:

```json
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "prefix": "!",
  "intents": {
    "guilds": true,
    "members": true,
    "messages": true,
    "message_content": true
  },
  "mongodb": {
    "uri": "mongodb://localhost:27017",
    "database": "myfirstbot"
  }
}
```

## Run Your Bot

```bash
python bot.py
```

Your bot should now be online! Invite it to your server using the OAuth2 URL from the Discord Developer Portal.

## Add Your First Command

Create `commands/hello.py`:

```python
import discord
from discord import app_commands

class Hello:
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database
        self.name = "hello"
        self.description = "Say hello!"

        self.slash_command = app_commands.Command(
            name=self.name,
            description=self.description,
            callback=self.run
        )

    async def run(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello, World! 🌍")

# The framework will automatically load this command!
```

## Next Steps

- Explore the [API documentation](api.md)
- Learn about [advanced configuration](configuration.md)
- Check out [deployment options](deployment.md)
- Join our [Discord community](https://discord.gg/pydiscobasepro)