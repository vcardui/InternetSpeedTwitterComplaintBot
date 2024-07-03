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
# | Last update..: July 2nd, 2024
# | WhatIs.......: Internet Speed X (Twitter) Complaint Bot - Main
# +----------------------------------------------------------------------------+

# ------------ Resources / Documentation involved -------------
# Locating Selenium Elements: https://selenium-python.readthedocs.io/locating-elements.html
# Tweepy Documentation: https://docs.tweepy.org/en/stable/client.html

# ------------------------- Libraries -------------------------
# CarduiBot
from carduiBot import InternetSpeedTwitterBot

# ------------------------- Variables -------------------------
# Promised Internet Speed by Telmex in Mega Bytes
PROMISED_UP = 60
PROMISED_DOWN = 60

# --------------------------- Code ----------------------------
carduiBot = InternetSpeedTwitterBot()
carduiBot.get_internet_speed()

# Decide whether to tweet or not
if not carduiBot.check_internet_speed(PROMISED_UP, PROMISED_DOWN):
    print("I will tweet")
    carduiBot.post_on_twitter()
else:
    print("Internet speed is doing good! Did not tweet")
