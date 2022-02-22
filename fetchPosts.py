import requests, private_info, json
from requests.api import post

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

def message(function, premessage):
    print (f"fetchPosts.py - {function}: {premessage}")

def validRedditLink(link) -> bool:
    return 'reddit' in link

# takes a link and strips it to perma link format for reddit
# used later in the search
def stripLink(fullLink) -> str:
    fullLink = fullLink.split('?utm')[0].split('/r/')[-1]
    return f'/r/{fullLink}'

def defineTarget() -> str:
    startFromLink = ""
    link = startFromLink
    '''
    while startFromLink != "Y" and startFromLink != "N":
        link = ""
        message("defineTarget()", "Would you like to start from a reddit link? (y/n)")
        startFromLink = input().upper()
        
        if startFromLink == "Y":
            message("defineTarget()", "After which post do you want to scrape from?:")
            link = input()
            if validRedditLink(link):
                link = stripLink(link)
            else:
                message("defineTarget()", "That is not a valid reddit link.")
                startFromLink = ""
    '''
    if link == "": 
        link = stripLink(lastDownload())
    message("defineTarget()", f"Target is {link}")
    return link

def lastDownload() -> str:
    with open("data.json") as file:
        data = json.load(file)
    return data["Last Post"]

def fetchRawPosts(numBatches = 10, postsPerBatch = 100) -> list:
    params = {
        'limit':postsPerBatch, 
        "raw_json": 1}
    batchedPollList = []
    
    for batchNumber in range(numBatches):
        message("fetchRawPosts()", f"Polling {postsPerBatch} upvoted posts from Reddit with batch {batchNumber+1} of {numBatches}")
        batch = requests.get(f'https://oauth.reddit.com/user/{private_info.Username}/upvoted/', headers=headers, params=params).json()
        # adds posts
        batchedPollList.append(batch["data"]["children"])
        # updates parameters in requests to get next 100
        params = {
            **params, 
            **{'after': batch['data']['after']}
            }
    message("fetchRawPosts()", "Completed polling upvoted posts")
    return batchedPollList

def convertRaw(permalink, rawPosts) -> list:
    message("convertRaw()", "Converting raw posts to RedditPost Objects")
    postlist = [ 
        RedditPost(
            child["kind"],
            child["data"]["id"],
            child["data"]["url"],
            child["data"]["permalink"]
        ) 
        for batch in rawPosts 
        for child in batch
        if child["data"]["url"] != None
        ]
    for i in range(len(postlist)):
        if permalink == postlist[i].permalink:
            message("convertRaw()", f"Found target: {postlist[i].fullLink()}. Trimming list")
            postlist = postlist[:i]
            break
    message("convertRaw()", f"RedditPost conversion completed. {len(postlist)} posts converted.")
    return postlist
    
def getPosts():
    target = defineTarget()
    posts = fetchRawPosts()
    posts = convertRaw(target, posts)
    posts.reverse()
    return posts

def storeLastDownload(post) -> None:
    dumper = {
        "Last Post": post.fullLink()
    }
    with open("data.json", "w") as file:
        json.dump(dumper, file, indent=6)   
    return

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
            f'{self.fullLink()}'
            ']'
        )

    def fullLink(self):
        return f"https://www.reddit.com{self.permalink}"
