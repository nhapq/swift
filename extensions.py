# -*- coding: utf-8 -*-

#from flask.ext.mongokit import MongoKit
#mdb = MongoKit()

from redis import Redis
redisdb0 = Redis( host='127.0.0.1', port=6379, db=0)
redisdb1 = Redis( host='127.0.0.1', port=6379, db=1)

