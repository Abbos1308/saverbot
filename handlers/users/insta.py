import requests
import json

async def instadownloader(link):
    url = "https://instagramapi.up.railway.app/instagram"
    querystring = {"link": link}

    

    response = requests.request("GET", url,  params=querystring)
    rest = json.loads(response.text)
    #print("Result: ",rest)

    result_dict = rest['data'][0]['url']
    return result_dict
    #if not rest['status']:
        #return result_dict
    #else:
        #result_dict['url'] = rest['data'][0]['url']
        #return result_dict

