import os
import discord
import asyncio
from github import Github
from discord.ext import tasks

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
    github_check.start()

@tasks.loop(seconds = 60)
async def github_check():

    # Get the latest commit hash
    latest_commit = repo.get_commits()[0].sha

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
    
    print("good excuse for a git commit test")



with open("token", "r+") as keyfile:
    key = keyfile.read()
    client.run(key)
    
# print("okay that isn't working")

