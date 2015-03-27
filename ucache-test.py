#!/usr/bin/python
import sys
from ucache import UserStore

if len(sys.argv) <= 1:
    print 'No cache size specified'
    sys.exit(1)

cache_size = int(sys.argv[1])
ustore = UserStore(cache_size)

user_test_set0 = (
                    ('1',{'found':True,'cache':'1'}),
                    ('2',{'found':False,'cache':'21'}),
                    ('3',{'found':True,'cache':'321'}),
                    ('2',{'found':True,'cache':'231'}),
                    ('1',{'found':True,'cache':'123'}),
                    ('4',{'found':True,'cache':'412'}),
                )

user_test_set1 = (
                    ('1',{'found':True,'cache':'1'}),
                    ('99',{'found':False,'cache':'1'}),
                    ('2',{'found':True,'cache':'21'}),
                    ('2',{'found':True,'cache':'21'}),
                    ('1',{'found':True,'cache':'12'}),
                    ('5',{'found':True,'cache':'512'}),
                    ('1',{'found':True,'cache':'152'}),
                    ('6',{'found':True,'cache':'615'}),
                    ('6',{'found':True,'cache':'615'}),
                    ('99',{'found':False,'cache':'615'}),
                )

def test(test_set):
    for user_id, expected in test_set:
        udata = ustore.getUser(user_id)
        cache = '%r' % ustore._ucache
        passed = (udata or not expected['found']) and expected['cache'] == cache
        print user_id, ':', '' if passed else 'NOT', 'passed | user data:', udata
        print ustore._ucache
        print '***'

test(user_test_set0)
#test(user_test_set1)
