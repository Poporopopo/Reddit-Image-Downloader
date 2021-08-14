import pathlib, requests

parentpath = pathlib.Path(__file__).parent

# downloads and writes file
def downloadFromUrl(url):
    if "wixmp" in url:
        wixmpDownload(url)
    # checking for redgifs mp4s
    elif "redgifs" in url:
        redgifDownload(url)
    else:
        filename = url.split("/")[-1]
        generalDownload(url, filename)

def generalDownload(url, filename):
    filepath = parentpath / "test" / filename
    download = requests.get(url)
    
    with filepath.open('wb') as f:
        f.write(download.content)

def wixmpDownload(url):
    # removes token to get the filename
    filename = url.split("?token")[0].split("/")[-1]
    verifyValidFileType(filename)
    generalDownload(url, filename)

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

def verifyValidFileType(filename):
    filetype = filename.split('.')[-1]
    if filetype not in ["jpg", "png", "jpeg", "gif", "mp4"]:
        raise TypeError

if __name__ == "__main__":
    print("lul")
    