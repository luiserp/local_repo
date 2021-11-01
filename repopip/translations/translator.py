import glob
import json

class Translator:

    def __init__(self):
        self.translations = { str: dict }
        self.loadLangages()

    def loadLangages(self):
        languages = glob.glob("repopip/translations/*.json")
        for lang in languages:
            path = lang.split('\\')
            code = path[-1].split('.')[0]
            with open(lang, encoding='utf-8') as f:
                self.translations[code] = json.load(f)

