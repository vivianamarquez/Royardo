########################################################
# Import Librarires
########################################################
import re
import json
import random
import pandas as pd

import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener


########################################################
# Authenticate
########################################################
# Load Keys
keys = pd.read_csv("keys.csv",header=None)
keys = dict(zip(keys[0],keys[1]))

# Authenticate through the API
auth = tweepy.OAuthHandler(keys['api_key'], keys['api_secret_key'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth)


########################################################
# Víctimas
########################################################
victimas = ['danielsampero']
victimas_ids = ['134855279'] # Find yours at http://gettwitterid.com/


########################################################
# Listen
########################################################
class listener(StreamListener):

    def on_status(self, data):
        try:
            tweet = data.text
            tweet_id = data.id
            user = data.user.screen_name
            
            if user.lower() not in victimas or "RT @" in tweet:
                pass
                
            else:
                if reply is None:
                    pass

                else:
                    reply = f"@{user} {reply}"
                    api.update_status("DANI, soy un bot, soy un fan. Mira este video: https://www.youtube.com/watch?v=xcsgZWe4zxA&ab_channel=vivmarquez", in_reply_to_status_id = tweet_id)

        except:
            print("badluck")
        
        return(True)

    def on_error(self, status):
        print("\n********* ERROR *********\n")
        print(status)

        
print("I'm working")
twitterStream = Stream(auth, listener())
while True:
    print("I'm looping!")
    try:
        twitterStream.filter(follow=victimas_ids)
    except:
        print("\033[1m\033[35moh fuck!\033[0m")
        print("Woah! New loop!")

