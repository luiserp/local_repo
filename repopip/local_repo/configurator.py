from pathlib import Path
import os
import platform


OS_DIC = {
    'Windows': {
        'Global': Path("C:").joinpath('/','ProgramData', 'pip'),
        'User': Path().home().joinpath("pip"),
        'File': 'pip.ini'
    },
    'Linux': {
        'Global': Path("/").joinpath('etc'),
        'User': Path().home().joinpath(".config", "pip"),
        'File': 'pip.conf'
    }
}


class Configurator:

    OS = OS_DIC.get(platform.system())

    def __init__(self, level = '', configuration = ''):
        self.level = level
        self.configuration = configuration 
        if(level != ''):
            self.PATH : Path = self.OS.get(level)            
            try:
                if(not self.PATH.exists()):
                    os.makedirs(self.PATH)
            except OSError:
                print(f"CONFIG ROUTE NOT WIRKING {self.PATH}")

        # print(self.PATH)

    def config(self):
        try:
            with open(self.PATH.joinpath(self.OS.get('File')), 'w') as f:
                if(f.writable()):
                    f.writelines(self.configuration)
                    return True
                return False
        except:
            return False


    def searchConfigs(self):
        configs = []
        for l, p in self.OS.items():
            path = Path(p)
            if( path.joinpath(self.OS.get('File')).exists() and os.path.getsize(path.joinpath(self.OS.get('File'))) != 0 ):
                configs.append((l, path.__str__()))
        return configs