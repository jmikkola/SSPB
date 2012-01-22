#!/usr/bin/env python

import sys
import os
from datetime import datetime
import markdown

from helper import *

def main(args):
    postPath = args[0]
    cwd = os.getcwd()

    if not os.path.exists(postPath):
        print "Could not find file:", postPath
        return

    # Get blog settings from settings.yaml
    sPath = os.path.join(cwd, 'settings.yaml')
    settings = Settings(sPath)
    
    # Add page to posts.dat
    addPost(cwd, postPath)

    # Read posts.dat
    with open('posts.dat') as inf:
        posts = inf.readlines()

    # Convert post from markdown to html
    with open(postPath) as inf:
        postText = inf.read()
    postHtml = markdown.markdown(postText)

    # Create and save page
    postName = getPostName(postPath)
    title = getTitle(postText)
    makePage(postHtml, title, postName, settings, posts)

    # Create new index page
    makeIndex(settings, posts)

    # Create new archive page
    makeArchive(settings, posts)


def addPost(cwd, post):
    ''' Adds the record of the post to the end
    of the posts.dat file '''
    time = datetime.now().strftime(dtFormat)
    line = time + ' ' + post + '\n'
    with open('posts.dat', 'a') as posts:
        posts.write(line)

def getTitle(postText):
    s = postText.strip()
    return s[:s.find('\n')]

if __name__ == '__main__':
    main(sys.argv[1:])
