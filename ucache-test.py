#!/usr/bin/python

from ucache import getUser

user_test_set1 = {
                    'user1':True,
                    'user2':True,
                    'user3':False,
                    'admin':True,
                    }

for u, expected in user_test_set1.items():
    udata = getUser(u)
    print u, '=', udata, '/', 'passed' if udata or not expected else 'NOT passed'


