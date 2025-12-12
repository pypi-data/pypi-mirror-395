from aiohttp import web
import json
from datetime import datetime

class Dashboard:
    def __init__(self, bot, database, config):
        self.bot = bot
        self.database = database
        self.config = config
        self.app = web.Application()
        self.start_time = datetime.now()
        self.setup_routes()

    def setup_routes(self):
        self.app.router.add_get('/', self.index)
        self.app.router.add_get('/stats', self.stats)
        self.app.router.add_static('/static', 'static')  # For future static files

    async def index(self, request):
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PyDiscoBasePro Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }}

        .header h1 {{
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
        }}

        .stat-icon {{
            font-size: 3rem;
            margin-bottom: 15px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .stat-number {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}

        .stat-label {{
            font-size: 1.1rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .charts {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .chart-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }}

        .chart-card h3 {{
            margin-bottom: 20px;
            color: #333;
            text-align: center;
        }}

        .chart-placeholder {{
            height: 200px;
            background: linear-gradient(45deg, #f0f0f0, #e0e0e0);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #666;
            font-style: italic;
        }}

        .recent-activity {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }}

        .activity-list {{
            list-style: none;
        }}

        .activity-item {{
            padding: 15px 0;
            border-bottom: 1px solid #eee;
            display: flex;
            align-items: center;
        }}

        .activity-item:last-child {{
            border-bottom: none;
        }}

        .activity-icon {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(45deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            margin-right: 15px;
        }}

        .activity-content {{
            flex: 1;
        }}

        .activity-content h4 {{
            margin-bottom: 5px;
            color: #333;
        }}

        .activity-content p {{
            color: #666;
            font-size: 0.9rem;
        }}

        .footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}

            .stats-grid {{
                grid-template-columns: 1fr;
            }}

            .charts {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-chart-line"></i> PyDiscoBasePro Dashboard</h1>
            <p>Real-time bot monitoring and analytics</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-server"></i></div>
                <div class="stat-number" id="guilds-count">0</div>
                <div class="stat-label">Guilds</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-users"></i></div>
                <div class="stat-number" id="users-count">0</div>
                <div class="stat-label">Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-terminal"></i></div>
                <div class="stat-number" id="commands-count">0</div>
                <div class="stat-label">Commands</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-clock"></i></div>
                <div class="stat-number" id="uptime">0s</div>
                <div class="stat-label">Uptime</div>
            </div>
        </div>

        <div class="charts">
            <div class="chart-card">
                <h3><i class="fas fa-chart-bar"></i> Command Usage</h3>
                <div class="chart-placeholder">
                    Chart visualization coming soon...
                </div>
            </div>
            <div class="chart-card">
                <h3><i class="fas fa-chart-pie"></i> Guild Distribution</h3>
                <div class="chart-placeholder">
                    Chart visualization coming soon...
                </div>
            </div>
        </div>

        <div class="recent-activity">
            <h3><i class="fas fa-history"></i> Recent Activity</h3>
            <ul class="activity-list" id="activity-list">
                <li class="activity-item">
                    <div class="activity-icon"><i class="fas fa-play"></i></div>
                    <div class="activity-content">
                        <h4>Bot Started</h4>
                        <p>Dashboard initialized and monitoring active</p>
                    </div>
                </li>
            </ul>
        </div>

        <div class="footer">
            <p>&copy; 2024 PyDiscoBasePro v2. Made with ❤️ by Code-Xon</p>
        </div>
    </div>

    <script>
        async function updateStats() {{
            try {{
                const response = await fetch('/stats');
                const stats = await response.json();

                document.getElementById('guilds-count').textContent = stats.guilds;
                document.getElementById('users-count').textContent = stats.users;
                document.getElementById('commands-count').textContent = stats.commands;
                document.getElementById('uptime').textContent = stats.uptime;
            }} catch (error) {{
                console.error('Failed to fetch stats:', error);
            }}
        }}

        // Update stats every 5 seconds
        updateStats();
        setInterval(updateStats, 5000);

        // Add some sample activity
        function addActivity(icon, title, description) {{
            const activityList = document.getElementById('activity-list');
            const li = document.createElement('li');
            li.className = 'activity-item';
            li.innerHTML = `
                <div class="activity-icon"><i class="fas fa-${{icon}}"></i></div>
                <div class="activity-content">
                    <h4>${{title}}</h4>
                    <p>${{description}}</p>
                </div>
            `;
            activityList.insertBefore(li, activityList.firstChild);
        }}

        // Simulate some activity
        setTimeout(() => addActivity('user-plus', 'New User', 'A new user joined a guild'), 3000);
        setTimeout(() => addActivity('terminal', 'Command Executed', 'Someone used the ping command'), 6000);
    </script>
</body>
</html>
        """
        return web.Response(text=html, content_type='text/html')

    async def stats(self, request):
        uptime = datetime.now() - self.start_time
        stats = {
            "guilds": len(self.bot.guilds),
            "users": sum(guild.member_count for guild in self.bot.guilds if guild.member_count),
            "commands": len(self.bot.commands) if hasattr(self.bot, 'commands') else 0,
            "uptime": f"{uptime.seconds}s"
        }
        return web.json_response(stats)

    async def run(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.config["host"], self.config["port"])
        await site.start()
        print(f"🚀 Dashboard running on http://{self.config['host']}:{self.config['port']}")