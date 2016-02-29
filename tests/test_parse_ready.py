from dissonance.models.channel import VoiceChannel, TextChannel
from tests.utils import dummy_stores, load_packet
from dissonance.client.events import READY
import pytest


@pytest.fixture(scope="module")
def ready_store():
    stores = dummy_stores()
    assert stores.dispatcher.dispatch(READY, load_packet('ready')) == 0
    return stores


def test_ready_parse_guild(ready_store):
    assert len(ready_store.guilds) == 1

    g = ready_store.guilds.find_one()
    assert g.name == 'test server'
    assert set(g.channels.keys()) == {153648966053920768, 153648966053920769}


def test_ready_parse_channels(ready_store):
    assert len(ready_store.channels) == 2

    voice_channel = ready_store.channels.with_id(153648966053920769)
    text_channel = ready_store.channels.with_id(153648966053920768)

    assert isinstance(voice_channel, VoiceChannel)
    assert isinstance(text_channel, TextChannel)


def test_parse_users(ready_store):
    assert len(ready_store.users) == 1
    user = ready_store.users.with_id(153648786160353280)
    assert user.id == 153648786160353280
    assert user.username == 'Bot Test'
    assert user.discriminator == 7751
    assert user.avatar == 'avatar'


