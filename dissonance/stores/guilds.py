from . import register, ObjectHolder, handler, wait_for
from ..client import events
from ..models.guild import Guild


@register('guilds')
class GuildStore(ObjectHolder):
    object_class = Guild

    @handler(events.READY)
    @wait_for('channels', 'users')
    def handle_ready(self, ready_packet):
        for guild in ready_packet['guilds']:
            self.add(Guild.from_ready_packet(self._stores, **guild))
            print('pg', guild)

    def add(self, guild):
        self._objects[guild.id] = guild

    def __repr__(self):
        return u'Guilds[%s]' % (', '.join(repr(g) for g in self._objects.values()))
