import os
import discord
from github import Github

# Set up your Discord bot
t = open("token", "r")
TOKEN = t.read()
intents = discord.Intents.all()
client = discord.Client(intents = intents)

# Set up your GitHub API
gt = open("github_pat", "r")
GITHUB_TOKEN = gt.read()
g = Github(GITHUB_TOKEN)

# Specify the repository you want to watch
REPO_OWNER = 'superbunytime'
REPO_NAME = 'discord-github-bot'
repo = g.get_repo(f'{REPO_OWNER}/{REPO_NAME}')

# Specify the Discord channel ID where you want to send the notifications
CHANNEL_ID = '775984233369960449' # bot-test server, bot-test channel

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

    # Get the latest commit hash
    latest_commit = repo.get_commits()[0].sha

    while True:
        try:
            # Check for new commits
            new_commits = repo.get_commits(since=latest_commit)
            if new_commits:
                # Send a notification to the Discord channel
                channel = client.get_channel(CHANNEL_ID)
                for commit in new_commits:
                    embed = discord.Embed(
                        title=f'New Commit in {REPO_NAME}',
                        description=commit.commit.message,
                        url=commit.html_url
                    )
                    embed.add_field(name='Author', value=commit.commit.author.name)
                    embed.add_field(name='Commit SHA', value=commit.sha)
                    await channel.send(embed=embed)
                latest_commit = new_commits[0].sha
        except Exception as e:
            print(f'Error checking for new commits: {e}')

        # Wait for a minute before checking again
        await client.wait_for('ready', timeout=60)

client.run(TOKEN)
