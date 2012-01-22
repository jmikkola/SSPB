#!/usr/bin/env python

import sys
import os
from datetime import datetime

from helper import *

def main(args):
    postPath = args[0]
    postTitle = ' '.join(args[1:])

    # Make sure title is non-empty
    if not postTitle:
        print "No title given"
        return

    # Make sure the file exists
    if not os.path.exists(postPath):
        print "Could not find file:", postPath
        return

    # Get blog settings from settings.yaml
    settings = Settings('settings.yaml')
    
    # Get posts, add page to it, and save it
    posts = Posts('posts.dat')
    posts.add(postPath, postTitle)
    posts.save('posts.dat')

    # Create and save page
    postHtml = getPostHtml(postPath)
    postName = getPostName(postPath)
    makePage(postHtml, postTitle, postName, settings, posts)

    # Update other pages
    makeIndex(settings, posts)
    makeArchive(settings, posts)

if __name__ == '__main__':
    main(sys.argv[1:])
