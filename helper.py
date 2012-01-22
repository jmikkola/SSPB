import os
from datetime import datetime
from string import Template

dtFormat = "%Y-%m-%d %H:%M:%S"
template = None

class Settings:
    def __init__(self, settingsPath=None):
        ''' Create a new instance of the settings class '''
        self.settings = dict()
        if settingsPath:
            self.readSettings(settingsPath)

    def readSettings(self, settingsPath):
        ''' Read in settings from a file '''
        with open(settingsPath) as fin:
            for line in fin:
                self.set(*(line.split(': ')))

    def set(self, key, value):
        ''' Set the value of a setting '''
        self.settings[key] = value

    def get(self, key):
        ''' Retrieve the value of a setting '''
        if key in self.settings:
            return self.settings[key]
        return None


def getPostName(path):
    ''' Gets the post name out of the file
    name of the markdown file '''
    basename = os.path.basename(path)
    if basename.endswith(".markdown"):
        basename = basename[:-9]
    return basename.replace(' ', '_')

def makePage(postHtml, title, postName, settings, posts):
    date = datetime.now().strftime('%I:%M %p, %B %d, %Y')
    nav = makeNav(settings, posts)
    name = settings.get('blog-name')
    values = {
        'content': postHtml,
        'title':   title,
        'nav':     nav,
        'date':    date,
        'name':    name,
    }
    page = getTemplate().safe_substitute(values)
    savePage(page, postName)

def makeIndex(settings, posts):
    pass

def makeArchive(settings, posts):
    pass

def makeNav(settings, posts, before=None):
    return 'nav goes here'

def getTemplate():
    global template
    if template is None:
        with open('template.html') as inf:
            template = Template(inf.read())
    return template

def savePage(page, name):
    with open('blog/' + name + '.html', 'w') as outf:
        outf.write(page)
