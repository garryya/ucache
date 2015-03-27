#!/usr/bin/python

class CacheNode:
    def __init__(self, key=None, data=None):
        self.key = key
        self.data = data
        self._next = None
        self._prev = None
    def __str__(self):
        return '%s' % self.key
    def __repr__(self):
        return '(%s,%s)' % (self.key,self.data)

def listiter(node):
    while node:
        yield node
        node = node._next

class UserCache:
    '''
    User cache implemented as doubly linked list
    '''
    def __init__(self, cache_limit):
        self._cache_length = 0
        self._cache_head = None
        self._cache_tail = None
        self._cache_limit = cache_limit

    def _update_head(self, node):
        if node == self._cache_head:
            return
        if node._next:
            node._next._prev = node._prev
        else:
            self._cache_tail = node._prev
        if node._prev:
            node._prev._next = node._next
        node._next = self._cache_head
        node._next._prev = node
        self._cache_head = node

    def find(self, key):
        '''
        Searches the cache for the key, updates list the list head if found
        :param key:
        :return:node data if found, else None
        '''
        for node in listiter(self._cache_head):
            if node.key == key:
                self._update_head(node)
                return node.data
        return None

    def _is_full(self):
        return self._cache_length >= self._cache_limit

    def add(self, key, data):
        node = CacheNode(key=key,data=data)
        node._next = self._cache_head
        if self._cache_head:
            self._cache_head._prev = node
        self._cache_head = node

        if not self._is_full():
            if self._cache_length == 1:
                self._cache_tail = self._cache_head
            self._cache_length += 1
        else:
            tail = self._cache_tail
            self._cache_tail = self._cache_tail._prev
            self._cache_tail._next = None
            del tail

    def __str__(self):
        s = 'cache: l=%d (%s) | ' % (self._cache_length,'full' if self._is_full() else 'not full')
        for node in listiter(self._cache_head):
            s = s + str(node) + ' '
        return s

    def __repr__(self):
        s = ''
        for node in listiter(self._cache_head):
            s += str(node)
        return s

class UserStore:

    def __init__(self, cache_limit, dbname='./ucache.dat'):
        self._dbname = dbname
        self._ucache = UserCache(cache_limit)
        self._userdb = {}
        with open(self._dbname) as f:
            for l in f:
                user_id, data = l.split('=')
                self._userdb[int(user_id)] = { v.split(':')[0].strip():v.split(':')[1].strip() for v in data.split(',') }

    def getUser(self, user_id):
        '''
        :param user_id: string
        :return: user data dictionary
        '''
        user_id = int(user_id)
        udata = self._ucache.find(user_id)
        if udata:
            return udata
        try:
            udata = self._userdb[user_id]
            self._ucache.add(user_id, udata)
            return udata
        except:
            pass
        return None

################################################

if __name__ == '__main__':
    ustore = UserStore(3)
    for u, ud in ustore._userdb.items():
        print u, ud


