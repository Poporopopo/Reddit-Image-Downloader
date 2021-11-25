import pathlib
from datetime import date
import downloader
from fetchPosts import RedditPost

class manager:
    def __init__(self, posts) -> None:
        parentpath = pathlib.Path(__file__).parent
        today = date.today().strftime("%Y-%m-%d")
        self.downloadFolder = parentpath / "Downloads" / today
        self.downloaders = self.createAllDownloaders(posts)
        self.messages = []

    def message(self, function, premessage):
        """Message function to display what is going on in manager"""
        print(f"downloadmanager.py - manager.{function}: {premessage} ")

    def downloaderFactory(self, post: RedditPost):
        """Factory for creating downloaders"""
        if "redgifs" in post.url:
            return downloader.RedGifDownloader(post, self.downloadFolder)
        elif "gallery" in post.url:
            return downloader.redditGalleryDownloader(post, self.downloadFolder)
        else:
            return downloader.GeneralDownloader(post, self.downloadFolder)
            
    def createAllDownloaders(self, posts: list):
        """On init, creates a list of downloader objects from a list of posts"""
        self.message("createAllDownloads()", "Creating downloader objects")
        return [self.downloaderFactory(post) for post in posts]

    def download(self):
        """Runs all the downloaders"""
        self.downloadFolder.mkdir(parents=True, exist_ok=True)
        self.message("download()", "Running all downloaders.")
        for downloader in self.downloaders:
            msg = downloader.download()
            self.messages.append(msg)
            print(msg)
        
    def findFails(self):
        """Finds all messages with failures for debugging"""
        self.message("findFails()", "Scanning console messages for fails")
        for message in self.messages:
            if "fail" in message:
                print (message)