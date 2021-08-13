'''
Code Idea:
Requirements: Reddit API key

Checks upvoted posts with pics and downloads them
If provided a link, it will use that as the earliest post and download from there to latest post.
'''

import authorize

# takes a link and strips it to perma link format for reddit
# used later in the search
def stripLink(fullLink):
    fullLink = fullLink.split('/r/')
    if 'reddit' in fullLink[0]:
        return f'/r/{fullLink[-1]}'
    else:
        return "bwuh"

# method to run and download
# checks if link can be stripped to a permalink
def run(early_link):
    early_link = stripLink(early_link)
    if early_link == "bwuh":
        return
    urls = authorize.fetchNewUpvoted(early_link)

if __name__ == "__main__":
    # print (stripLink('https://www.reddit.com/r/IWantToBeHerHentai2/comments/p3uvlw/i_wanna_be_one_of_the_girls_so_bad/'))
    # print (stripLink("https://google.com/"))

    run("https://www.reddit.com/r/IWantToBeHerHentai2/comments/p3mizl/im_gonna_hump_stuff_until_i_cum/")