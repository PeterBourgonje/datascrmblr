import os
import sys
import json
import random
from selenium import webdriver
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from apiclient.discovery import build
import nltk
import time
import codecs

DEV_API_KEY = '<DEV KEY HERE>'
FIREFOX_PROFILE = '<PATH TO FIREFOX PROFILE HERE>'
GECKO_PATH = '<PATH TO GECKO DRIVER HERE>'

#https://stackoverflow.com/questions/66209119/automation-google-login-with-python-and-selenium-shows-this-browser-or-app-may
profile = webdriver.FirefoxProfile(FIREFOX_PROFILE)
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.set_preference("media.volume_scale", "0.0") # mutes sound
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX

driver = webdriver.Firefox(executable_path=GECKO_PATH,
                           firefox_profile=profile,
                           desired_capabilities=desired)

yt = build('youtube', 'v3', developerKey=DEV_API_KEY)

def collect_urls(fp):
    
    terms = set()
    lines = codecs.open(fp).readlines()
    for line in lines:
        tokens = nltk.word_tokenize(line.lower())
        tags = nltk.pos_tag(tokens)
        for i in range(1, 5):
            for ngram in nltk.ngrams(tags, i):
                terms.add(' '.join([x[0] for x in ngram if len([y for y in ngram if y[1].startswith('N')]) == i])) # take only nouns/noun compounds
    
    search_terms = random.sample(list(terms), 20)
    vids = []
    for st in search_terms:
        search_response = yt.search().list(q=st, type="video", part="id,snippet").execute()
        for res in search_response.get('items', []):
            if res['id']['kind'] == 'youtube#video':
                vids.append(res['id']['videoId'])
    random.shuffle(vids)
    urls = []
    for vid in vids:
        url = 'https://www.youtube.com/watch?v=%s' % vid
        urls.append(url)
        
    return urls
    

def play_video(url):    
    
    driver.get(url)
    element = driver.find_element_by_id("player-container")
    element.click()


if __name__ == '__main__':

    if len(sys.argv) == 1:
        sys.stderr.write('Usage: youtubescrmblr.py <path to text file>\n')
        sys.exit(1)
    fp = sys.argv[1]
    
    sys.stderr.write('INFO: Collecting urls...\n')
    urls = collect_urls(fp)
    sys.stderr.write('INFO: Done.\n')
    
    try:
        while True:
            play_video(random.choice(urls))
            time.sleep(random.randint(300,1200))
    except KeyboardInterrupt:
        pass

    
