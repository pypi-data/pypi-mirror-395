import discord


class DiscordClient:
    def __init__(self):
        self.client = None

    def initialize(self, plugin_intents):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        self.client = discord.Client(intents=intents)


discord_client = DiscordClient()
