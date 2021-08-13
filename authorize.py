'''
copied/edited code to get a reddit oauth working
'''

import requests, json
from requests.api import head
import private_info

auth = requests.auth.HTTPBasicAuth(
    private_info.Client_ID,
    private_info.Secret_Token
)

# login method('password'), username and password
data = {
    'grant_type': 'password',
    'username': private_info.Username,
    'password': private_info.Password
    }

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'My Upvote Scraper/0.0.1'}

# send our request for an OAuth token
res = requests.post(
    'https://www.reddit.com/api/v1/access_token',
    auth=auth, 
    data=data, 
    headers=headers
    )

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
# test = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

print (res.json())
print (headers)
# print(test.json())

# while the token is valid (~2 hours) we just add headers=headers to our requests
test = requests.get(f'https://oauth.reddit.com/user/{private_info.Username}/upvoted/', headers=headers)
test = test.json()
# print (json.dumps(test))
print (test.keys())
print (test["kind"])
print (test["data"].keys())
for child in test["data"]["children"]:
    print (child["data"]["url"])