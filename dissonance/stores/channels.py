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

    @handler(events.CHANNEL_CREATE, events.CHANNEL_UPDATE)
    def handle_channel_create_or_update(self, channel):
        self.upsert(channel)

    @handler(events.GUILD_CREATE)
    def handle_guild_create(self, guild):
        for channel in guild['channels']:
            channel['guild_id'] = guild['id']
            self.upsert(channel)

    @handler(events.GUILD_DELETE)
    def handle_guild_create(self, guild):
        guild_id = guild['id']
        for channel_id, channel in list(self.items()):
            if channel.guild_id == guild_id:
                self.delete(channel.id)

    @handler(events.CHANNEL_DELETE)
    def handle_channel_delete(self, channel):
        self.delete(channel)

    def make_object(self, data):
        type = data['type']
        id = data['id']
        guild_id = data['guild_id']

        if type == 'text':
            return TextChannel(self._stores, id, guild_id)

        elif type == 'voice':
            return VoiceChannel(self._stores, id, guild_id)