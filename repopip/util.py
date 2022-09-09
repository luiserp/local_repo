from pathlib import Path
from typing import List
from flask import url_for
from hurry.filesize import size, alternative
import requests
import sys
from bs4 import BeautifulSoup
from http.client import HTTPConnection
from threading import Thread
from shutil import move
from repopip.local_repo import DEFAULT_INDEX_URL, SIMPLE_PATH, TEMP_PATH

# Flag for inet connection
connection = False

# Templates filters
def filesize(bytes_int: int):
    return size(bytes_int, system=alternative)

def url( url : dict ):
    if( 'lang' in url.keys()):
        return url_for(url['path'], lang=url['lang'])
    else:
        return url_for(url['path'])

# Text if there is inet conection, this functions is called in the Thread at the end of this file
def test_inet_connection():
    global connection
    c = HTTPConnection(host="pypi.org", port=443, timeout=2)
    try:
        c.request("HEAD", "/")
        connection = True
    except Exception:  
        connection = False
    finally:
        c.close()

# Download a file from a link and returns the progress step by step(generator)
def download(href, file_name):
    file = Path(TEMP_PATH).joinpath(file_name)
    with open(file, "wb") as f:
        print("\nDownloading %s" % file)
        response = requests.get(href, stream=True, timeout=2)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=8192):
                dl += len(data)
                done = int(50 * dl / total_length)
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl}/{total_length}" )    
                sys.stdout.flush()
                f.write(data)
                yield data

    # When download is completed
    move(file, Path(SIMPLE_PATH))

# This function scraps pypi.org if there is connection and get the versions of the packages that aren't in the local repo
def scrap_pypi(package, exclude: List) -> List:    
    """
        This function scraps pypi.org if there is connection and get the versions of the packages that aren't in the local repo
        
        :param package: Package name for locking for
        :param exclude: List of the packages fullname to excude
    
    """
    global connection
    if not connection: return []
    try:
        page = requests.get(f"{DEFAULT_INDEX_URL}/{package}", timeout=2)
        soup = BeautifulSoup(page.content, "html.parser")
        packages = soup.find_all("a", href=True)
        packages = [ (p["href"], p.text) for p in packages if p.text not in exclude]
        return packages
    except:
        return []


Thread(target=test_inet_connection).start()
