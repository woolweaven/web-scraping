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
    collected_data = [] # create an empty list
    if response_data.status_code == 200:  # checking internet availability

        # creating the soup though the html.parser
        data_source = response_data.text
        bs_soup = BeautifulSoup(data_source, 'html.parser')

        # matching tags with 'div tag'
        for question_summary in bs_soup.find_all('div', class_='summary'):
            for question_title in question_summary('h3'):
                for question_link in question_title.find_all('a', class_='question-hyperlink'):

                    # collect data from data_source.
                    while len(collected_data) < 10:
                        collected_data.append(request_string + question_link.get('href'))
                        break

        # save newly collected data.
        with open('updated_file.txt', 'w') as updated_file:
            for data_chuck in collected_data:
                updated_file.write(f'{data_chuck}\n')

class DT_Sender():
    chat_id = credentials['chat_id']   # telegram channel chat_id

    # open files and strip them line by line
    database = open('database.txt').read().split('\n')
    update_database = open('updated_file.txt').read().split('\n')

    # get the difference between files
    update_data = set(update_database) - set(database)     

    # updating the database by new data.
    data_tosend = []
    for index, data_chuck in enumerate(update_database):
        if data_chuck in update_data:

            # sending to telegram channel
            print('---> updating the database.')
            data_tosend.append(f'{index}.   {data_chuck} \n\n') 

            with open('database.txt', 'a') as database_file:
                database_file.write(data_chuck.strip()+'\n') # updating data

            print(f'{data_chuck.strip()}')

    if data_tosend:
        bot.sendMessage(chat_id=chat_id, text=''.join(data_tosend))

if __name__ == '__main__':
    DT_Getter()
    DT_Sender()
