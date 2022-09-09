from setuptools import find_packages, setup

setup(
    name='repopip',
    version='0.1.1.2',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        # The following would make these functions callable as
        # standalone scripts. In this case it would add the
        # spam command to run in your shell.
        'console_scripts': [
            'repopip = repopip.api:main',
        ],
    },
    author = 'Luis Enrique Reyes Pérez',
    author_email = 'luisreyesperez98@gmail.com',
    url = 'https://github.com/luiserp/local_repo',
    download_url = 'https://github.com/luiserp/local_repo/tarball/0.1',
    keywords = ['repository', 'local', 'packages'],
    zip_safe=False,
    install_requires=[
        'flask',
        'hurry.filesize',
        'pip',
        'requests',
        'beautifulsoup4'
    ],
)