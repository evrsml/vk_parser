import redis
import logging

logging.basicConfig(level=logging.DEBUG,
                  format='%(asctime)s %(levelname)s %(message)s',
                  filename='app.log',
                  filemode='w')


'''класс для записи и чтения в редис'''
class RedisCheck:
    def __init__(self, host='localhost', port=6379, decode_responses=True):
        self.r = redis.Redis(host=host, port=port, decode_responses=decode_responses)

    def check_n_write(self,  key, value=None):
        try:
            if not self.r.exists(key):
                self.r.set(key, value, ex=86400)
                logging.info('Записали в базу: %s', key)
                #print(key,'Записал в базу')
                return False
            else:
                logging.info('Сообщение уже в базе: %s', key)
                #print(key, 'Сообщение уже в базе')
                return True
            
        except Exception as e:
            logging.error('Ошибка redis:', e)
            raise

rc = RedisCheck()








