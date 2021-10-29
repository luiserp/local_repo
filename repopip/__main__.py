from repopip import create_app
from dotenv import load_dotenv
import subprocess
load_dotenv(override=True)

subprocess.run(['flask', 'run'])
# create_app().run(debug=True)
