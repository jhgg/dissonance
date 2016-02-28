from gevent.monkey import patch_all

patch_all()
from functools import partial
from dissonance.client import Client
from credentials import EMAIL, PASSWORD

client = Client() \
    .start_debug_manhole(9001) \
    .login(EMAIL, PASSWORD) \
    .connect()


@partial(client.events.on, 'message-create')
def on_message_create(client, message):
    if message.author == client.me:
        return

    print('omc', message)
    # if 'doot' in message.content:
    #     client.api_client.create_message(message.channel_id, 'doot doot')
    if 'doot mcount' in message.content:
        client.api_client.create_message(message.channel_id, 'doot doot i am storing %s messages' % len(client.stores.messages))


@partial(client.events.on, 'ready')
def on_ready(client, **kwargs):
    print('connected')
    print('parsed %i guilds' % len(client.stores.guilds))
    print('parsed %i channels' % len(client.stores.channels))
    print('parsed %i users' % len(client.stores.users))
    print('i am', client.me)

client.join()
