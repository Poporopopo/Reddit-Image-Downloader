'''
Code Idea:
Requirements: Reddit API key

Checks upvoted posts with pics and downloads them
If provided a link, it will use that as the earliest post and download from there to latest post.
'''

from requests.exceptions import RequestException
from fetchPosts import getPosts, storeLastDownload
from downloadmanager import manager

def message(premessage) -> None:
    print(f"main.py: {premessage}")

def main() -> None:
    message("Gathering posts")
    posts = getPosts()

    mng = manager(posts)
    mng.download()
    mng.findFails()
    if len(posts) > 0:
        storeLastDownload(posts[-1])
    
if __name__ == "__main__":
    main()