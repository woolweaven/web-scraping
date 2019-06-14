# Web Scraping
This is a simple python3 code for webscraping. Basically what the program does is channelling requests through tor and 
scrap for latest python-tagged questions [here](https://www.stackoverflow.com). Latest data is then sent to a telegram
channel via a bot. A scheduler which refreshes every 5 seconds manages the scrapper.py

 Python libraries used in web-scraping.

    BeautifulSoup
    TorRequest		
    Telepot	
    APScheduler		

**Setting up telegram bot:**

First of, you need to create a Telegram bot, if you haven't done this before its super easy you can look 
[at:](https://core.telegram.org/bots#6-botfather)
Take note of your bot token. The next thing is creating a public
channel on telegram, take note of the group @username. Now make the bot an administrator to the channel;
In any Telegram client:

    1. Open Channel info (in app title)
    2. Choose Administrators
    3. Add Administrator
    4. There will be no bots in contact list, so you need to search for it. Enter your bot's username
    5. Clicking on it you make it as administrator.

That's it with the bot creation, now the interesting part.

**Installing the required libraries:**

Clone this repository and when its done, navigate to the cloned directory through the terminal. Run the following
command to install all the required dependencies:
	
    pip3 install -r requirements.txt 

Now everything is set, only a few changes left.

**Scrapper.py**
    
    telepot.api.set_proxy() 
is used to set a proxy for your telegram-bot in case they are blocked in your region
otherwise you can comment it. For the proxy, you can google and grab anything of your choice, although private
proxies work great as well.

    bot = telepot.Bot('BOT_TOKEN') 
specifies your bot by taking your bot token generated earlier when you created a bot.
Bot token in in this syntax: 123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ.

    tr = TorRequest(password='BLANK') 
creates a tor request handler, unless you reconfigure tor, the password parameter 
should be left blank. 

    tr.reset_identity() 
creates a new hidden identity, ie assigns you a tor IP address.

    r = tr.get(l1 + '/questions/tagged/python/') 
is the  actual request made to stackoverflow.

I find it wise using the torrequest library as this keeps your identity hidden as
you scrape the site. But if you dont feel comfortable with it, request standard library all works fine with no flaws, 
the difference is that your real IP is exposed.


**DT_Fetcher()**

is responsible for making the scraping part. First a request is made, through looping around 
tags(html format), links to the questions are fetched. Note that at this point the link is not full. Which is why 
the link is concatinated with the l1 variable, for a complete working URL. The URLs are saved a list up until it 
gets to a length of 10. A with statement opens a text file *newD.txt*, then the contents of data are appended to the file.

**DT_Sender()**

compares the contents of *newD.txt* with those *old.txt*. Differences in the file represent new data, new data
is sent to the telegram channel and *old.txt* is updated.

The *Scheduler.py* is used to run the *scrapper.py*. This makes it almost possible to achieve real-time feed of questions 
being posted at any one moment.

Contributions are greatly appreciated. Hope you find this code useful.

**References and Resources:**

[article on TorRequest](https://www.scrapehero.com/make-anonymous-requests-using-tor-python/)

[Telepot Documentation](https://telepot.readthedocs.io/en/latest/)

[Making your bot channel admin](https://telmemeber.com/single/7/Make-telegram-bot-your-channel-admin)

[Free proxies](https://free-proxy-list.net/)

[BeautifulSoup4 Documentation](https://pypi.org/project/beautifulsoup4/)

[APScheduler Documentation](https://apscheduler.readthedocs.io/en/v3.6.0/userguide.html#code-examples)
