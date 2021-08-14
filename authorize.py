'''
copied/edited code to get a reddit oauth working
'''

import requests
import private_info
from downloader import redditGalleryDownload

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

params = {'limit':10}

def fetchNewUpvoted(earliest_permalink):
    postsPerBatch = 100
    params = {'limit':postsPerBatch}
    posturls = []
    permalink_found = False
    batchNumber = 1
    # polls reddit for a batch of 100 upvoted posts
    # repeats polling for next 100 posts
    # adds all new posts' urls to posturls
    # if permalink found stops looping
    while not permalink_found:
        print (f"Polling batch {batchNumber} of {postsPerBatch} from Reddit")
        batch = requests.get(f'https://oauth.reddit.com/user/{private_info.Username}/upvoted/', headers=headers, params=params).json()
        # adds posts
        # searchs for permalink match
        for child in batch["data"]["children"]:
            posturls.append(child["data"]["url"])
            if earliest_permalink in child["data"]["permalink"]:
                print ("Earliest post has been found!")
                permalink_found = True
                break
        # updates parameters in requests to get next 100
        params = {
            **params, 
            **{'after': f"t3_{batch['data']['children'][postsPerBatch - 1]['data']['id']}"}
            }
        batchNumber = batchNumber + 1
    return posturls

if __name__ == "__main__":
    # while the token is valid (~2 hours) we just add headers=headers to our requests
    # test = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    '''
    # while the token is valid (~2 hours) we just add headers=headers to our requests
    test = requests.get(f'https://oauth.reddit.com/user/{private_info.Username}/upvoted/', headers=headers, params=params)
    test = test.json()
    # print (json.dumps(test))
    print (test.keys())
    print (test["kind"])
    print (test["data"].keys())
    print(test["data"]["children"][0]["data"].keys())
    for child in test["data"]["children"]:
        print (child["data"]["url"], child["data"]['permalink'], child["data"]['id'])
    '''
    
    postsPerBatch = 100
    params = {'limit':postsPerBatch}
    permalink_found = False
    earliest_permalink = '/r/thighdeology/comments/omww18/fuck_the_wave_pool/'
    # polls reddit for a batch of 100 upvoted posts
    # repeats polling for next 100 posts
    # adds all new posts' urls to posturls
    # if permalink found stops looping
    while not permalink_found:
        batch = requests.get(f'https://oauth.reddit.com/user/{private_info.Username}/upvoted/', headers=headers, params=params).json()
        # adds posts
        # searchs for permalink match
        for child in batch["data"]["children"]:
            if earliest_permalink in child["data"]["permalink"]:
                print ("Earliest post has been found!")
                print(child["data"].keys())
                print(child["data"]["url"])
                print(child["data"]["permalink"])
                print(child["data"]["gallery_data"])
                print(child["data"]["media_only"])
                print(child["data"]["media"])
                permalink_found = True
                print(redditGalleryDownload(child["data"]["url"]))
                break
        # updates parameters in requests to get next 100
        params = {
            **params, 
            **{'after': f"t3_{batch['data']['children'][postsPerBatch - 1]['data']['id']}"}
            }