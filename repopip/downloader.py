from shutil import move
import sys
from typing import BinaryIO
import requests
from pathlib import Path
from repopip.local_repo import DEFAULT_INDEX_URL, SIMPLE_PATH, TEMP_PATH

# headers = requests.head(addr)
# print(headers.headers)

class Downloader:

    def __init__(self, addr: str, file_name: str) -> None:
        self.addr = addr
        self.file = Path(TEMP_PATH).joinpath(file_name)

    def download(self):      
        if (self.file.exists()):
           return self._resume_download()
        else:
            return self._new_download()

    def _new_download(self):
            print("\nDownloading %s" % self.file)
            response = requests.get(self.addr, stream=True)
            return self._to_file(response, 'wb')

    def _resume_download(self):
        print("\nResumming Download %s" % self.file)
        resume_header = {'Range':f'bytes={ Path(self.file).stat().st_size}-'}
        response = requests.get(self.addr,stream=True, headers=resume_header)
        with open(self.file, "rb") as f:
            byte = f.read(4096)
            while byte:
                yield byte
                byte = f.read(4096)
        yield from self._to_file(response, 'ab')

    def _to_file(self, response : requests.Response, mode: str):
        print('Downloading from internet')
        with open (self.file, mode) as f:
            total_length = response.headers.get('content-length')
            if total_length is None: # no content length header
                f.write(response.content)
            else:
                dl = self.file.stat().st_size

                # When is a new Download dl = 0 and total_length = to the total length
                # Whes is resuming download dl = current downloaded data and total_length is 
                # the data that has to be downloaded, not the total length of the file
                # total_length = (total_original_file_length - dl)

                total_length = dl + int(total_length) 
                if(dl < total_length):
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(50 * dl / total_length)
                        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                        sys.stdout.flush()
                        yield data

        # When download is completed
        move(self.file, Path(SIMPLE_PATH))