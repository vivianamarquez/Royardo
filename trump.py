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
victimas = ['realdonaldtrump']
victimas_ids = ['25073877'] # Find yours at http://gettwitterid.com/


########################################################
# Helper functions
########################################################
pattern1 = '?P<pic>pic.twitter.com/[^\s]+'
pattern2 = '?P<url>https?://[^\s]+'

aux_verbs = ["am", "is", "are", "was", "were", "being", "been", "be",
             "have", "has", "had", "do", "does", "did", "will", "would", "shall", "should",
             "may", "might", "must", "can", "could"]


def text_clean(text):
    links = [tuple(j for j in i if j)[-1] for i in re.findall(f"({pattern1})|({pattern2})",text)]
    for link in links:
        text = text.replace(link,"")
        
    text = " ".join([word for word in text.split()])    

    return text

    
def is_aux_verb(word):
    word = word.lower()
    if "'" in word:
        word1 = word.split("'")[0]
        word2 = word1[:-1]
        if word1 in aux_verbs or word2 in aux_verbs:
            return True
        else:
            return False
    if word in aux_verbs:
        return True
    return False


def return_first_question(text):
    text = text.replace(".","?").replace(",","?").replace(";","?").replace("!","?").split("?")
    for sentence in text:
        if "why" in sentence.lower() and is_aux_verb(sentence.split()[1]):
            idx = sentence.lower().index("why")
            new_sentence = sentence[idx:]
            return new_sentence


def memeficator(text):
    text = text_clean(text)
    text = re.sub(' +', ' ', text)
    
    # Do nothing for tweets that don't contain words
    if not any(char.isalpha() for char in text):
        return None, None 
    
    question = return_first_question(text)
    
    # Do nothing if the tweet doesn't have a why question
    if question is None:
        return None, None 
        
    img = "ninini.jpg"
    if question.isupper():
        text = f"MOMMY, {question.strip()}?"
    else:
        text = f"Mommy, w{question[1:].strip()}?"
        
    return text, img


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

