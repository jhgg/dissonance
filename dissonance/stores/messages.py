from collections import defaultdict, deque

from ..models.message import Message
from ..client import events
from . import register, handler, wait_for, ObjectHolder


@register('messages')
class MessageStore(ObjectHolder):
    object_class = Message
    weak = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._messages = defaultdict(lambda: deque(maxlen=50))

    @handler(events.MESSAGE_CREATE)
    @wait_for('users')
    def handle_message_create(self, message_data):
        message = self.upsert(message_data)
        print(self._objects)
        self._messages[message.channel_id].append(message)

    @handler(events.MESSAGE_UPDATE)
    @wait_for('users')
    def handle_message_update(self, message_data):
        self.update(message_data)

    def make_object(self, data):
        # noinspection PyCallingNonCallable
        return self.object_class(self._stores, data['id'], data['channel_id'])

    def get_recent_channel_messages(self, channel_id):
        if channel_id in self._messages:
            return self._messages[channel_id]

        return []
