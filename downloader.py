from abc import ABC, abstractmethod
from fetchPosts import RedditPost, message
import requests
from time import sleep, time

class AbstractDownloader (ABC):
    
    @abstractmethod
    def successmessage(self) -> str:
        pass

    @abstractmethod
    def failmessage(self, reason) -> str:
        pass

    @abstractmethod
    def download(self) -> str:
        pass

class GeneralDownloader (AbstractDownloader):
    '''
    Assumes that the url given is a direct link to image
    '''

    def __init__(self, post: RedditPost, DLpath):
        self.post = post
        self.DLpath = DLpath
        self.downloadertype = "General Downloader"
        self.validtypes = ["jpg", "png", "jpeg", "gif", "mp4"]

    def validFiletype(self, filename) -> bool:
        """
        Checks for acceptable files to download
        """
        filetype = filename.split('.')[-1]
        return filetype in self.validtypes

    def extractFileName(self, url) -> str:
        """
        Generic filename extractor.
        Removes all parameters following "?" and finds filename after last "/"
        """
        filename = url.split("?")[0].split("/")[-1]
        return filename

    def reAmpersand(self, string) -> str:
        """
        Some urls come with "\&amp;"
        This causes errors when polling and must be converted to "&"
        """
        return string.replace("&amp;", "&")

    def successmessage(self):
        """Message for when a file is successfully downloaded"""
        return f"downloader.py - {self.downloadertype}: Successfully downloaded from {self.post.fullLink()}."

    def failmessage(self, reason):
        """Message for when a file can't be downloaded. Formats the reason given."""
        return f"downloader.py - {self.downloadertype}: Failed to download from {self.post.fullLink()} because {reason}."

    def download (self) -> str:
        """High level representation of downloading the file"""
        url = self.reAmpersand(self.post.url)
        filename = self.extractFileName(url)
        DLpath = self.DLpath
        return self.genericDownloader(url, filename, DLpath)
        
    def genericDownloader(self, url, filename, DLpath) -> str:
        """"Low level representation of downloading the file"""
        if not self.validFiletype(filename):
            reason = (
                "this filetype is not supported. "
                "The list of support filetypes are: "
                f"{', '.join(self.validtypes)}. "
            )
            return self.failmessage(reason)

        filepath = DLpath / filename
        if filepath.exists():
            reason = (
                f"the file, {filename} already exists in this location. Skipping"
            )
            return self.failmessage(reason)

        download = requests.get(url)
        with filepath.open('wb') as f:
            f.write(download.content)
        return self.successmessage()

class RedGifDownloader (GeneralDownloader):
    
    def __init__(self, post: RedditPost, DLpath):
        super().__init__(post, DLpath)
        self.downloadertype = "RedGif Downloader"

    def download(self) -> str:
        url = self.reAmpersand(self.getURL(self.post.url))
        filename = self.extractFileName(url)
        DLpath = self.DLpath
        return self.genericDownloader(url, filename, DLpath)

    def getURL(self, url):
        '''Finds redgif video URL by scanning html'''
        # create lowercase video address
        vidname = url.split("/")[-1]
        lowerOGVid = f'https://thumbs2.redgifs.com/{vidname}.mp4'
        # finding position of original video link in Html
        req = requests.get(url)
        URLindex = req.text.lower().split('"').index(lowerOGVid)
        # retrieving original link
        url = req.text.split('"')[URLindex]
        
class redditGalleryDownloader(GeneralDownloader):
    
    def __init__(self, post: RedditPost, DLpath):
        super().__init__(post, DLpath)
        self.downloadertype = "Reddit Gallery Downloader"
    
    def download(self) -> str:
        resp = self.repeatRequest(10)
        imageLinks = self.findURLs(resp.text)
        outputmessage = f"Downloading from reddit gallery: {self.post.fullLink()}:\n"
        for imageLink in imageLinks:
            url = imageLink
            filename = self.extractFileName(url)
            DLpath = self.DLpath
            outputmessage += f"\t{self.genericDownloader(url, filename, DLpath)}\n"
        return outputmessage

    def repeatRequest(self, timeSleep) -> requests.Response:
        """Repeatedly queries the server when response fails. Waits 10s between queries"""
        while True:
            resp = requests.get(self.post.url)
            if resp.status_code == 200:
                break
            print(
                f"downloader.py - {self.downloadertype}.repeatRequest(): "
                f"Response status code {resp.status_code}. "
                f"Waiting {timeSleep} seconds. "
                )
            sleep(timeSleep)
        return resp
        
    def findURLs(self, html: str) -> list:
        """Searches through reddit gallery HTML to find image URLs."""
        # search in the html for preview.redd.it, but excluding the awards
        # at the same time separate the url from the html code
        links = [splice.split('"') for splice in html.split('<') if 'href="https://preview.redd.it' in splice and 'award' not in splice]
        links = [self.reAmpersand(link) for splice in links for link in splice if "https://preview.redd.it" in link]
        return links
    