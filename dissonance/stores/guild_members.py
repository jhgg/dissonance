from collections import defaultdict

from . import register, Store, handler, wait_for
from ..client import events
from ..models.guild import Member


@register('guild_members')
class GuildMemberStore(Store):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.guilds = defaultdict(dict)

    def get_members(self, guild_id):
        if guild_id in self.guilds:
            return self.guilds[guild_id]

        return {}

    def get_guild_member(self, guild_id, user_id):
        return self.get_members(guild_id).get(user_id)

    @handler(events.READY)
    @wait_for('channels', 'users')
    def handle_ready(self, ready_packet):
        for guild in ready_packet['guilds']:
            guild_id = int(guild['id'])
            guild_dict = self.guilds[guild_id]
            for member_data in guild['members']:
                member = Member(self._stores, member_data['user']['id'])
                member.update(member_data)
                guild_dict[member.id] = member
