import requests
import json

async def pindownloader(link):
    url = "https://instagramapi.up.railway.app/pin"

    querystring = {"link": link}

    

    response = requests.request("GET", url,  params=querystring)
    rest = json.loads(response.text)
    #print("Result: ",rest)

    result_dict = {}
    result_dict['type'] = rest['imran']['type']
    result_dict['url'] = rest['imran']['url']
    return result_dict
    