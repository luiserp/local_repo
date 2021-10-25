import math

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from repopip.local_repo.repo import Repo

repo = Repo()

bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    return render_template('pages/index.html.j2', terminal = True)


@bp.route('/contact')
def contacto():
    return render_template('pages/contact.html.j2')


@bp.route('/packages')
def packages():
    repo.loadPackages()
    packages = repo.packages
    repo_len = len(packages)
    total = (repo_len, repo.total_versions)

    if(request.args.get('all')):
        return render_template('pages/packages.html.j2', packages = packages, total = total, size = repo.size)

    page = request.args.get('page')
    if(page is not None and page.isnumeric()):
         page = int(page)
    else:
        page = 1

    step = 12
    total_pages = math.ceil(repo_len/step)
    start = page * step - step
    end = start + step
    slice_packages = dict(list(packages.items())[start:end])
    data_pages = {
        'current': page,
        'total_pages':  total_pages
    }
    return render_template('pages/packages.html.j2', packages = slice_packages, total = total, size = repo.size, data_pages = data_pages)


@bp.route('/config')
def configuracion():
    return render_template('pages/configuracion.html.j2')