from stem import response
from torrequest import TorRequest
from bs4 import BeautifulSoup
import telepot
import json


#Loading credentials.
credentials = {}
with open('credentials.json', 'r') as credentials_file:
    credentials = json.load(credentials_file)


#telepot.api.set_proxy('https://163.172.153.156:3128')

# Creating the bot. 
TOKEN = credentials['bot_token']
bot = telepot.Bot(token=TOKEN)

# Creating tor object.
PASSWORD = credentials['tor_password']
tor_request = TorRequest(password=PASSWORD)
tor_request.reset_identity()

#creating the request.
request_string = 'https://stackoverflow.com'
response_data = tor_request.get(request_string + '/questions/tagged/python/')


class DT_Getter():
    new_data = [] # create an empty list
    if response_data.status_code == 200:  # checking internet availability

        # creating the soup though the html.parser
        source = response_data.text
        soup = BeautifulSoup(source, 'html.parser')

        ''' .find_all() is a method that is used to search for all contents matching
            the specified parameters(tags). Tags are used to locate the desired content'''
        for summary in soup.find_all('div', class_='summary'):
            for title in summary('h3'):
                for link in title.find_all('a', class_='question-hyperlink'):
                    #add the scraped data to the list, while the condition still holds
                    while len(new_data) < 10:
                        new_data.append(request_string + link.get('href'))
                        break

        # open a text file and save the new scraped data
        with open('newD.txt', 'w') as f:
            for i in new_data:
                f.write('%s\n' % i)

class DT_Sender():
    chat_id = credentials['chat_id']   # telegram channel chat_id

    # open files and strip them line by line
    oldln = open('old.txt').read().split('\n')
    newln = open('newD.txt').read().split('\n')

    updln = set(newln) - set(oldln)     # get the difference between files

    '''finding new lines which didn't exist int the old file send them to tg, 
    and update old.txt'''
    for ln in newln:
        if ln in updln:
            print('---> sending sms...')
            bot.sendMessage(chat_id=chat_id, text='hi') #sending to tg channel
            with open('old.txt', 'a') as fout:
                fout.write(ln.strip()+'\n') # updating data
            print('[+]', ln.strip())


if __name__ == '__main__':
    DT_Getter()
    DT_Sender()
