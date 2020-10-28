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
keys = pd.read_csv("keys_royardo.csv",header=None)
keys = dict(zip(keys[0],keys[1]))

# Authenticate through the API
auth = tweepy.OAuthHandler(keys['api_key'], keys['api_secret_key'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth)


########################################################
# Víctimas
########################################################
victimas = ['actualidadpanam', 'joeldongsteen']
victimas_ids = ['2279705827', '1056631267'] # Find yours at http://gettwitterid.com/


########################################################
# Helper function
########################################################
vowels = ['a','e','i','o','u', 'á', 'é', 'í', 'ó', 'ú',
          'A', 'E', 'I', 'O', 'U', 'Á', 'É', 'Í', 'Ó', 'Ú']

pattern1 = '?P<pic>pic.twitter.com/[^\s]+'
pattern2 = '?P<url>https?://[^\s]+'


def text_clean(text):
    links = [tuple(j for j in i if j)[-1] for i in re.findall(f"({pattern1})|({pattern2})",text)]
    for link in links:
        text = text.replace(link,"")
             
    hashtags = [interaction for interaction in text.split() if interaction.startswith("#")]
    for hashtag in hashtags:
        text = text.replace(hashtag,"")
        
    mentions = [interaction for interaction in text.split() if interaction.startswith("@")]
    for mention in mentions:
        text = text.replace(mention,"")
        
    text = " ".join([word for word in text.split() if (set(word.lower()) != {'a', 'h'}) and (set(word.lower()) != {'a', 'j'})])    

    return text


def memeficator(text):
    text = text_clean(text)
    text = re.sub(' +', ' ', text)
    
    # Do nothing for tweets that don't contain words
    if not any(char.isalpha() for char in text):
        return None, None 
    
    method = random.choice(['ninini', 'spongebob'])
    
    if method == 'spongebob':
        img = "spongebob.png"
        text = text.lower()
        text = "".join((str.upper,str.lower)[i%2](ch) for i,ch in enumerate(text))
        
    if method == 'ninini':
        img = "ninini.jpg"
        text = "".join(['i' if letter in vowels else letter for letter in text])
        text = f"Ay, sí. Ay, sí... {text}"
        
    return text[:130], img


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
                print("\033[1m\033[94mTuit original:\033[0m")
                print(user, tweet)
                print()

                print("\033[1m\033[94mRespuesta:\033[0m")
                reply, img = memeficator(tweet)
                if reply is None:
                    print("Ninguna :(")

                else:
                    reply = f"@{user} {reply}"
                    print(f"{reply} <<<{img}>>>")
                    api.update_with_media(img, reply, in_reply_to_status_id = tweet_id)
                print()
                print("-----------------------------------------------------------------------------------")
                print()
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

