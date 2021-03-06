from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
url = 'https://thetrove.net/Books/Dungeons%20&%20Dragons/'


def scan_files(url):
    # tqdm.write('scanning '+url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    files = soup.find_all(class_='litem file',recursive=True)
    folders = soup.find_all(class_='litem dir',recursive=True)
    folders.pop(0)
    for folder in tqdm(folders, desc=url):
        scan = scan_files(url+str(folder.find('a')['href'])+'/')
        for file in tqdm(scan[0]):
            download_file(scan[1]+str(file.find('a')['href']).replace('./',''))
    return files,url


def download_file(url):
    # tqdm.write('downloading '+url)
    path = urllib.parse.unquote(url.replace('https://',''))
    if os.path.exists(path):
        # tqdm.write('Already exists, skipping')
        return
    r = requests.get(url, allow_redirects=True)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(r.content)

scan_files(url)