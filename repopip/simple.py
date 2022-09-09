from pathlib import Path
from flask import Blueprint, render_template, send_from_directory, Response, request

from repopip.local_repo import SIMPLE_PATH, repo
from repopip.util import download, scrap_pypi

repo = repo.Repo()
bp = Blueprint('simple', __name__, url_prefix='/')

@bp.route('/simple/')
def simple():
    repo.loadPackages()
    return render_template('simple/simple.html.j2', packages=repo.packages.keys())


@bp.route('/simple/<package>')
def get_package(package): 
    return send_from_directory(SIMPLE_PATH, package)


@bp.route('/simple/download/<package>')
def download_package(package): 
    href = request.args.get("href")
    return Response(download(href, package))
    

@bp.route('/simple/<package>/') # Renders the package template view
def package(package):
    packages=repo.getPackage(package)
    scrap = scrap_pypi(package, [ p.fullname for p in packages ])
    return render_template('simple/pakage.html.j2', packages=repo.getPackage(package), scrap=scrap)