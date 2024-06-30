import requests
import json

async def ttdownloader(link):
    url = "https://instagramapi.up.railway.app/tiktok"
    querystring = {"link": link}

    

    response = requests.request("GET", url,  params=querystring)
    rest = json.loads(response.text)
    #print("Result: ",rest)

    result_dict = rest['result']['video']
    return result_dict
    #if not rest['status']:
        #return result_dict
    #else:
        #result_dict['url'] = rest['data'][0]['url']
        #return result_dict
  
