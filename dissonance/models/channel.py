class BaseChannel(object):
    guild_id = None
    id = None
    name = None

    def __init__(self, stores, id, guild_id):
        self._stores = stores
        self.id = int(id)
        self.guild_id = int(guild_id)

    def update(self, data):
        self.name = data.get('name', self.name)

    @property
    def guild(self):
        return self._stores.guilds.with_id(self.guild_id)

    def __repr__(self):
        return u'<Channel %s in %r>' % (self.name, self.guild)


class TextChannel(BaseChannel):
    pass


class VoiceChannel(BaseChannel):
    pass
