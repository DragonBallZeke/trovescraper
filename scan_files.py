import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
url = 'https://thetrove.net/Books/Dungeons%20&%20Dragons/'


def scan_files(url):
    print('scanning '+url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    files = soup.find_all(class_='litem file',recursive=True)
    folders = soup.find_all(class_='litem dir',recursive=True)
    folders.pop(0)
    for folder in folders:
        scan = scan_files(url+str(folder.find('a')['href'])+'/')
        for file in scan[0]:
            download_file(scan[1]+str(file.find('a')['href']).replace('./',''))
    return files,url

def download_file(url):
    print('downloading '+url)
    path = urllib.parse.unquote(url.replace('https://',''))
    r = requests.get(url, allow_redirects=True)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(r.content)

print(scan_files(url))