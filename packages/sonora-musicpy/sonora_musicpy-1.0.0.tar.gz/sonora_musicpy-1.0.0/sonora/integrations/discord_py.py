"""Discord.py integration for Sonora."""

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    import discord
    from ..client import SonoraClient

class DiscordPyIntegration:
    """Integration for discord.py."""

    def __init__(self, bot, sonora_client: "SonoraClient"):
        self.bot = bot
        self.sonora = sonora_client
        self._voice_states: Dict[int, Dict[str, Any]] = {}
        self._voice_servers: Dict[int, Dict[str, Any]] = {}

    def attach(self):
        """Attach event listeners to the bot."""
        self.bot.add_listener(self.on_voice_state_update, 'on_voice_state_update')
        self.bot.add_listener(self.on_voice_server_update, 'on_voice_server_update')

    async def on_voice_state_update(self, member: "discord.Member", before: "discord.VoiceState", after: "discord.VoiceState"):
        """Handle voice state updates."""
        if member.id != self.bot.user.id:
            return

        guild_id = member.guild.id
        self._voice_states[guild_id] = {
            'channel_id': after.channel.id if after.channel else None,
            'session_id': after.session_id
        }

        # Check if we have both voice state and server update
        if guild_id in self._voice_servers:
            await self._connect_voice(guild_id)

    async def on_voice_server_update(self, guild: "discord.Guild", endpoint: str, token: str):
        """Handle voice server updates."""
        guild_id = guild.id
        self._voice_servers[guild_id] = {
            'endpoint': endpoint,
            'token': token
        }

        # Check if we have both voice state and server update
        if guild_id in self._voice_states:
            await self._connect_voice(guild_id)

    async def _connect_voice(self, guild_id: int):
        """Connect to voice channel."""
        state = self._voice_states[guild_id]
        server = self._voice_servers[guild_id]

        if state['channel_id'] and state['session_id']:
            player = await self.sonora.get_player(guild_id)
            await player.connect(state['channel_id'], state['session_id'], server['token'])

        # Clean up
        self._voice_states.pop(guild_id, None)
        self._voice_servers.pop(guild_id, None)