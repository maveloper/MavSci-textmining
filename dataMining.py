#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install tweepy')
get_ipython().system('pip install pymongo[str]')


# In[ ]:


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime
import json
from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd


# In[ ]:


consumer_key = "WP0MH64WBzyAHQLOofIOqzrpU"


# In[ ]:


consumer_secret = "oll1I0hcROhli054eoRN9o4NbA6GXFh63UuBtCPv8wlKbF9JVf"


# In[ ]:


access_token = "1184879854656856068-IibRmCEZgBZIypRDnSiJOAvaVHu029"


# In[ ]:


access_token_secret = "atMrbwfdk0OAes2oo1bgH5DhHOhvXKBBsUpR2X9AsS4vv"


# In[ ]:


auth = OAuthHandler(consumer_key, consumer_secret)


# In[ ]:


auth.set_access_token(access_token,access_token_secret)


# In[ ]:


# Class to listner tw data stream and store in mongoDB
class MyListener(StreamListener):
    def on_data(self, dados):
        tweet = json.loads(dados)
        created_at = tweet["created_at"]
        id_str = tweet["id_str"]
        text = tweet["text"]
        obj = {"created_at": created_at, "id_str": id_str, "text": text,}
        tweeting = collection.insert_one(obj).inserted_id
        print(obj)
        return True


# In[ ]:


mylistener = MyListener()


# In[ ]:


mystream = Stream(auth, listener = mylistener)


# In[ ]:


client = MongoClient('mongodb+srv://USER:PASSWORD@cluster0-jomy6.mongodb.net/test?retryWrites=true&w=majority')


# In[ ]:


#TW connection
db = client.twitterdb


# In[ ]:


collection = db.tweets


# In[ ]:


keywords = ['covid19', 'coronavirus', 'corona']


# In[ ]:


#Filter start and redording tweets in mongoDB
mystream.filter(track=keywords)


# In[ ]:


#Dataset with response data on mongoDB
dataset = [{"created_at": item["created_at"], "text": item["text"],} for item in collection.find()]


# In[ ]:


df = pd.DataFrame(dataset)


# In[ ]:


df


# In[ ]:


cv = CountVectorizer()
count_matrix = cv.fit_transform(df.text)


# In[ ]:


word_count = pd.DataFrame(cv.get_feature_names(), columns=["word"])
word_count["count"] = count_matrix.sum(axis=0).tolist()[0]
word_count = word_count.sort_values("count", ascending=False).reset_index(drop=True)
word_count[:50]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




