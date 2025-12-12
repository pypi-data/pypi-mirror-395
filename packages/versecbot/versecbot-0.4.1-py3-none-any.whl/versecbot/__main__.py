from importlib.metadata import entry_points
from logging import getLogger, StreamHandler
from os import getenv

from discord import Message, RawReactionActionEvent
from versecbot_interface import PluginRegistry, Plugin

from versecbot.client import discord_client
from versecbot.settings import get_settings
from versecbot.util import process_reaction

logging_level = getenv("VERSECBOT_LOG_LEVEL", "INFO")
logger = getLogger("discord").getChild("versecbot")

registry = PluginRegistry()

all_intents = set()
discovered_plugins = entry_points(group="versecbot.plugins")
for plugin in discovered_plugins:
    logger.info(f"Discovered plugin: {plugin.name}")
    loaded: Plugin = plugin.load()
    for intent in loaded.intents:
        all_intents.add(intent)

    registry.register(loaded)

settings = get_settings()

discord_client.initialize(all_intents)
client = discord_client.client


@client.event
async def on_ready():
    logger.info(f"We have logged in as {client.user}")
    logger.info("Initializing plugins...")
    logger.debug("Plugins to register: %s", ", ".join(registry.plugins.keys()))

    for plugin in registry.plugins.values():
        logger.debug("Loading settings for plugin: %s", plugin.name)
        plugin_settings = settings.plugins.get(plugin.name)
        if plugin_settings is None:
            logger.warning(
                f"Plugin {plugin.name} is not configured. It will not be initialized. Add a section to the config file to enable it."
            )
            continue

        logger.debug("Initializing plugin: %s", plugin.name)
        plugin.initialize(settings.plugins[plugin.name], client)


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    for plugin in registry.plugins.values():
        for hook in plugin.get_message_watchers():
            if hook.should_act(message):
                await hook.act(message)


@client.event
async def on_raw_reaction_add(reaction_event: RawReactionActionEvent):
    logger.debug("Reaction being processed...")

    user = client.get_user(reaction_event.user_id)
    if user == client.user:
        return

    reaction = await process_reaction(reaction_event, client)

    for plugin in registry.plugins.values():
        for hook in plugin.get_reaction_watchers():
            logger.debug("Reaction being processed by %s", hook.name)
            if hook.should_act(reaction):
                await hook.act(reaction)


client.run(
    token=settings.api_token, log_handler=StreamHandler(), log_level=logging_level
)
