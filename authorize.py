'''
copied/edited code to get a reddit oauth working
'''

import requests
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

def fetchNewUpvoted(numBatches = 10, postsPerBatch = 100) -> list:
    params = {
        'limit':postsPerBatch, 
        "raw_json": 1}
    batchedPollList = []
    batchNumber = 1
    # polls reddit for a batch of 100 upvoted posts
    # repeats polling for next 100 posts
    # adds all new posts' urls to posturls
    # if permalink found stops looping
    for batchNumber in range(numBatches):
        print (f"Polling {postsPerBatch} upvoted posts from Reddit with batch {batchNumber+1} of {numBatches} ")
        batch = requests.get(f'https://oauth.reddit.com/user/{private_info.Username}/upvoted/', headers=headers, params=params).json()
        # adds posts
        batchedPollList.append(batch["data"]["children"])
        # updates parameters in requests to get next 100
        params = {
            **params, 
            **{'after': batch['data']['after']}
            }
    return batchedPollList

def getPostsToDownload(permalink="", numBatches = 10, batchSize = 100) -> list:
    batchedList = fetchNewUpvoted(numBatches, batchSize)
    postlist = [ 
        RedditPost(
            child["kind"],
            child["data"]["id"],
            child["data"]["url"],
            child["data"]["permalink"]
        ) 
        for batch in batchedList for child in batch]
    for i in range(len(postlist)):
        if permalink == postlist[i].permalink:
            postlist = postlist[:i]
            break
    return postlist
    
class RedditPost:
    def __init__(self, kind, id, url, permalink) -> None:
        self.typePrefix = kind
        self.postid = id
        self.url = url
        self.permalink = permalink

    def __str__(self):
        return (f'['
            f'{self.typePrefix},'
            f'{self.postid},'
            f'{self.url},'
            f'{self.permalink}'
            ']'
        )

    def makeLink(self):
        return f"https://www.reddit.com/{self.permalink}"

if __name__ == "__main__":
    '''
    test = requests.get(f'https://oauth.reddit.com/user/{private_info.Username}/saved/', headers=headers, params=params)
    test = test.json()
    print (test["data"].keys())
    print (test["data"]["after"])
    print (len(test["data"]["children"]))
    print (test["data"]["children"][0]["kind"])
    print (test["data"]["children"][0]["data"].keys())
    print (test["data"]["children"][0]["data"]["url"])
    print (test["data"]["children"][0]["data"]["permalink"])
    print (test["data"]["children"][0]["data"]["id"])
    '''
    test = getPostsToDownload(numBatches=1,batchSize=10)
    for post in test:
        print (post)
