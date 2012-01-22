import os
import sys
from datetime import datetime
from string import Template
import markdown

dtFormat = "%Y-%m-%d %H:%M:%S"
template = None

class Settings:
    ''' This class stores the blog's settings. 
    It's data is stored in settings.yaml '''
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

class Posts:
    ''' This class stores information about past posts.
    It's data is stored in posts.dat '''
    def __init__(self, postsPath=None):
        ''' Creates a new instance of the Posts class '''
        self.posts = []
        if postsPath:
            self.load(postsPath)
            
    def load(self, postsPath):
        ''' Loads the list of posts from a file '''
        with open(postsPath) as inf:
            for line in inf:
                self.addLine(line.rstrip())

    def addLine(self, line):
        ''' (Internal method) Reads in a line from posts.dat '''
        dateField = line[:19]
        date = datetime.strptime(dateField, dtFormat)
        path, title = line[21:-1].split('","', 1)
        self.add(date, path, title.replace('\"', '"'))

    def add(self, path, title, date=None):
        ''' Adds an entry to the list '''
        if date is None:
            date = datetime.now()
        self.posts.append( (date,path,title) )

    def getTitle(self, postPath):
        ''' Gives the title of an existing post,
        or None if the post cannot be found '''
        for (date,path,title) in self.posts:
            if path == postPath:
                return title
        return None

    def getRecent(self, max=None):
        ''' Returns info for recent posts '''
        return self.posts[-max:] if max else self.posts
        
    def save(self, path):
        ''' Saves the current list of posts to disk '''
        self.posts.sort()
        with open(path, 'w') as outf:
            for (date,path,title) in self.posts:
                outf.write(date.strftime(dtFormat))
                outf.write(',"' + path + '","')
                outf.write(title.replace('"', '\"') + '"\n')

    def __str__(self):
        return '\n'.join(self.posts)

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
    ''' Render page for a blog post '''
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
    maxPosts = settings.home_max_posts
    content = ''.join(map(getPost, posts.getRecent(maxPosts)))
    return content

def getPost(postInfo):
    ''' Returns the summary or full content of a post 
    wrapped in a link to the post '''
    date, path, title = postInfo
    fmt = '''<div class="post">
             <a href="{0}"><h2>{1}</h2></a>
             {2}
             </div> \n'''
    return fmt.format(getPostURL(path), title, getPostHtml(path))

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
    return 'archive content goes here'

def makeNav(settings, posts, before=None):
    ''' Create the navigation links '''
    recent = posts.getRecent(settings.nav_max_posts)
    fmt = '<a href="{0}">{1}</a>\n'
    nav = fmt.format('index.html', 'Home')
    nav += fmt.format('archive.html', 'Archive')
    nav += '<hr />\n'
    for (date,path,title) in recent:
        nav += fmt.format(getPostURL(path), title)
    return nav

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
