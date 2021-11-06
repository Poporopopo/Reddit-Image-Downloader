'''
Code Idea:
Requirements: Reddit API key

Checks upvoted posts with pics and downloads them
If provided a link, it will use that as the earliest post and download from there to latest post.
'''

from requests.exceptions import RequestException
import authorize, downloader
from time import sleep

def verifyRedditLink(link) -> bool:
    return 'reddit' in link

# takes a link and strips it to perma link format for reddit
# used later in the search
def stripLink(fullLink) -> str:
    if "?utm" in fullLink:
        fullLink = fullLink.split('?utm')[0]
    fullLink = fullLink.split('/r/')[-1]
    return f'/r/{fullLink}'

def wantLink() -> bool:
    startFromLink = ""
    while startFromLink != "Y" and startFromLink != "N":
        startFromLink = input("Would you like to start from a reddit link? (Y/N) \n").upper()
    return startFromLink == "Y"


def defineTarget() -> str:
    link = ""
    while not verifyRedditLink(link):
        link = input("After which post do you want to scrape from?: \n")
    link = stripLink(link)
    return link

# method to run and download
# checks if link can be stripped to a permalink
def main():
    address = ""
    if wantLink():
        address = defineTarget()
        print (f"Scrape from upvoted posts after{address}")
    else:
        print ("Scrape all upvoted posts.")

    print ("Beginning Polling from Reddit")
    posts = authorize.getPostsToDownload(address)
    print(posts)
    print ("Polling complete!")

    # downloader.runDownloads(posts)
    '''
    badlinks = []
    print ("Beginning Downloading from links")
    for url in urls:
        try:
            url, filename = downloader.downloadFromUrl(url)
            print (f"Successfully downloaded {filename} from {url}")
        except TypeError as e:
            # print (getattr(e, 'message', repr(e)))
            print (f"Failed to download from {url}. A list has been generated")
            badlinks.append(url)
        except RequestException as e:
            print (f'Failed to request from {url}. A list has been generated')
            badlinks.append(url)
        except FileExistsError as e:
            print (f'File from {url} appears to have already been downloaded')
        # sleep(1)
    if len(badlinks) > 0:
        print ("Errors trying to pull from: ", str(badlinks))
    '''
    
if __name__ == "__main__":
    main()