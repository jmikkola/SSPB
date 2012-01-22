import os
import sys
from datetime import datetime
from string import Template
import markdown

dtFormat = "%Y-%m-%d %H:%M:%S"
template = None

class Settings:
    def __init__(self, settingsPath=None):
        ''' Create a new instance of the settings class '''
        # set defaults
        self.blog_name = ''
        self.nav_max_posts = 10
        self.home_max_posts = 3
        # load settings from a file
        if settingsPath:
            self.readSettings(settingsPath)

    def readSettings(self, settingsPath):
        ''' Read in settings from a file '''
        with open(settingsPath) as fin:
            for line in fin:
                if not line.strip(): continue
                setting, value = line.split(': ', 1)
                self.set(setting, value)

    def set(self, setting, value):
        ''' Set the value of a setting '''
        if setting == 'blog-name':
            self.blog_name = value
        elif setting == 'nav-max-posts':
            self.nav_max_posts = int(value)
        elif setting == 'home-max-posts':
            self.home_max_posts = int(value)
        else:
            sys.stderr.write("Unrecognised setting type: ")
            sys.stderr.write(setting + "\n")

    def __str__(self):
        ''' Converts Settings to a string '''
        s = 'blog-name: ' + self.blog_name + '\n'
        s += 'nav-max-posts: ' + str(self.nav_max_posts) + '\n'
        s += 'home-max-posts: ' + str(self.home_max_posts) + '\n'
        return s

def getPostName(path):
    ''' Gets the post name out of the file
    name of the markdown file '''
    basename = os.path.basename(path)
    if basename.endswith(".markdown"):
        basename = basename[:-9]
    return basename.replace(' ', '_')

def getPostURL(path):
    return getPostName(path) + '.html'

def makePage(postHtml, title, postName, settings, posts):
    ''' Create a page for a blog post '''
    date = datetime.now().strftime('%I:%M %p, %B %d, %Y')
    nav = makeNav(settings, posts)
    name = settings.blog_name
    page = buildPage(postHtml, title, nav, date, name)
    savePage(page, postName)

def makeIndex(settings, posts):
    ''' Create the index (home) page '''
    content = makeIndexContent(settings, posts)
    nav = makeNav(settings, posts)
    name = settings.blog_name
    page = buildPage(content, 'Home', nav, '', name)
    savePage(page, 'index')

def makeIndexContent(settings, posts):
    ''' Create the content of the index page '''
    # Get settings
    maxPosts = settings.home_max_posts
    if maxPosts is None or type(maxPosts) != int or maxPosts < 0:
        maxPosts = 1
    # Get content
    recent = getRecentPosts(maxPosts)
    content = ''
    for postPath in recent:
        content += getPost(postPath)
    return content

def getRecentPosts(maxPosts):
    ''' Returns the path of the recent posts '''
    with open('posts.dat') as inf:
        lines = inf.readlines()
    lines = lines[-maxPosts:]
    return map(lambda l: l.rstrip()[20:], lines)

def getPost(postPath):
    ''' Returns the summary or full content of a post 
    wrapped in a link to the post '''
    return '<div class="post"> <a href="' + \
        getPostURL(postPath) + '">\n' + \
        getPostHtml(postPath) + \
        '</a></div>\n'

def getPostHtml(postPath):
    ''' Loads the post's markdown from the path
    and converts it to html '''
    with open(postPath) as inf:
        postText = inf.read()
    return markdown.markdown(postText)

def makeArchive(settings, posts):
    ''' Create the archive page '''
    content = makeArchiveContent(settings, posts)
    nav = makeNav(settings, posts)
    name = settings.blog_name
    page = buildPage(content, 'Blog archive', nav, '', name)
    savePage(page, 'archive')

def makeArchiveContent(settings, posts):
    ''' Create the content of the archive page '''
    recent = getRecentPosts(0)
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
