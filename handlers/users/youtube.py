import requests
from pytube import YouTube
import random  

word = "q w e r t y u i  o p a s d f g h  j k l z x  c v b n m"
words = word.split(' ')

def yt(link):
    url = "https://yt-api.p.rapidapi.com/dl"

    # Extracting video ID
    video_id = YouTube(link).video_id

    print("Video ID:", video_id)
    querystring = {"id":video_id}
    
    headers = {
    	"x-rapidapi-key": "913d2822eemsh19cdbd1ccfa70ccp1098c9jsn42392168a2a7",
    	"x-rapidapi-host": "yt-api.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    res = response.json()
    url = res['formats'][0]['url']
    sub = random.choice(words)
    sub2 = random.choice(words)
    filename = f"video_{sub}_{sub2}.mp4"

    response = requests.get(url)

    with open(filename, 'wb') as f:
        f.write(response.content)
    file = types.InputFile(filename)
    return file
