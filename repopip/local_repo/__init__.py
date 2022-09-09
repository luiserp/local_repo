from pathlib import Path
import os

DEFAULT_INDEX_URL = "https://pypi.org/simple"

try:
    SIMPLE_PATH = Path().home().joinpath('.static', 'simple')
    TEMP_PATH = Path().home().joinpath('.static', 'temp')
    if(not SIMPLE_PATH.exists()):
        os.makedirs(SIMPLE_PATH)
        
    if(not TEMP_PATH.exists()):
        os.makedirs(TEMP_PATH)
except OSError:
    pass

