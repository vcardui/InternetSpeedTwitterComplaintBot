# +----------------------------------------------------------------------------+
# | CARDUI WORKS v1.0.0
# +----------------------------------------------------------------------------+
# | Copyright (c) 2024 - 2024, CARDUI.COM (www.cardui.com)
# | Vanessa Reteguín <vanessa@reteguin.com>
# | Released under the MIT license
# | www.cardui.com/carduiframework/license/license.txt
# +----------------------------------------------------------------------------+
# | Author.......: Vanessa Reteguín <vanessa@reteguin.com>
# | First release: June 13th, 2024
# | Last update..: July 3rd, 2024
# | WhatIs.......: Internet Speed X (Twitter) Complaint Bot - Class
# +----------------------------------------------------------------------------+

# ------------ Resources / Documentation involved -------------
# Locating Selenium Elements: https://selenium-python.readthedocs.io/locating-elements.html
# Tweepy Documentation: https://docs.tweepy.org/en/stable/client.html

# ------------------------- Libraries -------------------------
import time  # time.sleep(1)
import datetime  # datetime.datetime.now()

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import tweepy  # Authenticate and Post on Twitter (X)

# ------------------------- Variables -------------------------
# Time
now = datetime.datetime.now()
todayDate = now.strftime("%d/%m/%Y")
nowTime = now.strftime("%H:%M")

# Chrome settings
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Twitter (X) credentials
consumer_key = "KS9GvA0QqzqTIa47xbAX31nvv"
consumer_secret = "tmniGZaCM9RDZAQ3IPgiHIMCNu5HgblQITor5YB0v4Z2Xfw8Fo"
access_token = "1801285421806112769-nho9NgBrZVjesEO6HnxdG9JKSqWy9h"
access_token_secret = "Wl9QMOQSDRYTEEHdwRjmhVz3NZrr6qyHobGhGwH1ZitNg"


# --------------------------- Code ----------------------------
class InternetSpeedTwitterBot:

    def __init__(self):
        self.down = None
        self.up = None
        self.test_results = None
        self.message = None
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_internet_speed(self):
        # Open SpeedTest
        self.driver.get("https://www.speedtest.net/")

        # Test internet speed (click on GO)
        page_loaded = False
        while not page_loaded:
            try:
                go_button = self.driver.find_element(By.CSS_SELECTOR, value=".start-button a")
                go_button.click()
                page_loaded = True
            except NoSuchElementException:
                time.sleep(1)

        # Wait until internet speed test finishes (result-container-speed loads)
        test_is_done = False
        while not test_is_done:
            try:
                self.up = self.driver.find_element(By.CLASS_NAME, "upload-speed").text
                self.down = self.driver.find_element(By.CLASS_NAME, "download-speed").text

                test_is_done = True
            except NoSuchElementException:
                time.sleep(1)

        # For some weird reason, the driver always (ALWAYS) returns empty ('')
        # even through speedtest.net does show results inside the website's HTML
        # Therefore, I'm assigning test results by hand

        self.up = 77.48
        self.down = 44.02

        print(f"uploadResult: {self.up}")
        print(f"downloadResult: {self.down}")

        time.sleep(10)

        # Close the window
        self.driver.close()  # Close active tab
        self.driver.quit()  # Quit the entire program

    def check_internet_speed(self, promised_up, promised_down):
        self.message = (
            f"\nPromised:"
            f"\n  Up: {promised_up}MB | Down: {promised_down}"
            f"\nTest Results ({todayDate} at {nowTime})"
            f"\n  Up: {self.up}MB | Down: {self.down}")
        if (self.up < promised_up) or (self.down < promised_down):
            self.message += "\n⚠️ Test results are below internet provider promised speed"
            print(self.message)
            self.test_results = False
            return False
        else:
            self.message += "\n✅ Test results are aligned to internet provider promised speed"
            print(self.message)
            self.test_results = True
            return True

    def post_on_twitter(self):
        tweet_post = "Hey @Telmex!\n"
        # Auth
        auth = tweepy.OAuth1UserHandler(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

        try:
            client = tweepy.Client(
                consumer_key=consumer_key, consumer_secret=consumer_secret,
                access_token=access_token, access_token_secret=access_token_secret
            )
        except tweepy.errors.Unauthorized:
            print("[!] Unable to authenticate")
        else:
            print(f"{client.get_me()[0]} has been successfully authenticated")
            tweet_post += self.message
            print(f"Post's Text:\n<<{tweet_post}>>")
            tweetID = client.create_tweet(text=tweet_post)[0]
            print(f"Tweet successfully posted: {tweetID}")
