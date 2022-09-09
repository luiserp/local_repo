from pathlib import Path
from typing import List
from . import SIMPLE_PATH
import os

class Version():

    def __init__(self, fullname: str, v: str, size: int):
        self.fullname = fullname
        self.v = v
        self.size = size

class Package:

    def __init__( self, name: str, versions: List[Version] = []):
        self.name = name
        self.versions: List[Version] = versions

    def __str__(self):
        return f'{self.name} - {self.versions}'

class Repo(object):

    packages = { str: Package }
    size: int = 0
    total_versions: int = 0

    def __init__(self):
        self.loadPackages()

    def getName(self, pkg: Path):
        return pkg.name.split('-')[0].lower().replace('.', '-')

    def toVersion(self, pkg: Path):
        version = pkg.name.split('-')[1].replace('.tar.gz', '').replace('.whel', '')
        return Version(pkg.name, version, os.path.getsize(pkg))

    def loadPackages(self):
        self.packages = { str: Package }
        self.size = 0
        self.total_versions = 0

        for pkg in SIMPLE_PATH.iterdir():
            name = self.getName(pkg) #Nombre de la clave del diccionario
            version = self.toVersion(pkg)
            if ( name not in self.packages.keys() ):
                self.size += version.size
                self.total_versions += 1
                self.packages[name] = Package(name, [version, ])
            else: 
                # if( version.v not in [v.v for v in self.packages[name].versions] ):
                self.size += version.size
                self.total_versions += 1
                self.packages.get(name).versions.append(version)

    def getPackages(self, name: str) -> List[Version]:
        try:
            if ( name not in self.packages.keys() ):
                name = name.replace(".","-")
                if ( name not in self.packages.keys() ):
                    name = name.replace("-","_")
            if p := self.packages.get(name):
                return p.versions
            else:
                return []
        except:
            return []