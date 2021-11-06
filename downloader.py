import pathlib, requests
from datetime import date
from time import sleep, time
from abc import ABC, abstractmethod
from authorize import RedditPost

# create downloads folder with date of downloads
parentpath = pathlib.Path(__file__).parent
today = date.today().strftime("%Y-%m-%d")
downloadfolder = parentpath / "Downloads" / today
downloadfolder.mkdir(parents=True, exist_ok=True)

def runDownloads(redditPosts: list):
    log = ""
    downloaders = [createDownloader(post) for post in redditPosts]
    for downloader in downloaders:
        log += f"{downloader.download()}\n"
        
def createDownloader(post: RedditPost):
    if "redgifs" in post.url:
        print("RedGif - WIP")
    elif "gallery" in post.url:
        print("Reddit gallery - WIP")
    else:
        return GeneralDownloader(post)

'''
# downloads and writes file
def downloadFromUrl(url):
    # checking for redgifs mp4s
    if "redgifs" in url:
        url, filename = redgifDownload(url)
        return url, filename
    # checking for reddit galleries
    elif "gallery" in url:
        url, filename = redditGalleryDownload(url)
        return url, filename
    else:
        filename = extractFileName(url)
        url = reAmpersand(url)
        generalDownload(url, filename)
        return url, filename

def redgifDownload(url):
    # create lowercase video address
    vidname = url.split("/")[-1]
    lowerOGVid = f'https://thumbs2.redgifs.com/{vidname}.mp4'
    # finding position of original video link
    req = requestGetUntilSuccess(url)
    URLindex = req.text.lower().split('"').index(lowerOGVid)
    # retrieving original link
    url = req.text.split('"')[URLindex]
    filename = extractFileName(url)
    generalDownload(url, filename)
    return url, filename

def redditGalleryDownload(url):
    # get html text
    html = requestGetUntilSuccess(url, waittime=60, max=10)
    html = html.text.split('<')
    # search for preview.redd.it, excluding the awards
    # download from those links
    dfiles = ""
    for splice in html:
        # parse for full size image links
        if 'href="https://preview.redd.it' in splice and 'award' not in splice:
            splice = splice.split('"')
            splice = reAmpersand([x for x in splice if "preview" in x][0])
            dfiles += f"{redditGalleryMini(splice)}, "
    return url, dfiles

# redundant?
def redditGalleryMini(url):
    filename = extractFileName(url)
    generalDownload(url,filename)
    return filename
'''            

class AbstractDownloader (ABC):
    
    @abstractmethod
    def download(self):
        pass
    
    def verifyValidFileType(filename) -> bool:
        """
        checks for acceptable files for this program
        mostly for bugfinding for unknown URL types
        """
        filetype = filename.split('.')[-1]
        return filetype not in ["jpg", "png", "jpeg", "gif", "mp4"]

    def extractFileName(url) -> str:
        """
        generic filename extractor
        removes all parameters following "?"
        finds filename after last "/"
        """
        filename = url.split("?")[0].split("/")[-1]
        return filename

    def reAmpersand(string) -> str:
        """
        some urls come with "&amp;"
        this causes errors when polling and must be converted to "&"
        """
        return string.replace("&amp;", "&")

class GeneralDownloader (AbstractDownloader):
    
    def __init__(self, post: RedditPost):
        self.post = post
        parentpath = pathlib.Path(__file__).parent
        today = date.today().strftime("%Y-%m-%d")
        downloadfolder = parentpath / "Downloads" / today
        downloadfolder.mkdir(parents=True, exist_ok=True)
        self.downloadfolder = downloadfolder

    def download (self) -> str:
        filename = self.extractFileName(self.post.url)
        self.verifyValidFileType(filename)
        filepath = self.downloadfolder / filename
        if filepath.exists():
            raise FileExistsError
        download = requests.get(self.post.url)
        with filepath.open('wb') as f:
            f.write(download.content)
        return (f"Downloaded {filename} from {self.post.makeLink()} to {downloadfolder}")        

class RedGifDownloader (GeneralDownloader):
    
    def download(self) -> None:
        return super().download()