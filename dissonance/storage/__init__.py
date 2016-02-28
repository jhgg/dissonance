from ..utils import importing


def get_store_by_name(name):
    if '.' not in name:
        name = 'dissonance.storage.%s.storage' % name

    return importing.import_dotted_path(name)