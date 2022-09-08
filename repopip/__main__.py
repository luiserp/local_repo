from repopip.api import create_app
from dotenv import load_dotenv

load_dotenv(override=True)

# subprocess.run(['flask', 'run'])
create_app().run(debug=True)
