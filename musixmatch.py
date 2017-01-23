import json
import urllib.parse
import requests

base_url = "http://api.genius.com"

headers = {'Authorization': "Bearer " + '1GYxipTmiBvcVCUJeONdMLbnf4VXpDOi1U5QZMfuRvRZVQTCh6S-jRkYCw40u9Dl'}
search_url = base_url + "/search?q={}"
song_title = "Wesley's Theory"
search_url =search_url.format(urllib.parse.quote(song_title))
response = requests.get(search_url, headers=headers)
recv_json = response.json()
print(recv_json["response"]["hits"][0]["result"]["path"])
#file_obj = open("response.json", 'w')
#json.dump(response.json(), file_obj, indent=4)