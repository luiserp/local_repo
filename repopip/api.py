import logging
import webbrowser
from flask import Flask
from repopip.util import filesize, url
from repopip import site, simple
from repopip.local_repo.repo import Repo
from werkzeug.serving import make_server

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'repopip.sqlite'),
    )
    repo = Repo()

    app.add_template_filter(filesize)
    app.add_template_filter(url)

    app.register_blueprint(site.bp)
    app.register_blueprint(simple.create_bp(repo))

    return app

def main():
    app = create_app()
    log = logging.getLogger('werkzeug')
    log.disabled = True 
    try:
        srv = make_server("0.0.0.0", 5000, app, threaded=True)
        print("Server on http://127.0.0.1:5000")
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()

if __name__ == "__main__":
    main()