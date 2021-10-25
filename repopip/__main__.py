from repopip import create_app
from dotenv import load_dotenv
load_dotenv(override=True)

create_app().run(debug=True)
