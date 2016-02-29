from collections import defaultdict

from . import register, handler, Store
from ..client import events


@register('typing')
class TypingStore(Store):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.typing_users_by_channel = defaultdict(set)

    @handler(events.READY)
    def handle_ready(self, ready_packet):
        self.typing_users_by_channel = defaultdict(set)

    @handler(events.TYPING_START)
    def handle_typing_start(self, typing_event):
        self.client.call_later(None)
        pass

    @handler(events.TYPING_STOP)
    def handle_typing_stop(self, typing_event):
        pass

    @handler(events.MESSAGE_CREATE)
    def handle_message_create(self, message):
        pass

    def get_typing_users(self, channel_id):
        if channel_id in self.typing_users_by_channel:
            return self.typing_users_by_channel[channel_id]

        return set()

    def is_user_typing(self, channel_id, user_id):
        return user_id in self.get_typing_users(channel_id)
