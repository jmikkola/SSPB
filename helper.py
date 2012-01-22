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
    ''' Create a page for a blog post '''
    date = datetime.now().strftime('%I:%M %p, %B %d, %Y')
    nav = makeNav(settings, posts)
    name = settings.get('blog-name')
    page = buildPage(postHtml, title, nav, date, name)
    savePage(page, postName)

def makeIndex(settings, posts):
    ''' Create the index (home) page '''
    content = makeIndexContent(settings, posts)
    nav = makeNav(settings, posts)
    name = settings.get('blog-name')
    page = buildPage(content, 'Home', nav, '', name)
    savePage(page, 'index')

def makeIndexContent(settings, posts):
    ''' Create the content of the index page '''
    return 'index content goes here'

def makeArchive(settings, posts):
    ''' Create the archive page '''
    content = makeArchiveContent(settings, posts)
    nav = makeNav(settings, posts)
    name = settings.get('blog-name')
    page = buildPage(content, 'Blog archive', nav, '', name)
    savePage(page, 'archive')

def makeArchiveContent(settings, posts):
    ''' Create the content of the archive page '''
    return 'archive content goes here'

def makeNav(settings, posts, before=None):
    ''' Create the navigation links '''
    return 'nav goes here'

def buildPage(content, title, nav, date, name):
    ''' Builds a page by putting the parameters 
    into the template '''
    values = {
        'content': content,
        'title':   title,
        'nav':     nav,
        'date':    date,
        'name':    name
    }
    return getTemplate().safe_substitute(values)

def getTemplate():
    ''' Returns the template object '''
    global template
    if template is None:
        with open('template.html') as inf:
            template = Template(inf.read())
    return template

def savePage(page, name):
    ''' Saves the page to a file '''
    with open('blog/' + name + '.html', 'w') as outf:
        outf.write(page)
