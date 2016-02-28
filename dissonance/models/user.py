class User(object):
    username = None
    discriminator = None
    avatar = None

    def __init__(self, stores, id):
        self._stores = stores
        self.id = int(id)

    def update(self, data):
        self.id = int(data.get('id', self.id))
        self.discriminator = int(data.get('discriminator', self.discriminator))
        self.username = data.get('username', self.username)
        self.avatar = data.get('avatar', self.avatar)

    def __repr__(self):
        return u'<User %s#%04i>' % (self.username, self.discriminator)
