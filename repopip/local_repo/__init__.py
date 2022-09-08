from pathlib import Path
import os

DEFAULT_INDEX_URL = "https://pypi.org/simple"

try:
    SIMPLE_PATH = Path().home().joinpath('.static', 'simple')
    if(not SIMPLE_PATH.exists()):
        os.makedirs(SIMPLE_PATH)
except OSError:
    pass

