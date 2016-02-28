from collections import defaultdict, deque

from ..models.message import Message
from ..client import events
from . import register, handler, wait_for, ObjectHolder


@register('messages')
class MessageStore(ObjectHolder):
    object_class = Message

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._messages = defaultdict(lambda: deque(maxlen=50))

    @handler(events.MESSAGE_CREATE)
    @wait_for('users')
    def handle_message_create(self, message_data):
        message = self.upsert(message_data)
        self._messages[message.channel_id].append(message)

    def make_object(self, data):
        # noinspection PyCallingNonCallable
        return self.object_class(self._stores, data['id'], data['channel_id'])
