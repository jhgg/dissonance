class Role(object):
    id = None
    name = None
    color = None
    managed = None
    hoist = None
    position = None
    permissions = None

    def __init__(self, stores, id):
        self._stores = stores
        self.id = int(id)

    def update(self, role_data):
        self.name = role_data.get('name', self.name)
        self.color = int(role_data.get('color', self.color))
        self.managed = bool(role_data.get('managed', self.managed))
        self.hoist = bool(role_data.get('hoist', self.hoist))
        self.position = int(role_data.get('position', self.position))
        self.permissions = int(role_data.get('permissions', self.permissions))


class Member(object):
    deaf = None
    mute = None
    joined_at = None

    def __init__(self, stores, id):
        self._stores = stores
        self.id = int(id)

    def update(self, member_data):
        self.deaf = bool(member_data.get('deaf', self.deaf))
        self.mute = bool(member_data.get('mute', self.mute))
        self.joined_at = member_data.get('joined_at', self.joined_at)

    @property
    def user(self):
        return self._stores.users.with_id(self.id)

    def __repr__(self):
        return u'<GuildMember: %r>' % self.user


class Guild(object):
    afk_channel_id = None
    splash = None
    roles = None
    name = None
    voice_states = None
    large = None
    verification_level = None
    member_count = None
    region = None
    joined_at = None
    icon = None
    features = None
    emojis = None
    members = None
    afk_timeout = None
    channels = None
    owner_id = None
    presences = None
    id = None

    def __init__(self, id, channels, **kwargs):
        self.id = int(id)
        self.channels = channels
        self.__dict__.update(kwargs)

    @classmethod
    def from_ready_packet(cls, stores, **kwargs):
        kwargs['roles'] = Guild.parse_roles(stores, kwargs['roles'])
        kwargs['channels'] = stores.channels.in_bulk(c['id'] for c in kwargs['channels'])
        return Guild(**kwargs)

    def __repr__(self):
        return u'<Guild %s (%s)>' % (self.name, self.id)

    @classmethod
    def parse_members(cls, stores, roles, members):
        member_dict = {}
        users = stores.users

        for member in members:
            print(member['user']['id'])
            member['user'] = users.with_id(member['user']['id'])
            member['roles'] = filter(None, (roles.get(int(r)) for r in member['roles']))
            member = Member(stores, member['user']['id'])
            member_dict[member.id] = member

        return member_dict

    @classmethod
    def parse_roles(cls, stores, roles):
        role_dict = {}
        for role_data in roles:
            role = Role(stores, role_data['id'])
            role.update(role_data)
            role_dict[role.id] = role

        return role_dict
