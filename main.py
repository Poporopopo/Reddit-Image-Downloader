'''
Code Idea:
Requirements: Reddit API key

Checks upvoted posts with pics and downloads them
If provided a link, it will use that as the earliest post and download from there to latest post.
'''

import authorize, downloader

def verifyRedditLink(link):
    return 'reddit' in link

# takes a link and strips it to perma link format for reddit
# used later in the search
def stripLink(fullLink):
    if "?utm" in fullLink:
        fullLink = fullLink.split('?utm')[0]
    fullLink = fullLink.split('/r/')[-1]
    return f'/r/{fullLink}'

    
# method to run and download
# checks if link can be stripped to a permalink
def run(link):
    urls = authorize.fetchNewUpvoted(link)
    badlinks = []
    for url in urls:
        try:
            file = downloader.downloadFromUrl(url)
            print(f"Successfully downloaded {file} from {url}")
        except TypeError as e:
            print (f"Failed to download from {url}. A list has been generated")
            badlinks.append(url)
            print(e)
    if len(badlinks) > 0:
        print ("Errors trying to pull from: ", str(badlinks))

if __name__ == "__main__":
    address = ""
    while not verifyRedditLink(address):
        address = input("Give me the earliest reddit post you want to start from: \n")
    address = stripLink(address)
    print (f"Running scraper starting from {address}")
    run(address)