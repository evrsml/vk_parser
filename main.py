from googleAPI import values
import time
from parser_logic import user_link_parse


'''входная точка приложения'''
def link_grabber(links):

    while True:
        for link in links:
            if link:
                user_link_parse(link)
                time.sleep(3)
            else:
                 pass

link_grabber(values)



















