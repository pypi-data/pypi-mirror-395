from discord import Client, RawReactionActionEvent

from versecbot_interface.reaction import VersecbotReaction


async def process_reaction(reaction_event: RawReactionActionEvent, client: Client):
    """Convert a RawReactionActionEvent into a Reaction object."""
    channel = client.get_channel(reaction_event.channel_id)
    message = await channel.fetch_message(reaction_event.message_id)
    user = await channel.guild.fetch_member(reaction_event.user_id)
    emoji = reaction_event.emoji

    return VersecbotReaction(message=message, emoji=emoji, user=user)
