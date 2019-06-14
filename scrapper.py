from torrequest import TorRequest
from bs4 import BeautifulSoup
import telepot

#telepot.api.set_proxy('https://163.172.153.156:3128')
bot = telepot.Bot('***BOT_TOKEN_GOES_HERE***')
tr=TorRequest(password='BLANK')
tr.reset_identity()

l1 = 'https://stackoverflow.com'
r = tr.get(l1 + '/questions/tagged/python/')

class DT_Getter():
    new_data = [] # create an empty list
    if r.status_code == 200:  # checking internet availability

        # creating the soup though the html.parser
        source = r.text
        soup = BeautifulSoup(source, 'html.parser')

        ''' .find_all() is a method that is used to search for all contents matching
            the specified parameters(tags). Tags are used to locate the desired content'''
        for summary in soup.find_all('div', class_='summary'):
            for title in summary('h3'):
                for link in title.find_all('a', class_='question-hyperlink'):
                    #add the scraped data to the list, while the condition still holds
                    while len(new_data) < 10:
                        new_data.append(l1 + link.get('href'))
                        break

        # open a text file and save the new scraped data
        with open('newD.txt', 'w') as f:
            for i in new_data:
                f.write('%s\n' % i)

class DT_Sender():
    username = '@pythonstackoverflowqns'    # telegram channel user_id

    # open files and strip them line by line
    oldln = open('old.txt').read().split('\n')
    newln = open('newD.txt').read().split('\n')

    updln = set(newln) - set(oldln)     # get the difference between files

    '''finding new lines which didn't exist int the old file send them to tg, 
    and update old.txt'''
    for ln in newln:
        if ln in updln:
            bot.sendMessage(username, ln.strip()) #sending to tg channel
            with open('old.txt', 'a') as fout:
                fout.write(ln.strip()+'\n') # updating data
            print('[+]', ln.strip())

if __name__ == '__main__':
    DT_Getter()
    DT_Sender()
