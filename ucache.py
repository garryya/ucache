#!/usr/bin/python

class UserCache:
    def __init__(self):
        pass
    def get(self, uname):
        return None
    def update(self, uname, udata):
        pass

class UserStore:

    def __init__(self, dbname='./ucache.dat'):
        self._dbname = dbname
        self._ucache = UserCache()
        self._userdb = {}
        with open(self._dbname) as f:
            for l in f:
                user, data = l.split('=')
                self._userdb[user] = { v.split(':')[0].strip():v.split(':')[1].strip() for v in data.split(',') }

    def getUser(self, uname):
        udata = self._ucache.get(uname)
        if udata:
            return udata
        try:
            udata = self._userdb[uname]
            self._ucache.update(uname, udata)
            return udata
        except:
            pass
        return None


def getUser(uname):
    return UserStore().getUser(uname)

if __name__ == '__main__':
    ustore = UserStore()
    for u, ud in ustore._userdb.items():
        print u, ud


