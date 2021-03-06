from ..models.user import User
from ..client import events
from . import register, handler, ObjectHolder


@register('users')
class UserStore(ObjectHolder):
    object_class = User

    @handler(events.READY)
    def handle_ready(self, ready_packet):
        for guild in ready_packet['guilds']:
            for member in guild['members']:
                self.upsert(member['user'])

        self.upsert(ready_packet['user'])

    @handler(events.MESSAGE_CREATE, events.MESSAGE_UPDATE)
    def handle_message(self, message_data):
        if 'author' in message_data:
            self.upsert(message_data['author'])
