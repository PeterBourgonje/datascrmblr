import os
import sys
import json
import random
from selenium import webdriver
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from apiclient.discovery import build

DEV_API_KEY = '<API key here>'
FIREFOX_PROFILE = '<Firefox profile here>'
GECKO_PATH = '<Gecko path here>'

yt = build('youtube', 'v3', developerKey=DEV_API_KEY)

search_response = yt.search().list(q='aapjes', type="video", part="id,snippet").execute()

vids = []
for res in search_response.get('items', []):
    if res['id']['kind'] == 'youtube#video':
        vids.append(res['id']['videoId'])

url = 'https://www.youtube.com/watch?v=%s' % random.choice(vids)

# TODO: collect a bunch of vid urls, perhaps detached from this script (or at least wait a while before watching that exact video...)
    
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

#driver.get('https://www.youtube.com/watch?v=NUC2EQvdzmY&list=RD8Q95z8ObgF8&index=6')
driver.get(url)
element = driver.find_element_by_id("player-container")
element.click()
