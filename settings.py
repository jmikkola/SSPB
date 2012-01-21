
class Settings:
    def __init__(self, settingsPath):
        self.settings = dict()
        if settingsPath:
            self.readSettings(settingsPath)

    def readSettings(self, settingsPath):
        with open(settingsPath) as fin:
            for line in fin:
                self.set(*(line.split(': ')))

    def set(self, key, value):
        self.settings[key] = value

    def get(self, key):
        return set.settings[key]
