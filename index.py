#
# Weather Bot for Twitter
# Created by: Sean Kohler
#

from bs4 import BeautifulSoup
from selenium import webdriver
from credentials import twitter_keys #Credentials for my twitter account
from website import ws
import tweepy
import time

#
# Paste the website you wish to get data from
#

website = ws #imported from file to protect my location Ex. 'http://weather_url'

while True:
    driver = webdriver.Chrome("chromedriver.exe")
    temp = []
    driver.get(website)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    #
    # Get the closest tag to the data and the associated class (URL Specific)
    #

    finstr = ''
    ltags = soup.find_all('div', class_='wob_loc mfMhoc')  # Location
    tags = soup.find_all('span', class_='wob_t TVtOme')  # Temperature
    ptags = soup.find_all('div', class_='wtsRwe')  # Precipitation, Humidity Chance, Wind Speeds
    dtags = soup.find_all('div', class_='wob_dts')  # Date & Time
    for dtag in dtags:
        finstr = dtag.text
    for tag in tags:
        finstr += tag.text+"°F "
        for ltag in ltags:
            finstr += ltag.text+""
            for ptag in ptags:
                finstr += ptag.text+" "
                #
                # Now Write it to a file
                #
    f = open("weather.txt", "w")
    f.write(finstr)
    f.close()
    f = open("weather.txt", "r")
    print(f.read())
    driver.close()

    #
    # Now log into twitter
    #
    twitter_auth_keys = twitter_keys #Credentials from other file

    auth = tweepy.OAuthHandler(
        twitter_auth_keys['consumer_key'],
        twitter_auth_keys['consumer_secret']
    )
    auth.set_access_token(
        twitter_auth_keys['access_token'],
        twitter_auth_keys['access_token_secret']
    )
    api = tweepy.API(auth)

    #
    # Now format Results and Tweet
    #

    f = open("weather.txt", "r")
    tweet = f.read()
    f.close()
    word = ''
    for c in tweet:
        if c == '�': #Degrees symbol gets lost when transfering from file
            word += '°'
        else:
            word += c
            leng = word.__len__()
            if leng > 3:
                if c == 'Y' or c == '%' or c == 'M': #Bad way of formatting
                    word += '\n'
                elif c == 'h':
                    word += ' , '
    i = 0
    finstring = ''
    print(word.__len__())
    for x in word:
        if i < 85:
            finstring += x
            i = i+1

    print(finstring)
    status = api.update_status(status=word)
    time.sleep(3595)
