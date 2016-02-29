import json
import os.path
from unittest.mock import patch
from copy import deepcopy


@patch('dissonance.client.Client')
def dummy_stores(Client):
    from dissonance.stores import Stores, autodiscover
    autodiscover()

    return Stores(Client())


_cached_packets = {}


def load_packet(packet_type):
    if packet_type in _cached_packets:
        return deepcopy(_cached_packets[packet_type])

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'packets', '%s.json' % packet_type)
    with open(path) as fp:
        packet = json.load(fp)
        _cached_packets[packet_type] = packet
        return deepcopy(packet)
