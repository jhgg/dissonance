from . import register, ObjectHolder, handler
from ..client import events
from ..models.channel import TextChannel, VoiceChannel


@register('channels')
class ChannelStore(ObjectHolder):
    @handler(events.READY)
    def handle_ready(self, ready_packet):
        for guild in ready_packet['guilds']:
            for channel in guild['channels']:
                channel['guild_id'] = guild['id']
                self.upsert(channel)

    def make_object(self, data):
        type = data['type']
        id = data['id']
        guild_id = data['guild_id']

        if type == 'text':
            return TextChannel(self._stores, id, guild_id)

        elif type == 'voice':
            return VoiceChannel(self._stores, id, guild_id)
