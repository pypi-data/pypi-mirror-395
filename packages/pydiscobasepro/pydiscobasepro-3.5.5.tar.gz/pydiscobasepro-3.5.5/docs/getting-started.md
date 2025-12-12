---
layout: default
title: Getting Started
nav_order: 2
---

<div class="page-header">
  <h1><i class="fas fa-rocket"></i> Getting Started with PyDiscoBasePro</h1>
  <p class="page-subtitle">Build your first Discord bot in under 10 minutes with our comprehensive framework</p>
</div>

## 📋 Prerequisites

<div class="prerequisites-grid">
  <div class="prereq-item">
    <div class="prereq-icon">🐍</div>
    <div class="prereq-content">
      <h4>Python 3.11+</h4>
      <p>Latest Python version for optimal performance</p>
      <code>python --version</code>
    </div>
  </div>

  <div class="prereq-item">
    <div class="prereq-icon">🤖</div>
    <div class="prereq-content">
      <h4>Discord Bot Token</h4>
      <p>Create a bot at <a href="https://discord.com/developers/applications">Discord Developer Portal</a></p>
      <a href="https://discord.com/developers/applications" class="btn btn-sm">Get Token</a>
    </div>
  </div>

  <div class="prereq-item">
    <div class="prereq-icon">🗄️</div>
    <div class="prereq-content">
      <h4>MongoDB Database</h4>
      <p>Local installation or cloud service (MongoDB Atlas)</p>
      <a href="https://www.mongodb.com/atlas" class="btn btn-sm">MongoDB Atlas</a>
    </div>
  </div>
</div>

## 🚀 Quick Installation

<div class="installation-tabs">
  <div class="tab-buttons">
    <button class="tab-btn active" data-tab="pip">pip</button>
    <button class="tab-btn" data-tab="docker">Docker</button>
    <button class="tab-btn" data-tab="source">From Source</button>
  </div>

  <div class="tab-content">
    <div class="tab-pane active" id="pip">
```bash
# Install PyDiscoBasePro
pip install pydiscobasepro

# Verify installation
pydiscobasepro --version
```
    </div>

    <div class="tab-pane" id="docker">
```bash
# Pull the official Docker image
docker pull code-xon/pydiscobasepro:latest

# Run with Docker
docker run -it code-xon/pydiscobasepro:latest
```
    </div>

    <div class="tab-pane" id="source">
```bash
# Clone the repository
git clone https://github.com/code-xon/pydiscobasepro.git
cd pydiscobasepro

# Install in development mode
pip install -e .

# Run tests to verify
python -m pytest tests/
```
    </div>
  </div>
</div>

## 🎯 Create Your First Bot

<div class="step-by-step">
  <div class="step-card">
    <div class="step-header">
      <span class="step-number">1</span>
      <h3>Use the CLI to Create a Project</h3>
    </div>
    <div class="step-content">
```bash
# Create a new bot project
pydiscobasepro project create my-awesome-bot

# Navigate to the project
cd my-awesome-bot

# Install dependencies
pip install -r requirements.txt
```
    </div>
  </div>

  <div class="step-card">
    <div class="step-header">
      <span class="step-number">2</span>
      <h3>Configure Your Bot</h3>
    </div>
    <div class="step-content">
      <p>Edit the configuration file:</p>
      <code>config/config.json</code>

```json
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "prefix": "!",
  "description": "My Awesome Discord Bot",
  "version": "1.0.0",

  "intents": {
    "guilds": true,
    "members": true,
    "messages": true,
    "message_content": true,
    "voice_states": true
  },

  "mongodb": {
    "uri": "mongodb://localhost:27017",
    "database": "my_awesome_bot",
    "collections": {
      "users": "users",
      "guilds": "guilds",
      "logs": "logs"
    }
  },

  "logging": {
    "level": "INFO",
    "file": "logs/bot.log",
    "max_size": "10MB",
    "backup_count": 5
  },

  "dashboard": {
    "enabled": true,
    "host": "0.0.0.0",
    "port": 8080,
    "secret_key": "your-secret-key-here"
  }
}
```
    </div>
  </div>

  <div class="step-card">
    <div class="step-header">
      <span class="step-number">3</span>
      <h3>Launch Your Bot</h3>
    </div>
    <div class="step-content">
```bash
# Start your bot
python bot.py

# You should see output like:
# [INFO] PyDiscoBasePro v3.5.5 starting...
# [INFO] Connected to Discord as MyAwesomeBot#1234
# [INFO] Dashboard running on http://0.0.0.0:8080
```
    </div>
  </div>
</div>

## 🎨 Add Your First Command

<div class="command-tutorial">
  <div class="tutorial-header">
    <h3>Create a Hello World Command</h3>
    <p>Let's create a simple slash command that responds with a greeting.</p>
  </div>

  <div class="file-structure">
    <h4>File Structure</h4>
    <pre><code>my-awesome-bot/
├── commands/
│   └── hello.py          # Your command file
├── events/
│   └── on_ready.py       # Bot ready event
├── config/
│   └── config.json       # Configuration
├── bot.py                # Main bot file
└── requirements.txt      # Dependencies</code></pre>
  </div>

  <div class="code-example">
    <h4>Create <code>commands/hello.py</code></h4>
```python
import discord
from discord import app_commands
from pydiscobasepro.core.database import Database

class HelloCommand:
    """A friendly hello command with multiple greeting options."""

    def __init__(self, bot, database: Database):
        self.bot = bot
        self.database = database
        self.name = "hello"
        self.description = "Say hello with various greetings!"

        # Create the slash command
        self.slash_command = app_commands.Command(
            name=self.name,
            description=self.description,
            callback=self.run
        )

        # Add options to the command
        self.slash_command.add_option(
            name="greeting",
            description="Choose your greeting style",
            type=discord.AppCommandOptionType.string,
            choices=[
                discord.app_commands.Choice(name="Friendly", value="friendly"),
                discord.app_commands.Choice(name="Formal", value="formal"),
                discord.app_commands.Choice(name="Funny", value="funny"),
                discord.app_commands.Choice(name="Custom", value="custom")
            ],
            required=False
        )

        self.slash_command.add_option(
            name="target",
            description="Who to greet (leave empty for yourself)",
            type=discord.AppCommandOptionType.user,
            required=False
        )

    async def run(self, interaction: discord.Interaction, greeting: str = "friendly", target: discord.User = None):
        """Execute the hello command."""

        # Determine the greeting message
        greetings = {
            "friendly": "Hey there! 👋",
            "formal": "Greetings and salutations!",
            "funny": "Well hello there, fancy seeing you here! 🤪",
            "custom": "Hello, beautiful person! ✨"
        }

        message = greetings.get(greeting, greetings["friendly"])

        # Add target if specified
        if target:
            if target == interaction.user:
                message += f" (talking to yourself, {interaction.user.display_name}?)"
            else:
                message += f" (directed at {target.display_name})"
        else:
            message += f" (nice to meet you, {interaction.user.display_name}!)"

        # Log command usage
        await self.database.increment_command_usage("hello")

        # Send response
        embed = discord.Embed(
            title="👋 Hello!",
            description=message,
            color=discord.Color.blue()
        )

        embed.set_footer(text=f"Command executed by {interaction.user}")

        await interaction.response.send_message(embed=embed)

# Export for auto-loading
hello_command = HelloCommand
```
  </div>

  <div class="command-testing">
    <h4>Test Your Command</h4>
    <ol>
      <li>Make sure your bot is running</li>
      <li>In Discord, type <code>/hello</code></li>
      <li>Try different options: <code>/hello greeting:funny</code></li>
      <li>Tag someone: <code>/hello target:@username</code></li>
    </ol>
  </div>
</div>

## 🎛️ Explore the Web Dashboard

<div class="dashboard-intro">
  <div class="dashboard-preview">
    <h3>Built-in Web Dashboard</h3>
    <p>Your bot comes with a comprehensive web interface for monitoring and management.</p>

    <div class="dashboard-features">
      <div class="feature">
        <i class="fas fa-chart-line"></i>
        <span>Real-time Metrics</span>
      </div>
      <div class="feature">
        <i class="fas fa-terminal"></i>
        <span>Command Logs</span>
      </div>
      <div class="feature">
        <i class="fas fa-cogs"></i>
        <span>Configuration</span>
      </div>
      <div class="feature">
        <i class="fas fa-users"></i>
        <span>User Management</span>
      </div>
    </div>
  </div>

  <div class="dashboard-access">
```bash
# Access the dashboard
# Open your browser to: http://localhost:8080

# Default credentials:
# Username: admin
# Password: admin123
```
  </div>
</div>

## 🔧 Advanced Configuration

<div class="config-sections">
  <div class="config-section">
    <h4>Database Configuration</h4>
```json
{
  "mongodb": {
    "uri": "mongodb+srv://username:password@cluster.mongodb.net/",
    "database": "my_bot_db",
    "connection_timeout": 5000,
    "server_selection_timeout": 5000
  }
}
```
  </div>

  <div class="config-section">
    <h4>Security Settings</h4>
```json
{
  "security": {
    "rate_limit": {
      "commands_per_minute": 30,
      "global_cooldown": 2
    },
    "encryption": {
      "enabled": true,
      "key_rotation_days": 30
    }
  }
}
```
  </div>

  <div class="config-section">
    <h4>Plugin Configuration</h4>
```json
{
  "plugins": {
    "enabled": true,
    "sandbox_enabled": true,
    "auto_update": true,
    "marketplace_url": "https://plugins.pydiscobasepro.com"
  }
}
```
  </div>
</div>

## 🚀 Next Steps

<div class="next-steps-grid">
  <div class="next-step">
    <div class="step-icon">📚</div>
    <h4>Learn More</h4>
    <p>Dive deeper into the framework capabilities.</p>
    <a href="api.html">API Reference →</a>
  </div>

  <div class="next-step">
    <div class="step-icon">⚙️</div>
    <h4>Advanced Config</h4>
    <p>Explore all configuration options.</p>
    <a href="configuration.html">Configuration →</a>
  </div>

  <div class="next-step">
    <div class="step-icon">🚀</div>
    <h4>Deploy to Production</h4>
    <p>Get your bot ready for production.</p>
    <a href="deployment.html">Deployment →</a>
  </div>

  <div class="next-step">
    <div class="step-icon">💬</div>
    <h4>Join Community</h4>
    <p>Get help and share your creations.</p>
    <a href="https://discord.gg/pydiscobasepro">Discord Server →</a>
  </div>
</div>

## 🆘 Troubleshooting

<div class="troubleshooting">
  <details>
    <summary><strong>Bot not responding to commands?</strong></summary>
    <ul>
      <li>Check that your bot token is correct</li>
      <li>Ensure bot has proper permissions in your server</li>
      <li>Verify slash commands are synced: restart the bot</li>
      <li>Check bot logs for error messages</li>
    </ul>
  </details>

  <details>
    <summary><strong>Database connection failed?</strong></summary>
    <ul>
      <li>Verify MongoDB is running locally or cloud URI is correct</li>
      <li>Check network connectivity to database</li>
      <li>Ensure database credentials are valid</li>
      <li>Review connection timeout settings</li>
    </ul>
  </details>

  <details>
    <summary><strong>Dashboard not loading?</strong></summary>
    <ul>
      <li>Check that dashboard is enabled in config</li>
      <li>Verify port 8080 is not in use</li>
      <li>Ensure firewall allows local connections</li>
      <li>Try accessing via 127.0.0.1:8080 instead of localhost</li>
    </ul>
  </details>
</div>

## 📞 Need Help?

<div class="help-resources">
  <div class="help-item">
    <i class="fab fa-discord"></i>
    <div>
      <h4>Discord Community</h4>
      <p>Get real-time help from the community</p>
      <a href="https://discord.gg/pydiscobasepro">Join Discord</a>
    </div>
  </div>

  <div class="help-item">
    <i class="fab fa-github"></i>
    <div>
      <h4>GitHub Issues</h4>
      <p>Report bugs or request features</p>
      <a href="https://github.com/code-xon/pydiscobasepro/issues">Open Issue</a>
    </div>
  </div>

  <div class="help-item">
    <i class="fas fa-book"></i>
    <div>
      <h4>Documentation</h4>
      <p>Comprehensive guides and tutorials</p>
      <a href="api.html">Browse Docs</a>
    </div>
  </div>
</div>