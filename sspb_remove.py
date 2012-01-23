#!/usr/bin/env python

import sys
import os

from helper import *

def main(args):
    if len(args) != 1:
        return print_usage()

    # Check with user about removing the post
    path = args[0]
    sys.stdout.write("Are you sure you want to remove ")
    sys.stdout.write("the post at " + path + "? y/[n]: ")
    s = raw_input()
    if not s in ['y', 'yes']:
        return

    # Remove from posts
    posts = Posts('posts.dat')
    posts.remove(path)
    posts.save('posts.dat')

    # Remove post from blog/ folder
    os.remove('blog/' + getPostName(path) + '.html')
    print "post removed"
    
    # Re-make archive and index
    settings = Settings('settings.yaml')
    makeIndex(settings, posts)
    makeArchive(settings, posts)

    # Check with user about deleting markdown file
    s = raw_input("Also delete the file " + path + "? y/[n]: ")
    if s in ['y', 'yes']:
        os.remove(path)
        print "path removed"
        

def print_usage():
    print "usage:"
    print "\tsspb remove posts/postname"

if __name__ == '__main__':
    main(sys.argv[1:])
