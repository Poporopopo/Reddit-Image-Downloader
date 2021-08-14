import pathlib, requests
from datetime import date

# create downloads folder with date of downloads
parentpath = pathlib.Path(__file__).parent
today = date.today().strftime("%Y-%m-%d")
downloadfolder = parentpath / "Downloads" / today
downloadfolder.mkdir(parents=True, exist_ok=True)

def verifyValidFileType(filename):
    filetype = filename.split('.')[-1]
    if filetype not in ["jpg", "png", "jpeg", "gif", "mp4"]:
        raise TypeError

# downloads and writes file
def downloadFromUrl(url):
    if "wixmp" in url:
        url, filename = wixmpDownload(url)
        return url, filename
    # checking for redgifs mp4s
    elif "redgifs" in url:
        url, filename = redgifDownload(url)
        return url, filename
    # checking for reddit galleries
    elif "gallery" in url:
        return 
    else:
        filename = url.split("/")[-1]
        generalDownload(url, filename)
        return url, filename
        
def generalDownload(url, filename):
    filepath = downloadfolder / filename
    download = requests.get(url)
    
    with filepath.open('wb') as f:
        f.write(download.content)
    return url, filename

def wixmpDownload(url):
    # removes token to get the filename
    filename = url.split("?token")[0].split("/")[-1]
    verifyValidFileType(filename)
    generalDownload(url, filename)
    return url, filename

def redgifDownload(url):
    # create lowercase video address
    vidname = url.split("/")[-1]
    lowerOGVid = f'https://thumbs2.redgifs.com/{vidname}.mp4'
    # finding position of original video link
    req = requests.get(url)
    URLindex = req.text.lower().split('"').index(lowerOGVid)
    # retrieving original link
    url = req.text.split('"')[URLindex]
    filename = url.split("/")[-1]
    generalDownload(url, filename)
    return url, filename

def redditGalleryDownload(url):
    # get html text
    html = requests.get(url)
    html = html.text.split('<')
    # search for preview.redd.it, excluding the awards
    # download from those links
    dfiles = ""
    for splice in html:
        # parse for full size image links
        if 'href="https://preview.redd.it' in splice and 'award' not in splice:
            splice = splice.split('"')
            splice = [x for x in splice if "preview" in x][0].replace("&amp;", "&")
            dfiles += f"{redditGalleryMini(splice)}, "
    return url, dfiles

def redditGalleryMini(url):
    filename = url.split("?")[0].split("/")[-1]
    generalDownload(url,filename)
    return filename

if __name__ == "__main__":
    print("lul")
    print(parentpath)
    print(today)
    print(downloadfolder)