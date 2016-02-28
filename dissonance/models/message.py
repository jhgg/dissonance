class Message(object):
    attachments = None
    author_id = None
    content = None
    mentions = None
    embeds = None
    mention_everyone = None
    timestamp = None
    edited_timestamp = None

    def __init__(self, stores, id, channel_id):
        self._stores = stores
        self.id = int(id)
        self.channel_id = int(channel_id)

    @property
    def channel(self):
        return self._stores.channels.with_id(self.channel_id)

    @property
    def author(self):
        return self._stores.users.with_id(self.author_id)

    def update(self, message_data):
        self.content = message_data.get('content', self.content)
        self.mentions = message_data.get('mentions', self.mentions)
        self.mention_everyone = bool(message_data.get('mention_everyone', self.mention_everyone))
        self.embeds = message_data.get('embeds', self.embeds)
        self.edited_timestamp = message_data.get('edited_timestamp', self.edited_timestamp)
        self.timestamp = message_data.get('timestamp', self.timestamp)

        if 'author' in message_data:
            self.author_id = int(message_data['author']['id'])

    def __repr__(self):
        return u'<Message author: %r, channel: %r, content: %r>' % (self.author, self.channel, self.content)
