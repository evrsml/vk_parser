import redis

'''класс для записи и чтения в редис'''
class RedisCheck:
    def __init__(self, host='localhost', port=6379, decode_responses=True):
        self.r = redis.Redis(host=host, port=port, decode_responses=decode_responses)

    def check_n_write(self, hash, key, value=None):
        if not self.r.hexists(hash, key):
            self.r.hset(hash, key, value)
            self.r.expire(key, 86400)
            #print('В базе данных сообщения нет, записал!')
            return False
        else:
            #print('Сообщение уже в базе')
            return True

rc = RedisCheck()


