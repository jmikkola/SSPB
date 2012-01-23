#!/usr/bin/env python

import sys

from helper import *

def main(args):
    if len(args) == 0:
        updateAll()
    else:
        updatePost(args)

def updateAll():
    ''' Update all posts & pages '''
    # Load info
    settings = Settings('settings.yaml')
    posts = Posts('posts.dat')
    # Re-make post pages
    for (date,path,title) in posts.getRecent():
        makePage(path, settings, posts)
    # Re-make index and archive pages
    makeIndex(settings, posts)
    makeArchive(settings, posts)

def updatePost(args):
    ''' Update a specific post '''
    path = args[0]
    title = ' '.join(args[1:])
    # Load info
    settings = Settings('settings.yaml')
    posts = Posts('posts.dat')
    # Handle the title
    if title:
        updateTitle(posts, path, title)
        makeArchive(settings, posts)
    else:
        _, _, title = posts.getPost(path)
    # Re-create the page
    makePage(path, settings, posts)
    # Re-make index, just to be safe
    makeIndex(settings, posts)
    
def updateTitle(posts, path, title):
    posts.setTitle(path, title)
    posts.save('posts.dat')

if __name__ == '__main__':
    main(sys.argv[1:])
