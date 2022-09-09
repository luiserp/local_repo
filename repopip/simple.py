from flask import Blueprint, render_template, send_from_directory, Response, request
import requests
from repopip.local_repo import SIMPLE_PATH, repo
from repopip.util import download, scrap_pypi
from repopip.downloader import Downloader

def create_bp(repo: repo.Repo):
    bp = Blueprint('simple', __name__, url_prefix='/')

    # Lis of all of packages
    @bp.route('/simple/')
    def simple():
        repo.loadPackages()
        return render_template('simple/simple.html.j2', packages=repo.packages.keys())

    # For packages in the local repo
    @bp.route('/simple/local/<package>')
    def get_package(package): 
        return send_from_directory(SIMPLE_PATH, package)

    # If there is Inet Connection the '/simple/<package>/' route get the list from pypi
    # and redirec to this route the pacakges that aren't in the local repo 
    @bp.route('/simple/download/<package>')
    def download_package(package): 
        href = request.args.get("href")
        # Headers from requests format to Flask response format
        headers = [(k, v) for k, v in requests.head(href).headers.items()]
        d = Downloader(href, package)
        return Response(d.download(), headers=headers)
        

    @bp.route('/simple/<package>/') # Renders the package template view
    def package(package):
        repo.loadPackages()
        packages=repo.getPackages(package)
        scrap = scrap_pypi(package, [ p.fullname for p in packages ])
        return render_template('simple/pakage.html.j2', packages=packages, scrap=scrap)

    return bp