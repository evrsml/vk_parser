from googleAPI import values
import time
from parser_logic import user_link_parse

def link_grabber(links):

    while True:
        for link in links:
            if link:
                user_link_parse(link)
                time.sleep(2)
            else:
                 pass

showq = link_grabber(values)

print(showq)

















