#!/usr/bin/env python

import sys
import os
import shutil

def main(args):
    folder = args[0]
    blogname = ' '.join(args[1:])
    cwd = os.getcwd()
    
    if checkExists(cwd):
        setupStructure(cwd, folder)
        createSettings(cwd, blogname)
    else:
        print "It looks like there is already a blog here."
        print "To force this operation to run, delete the "
        print "blog's existing files then re-run."

def checkExists(cwd):
    ''' Ensures that the blog has not alreay been set up '''
    tests = ['posts.dat', 'settings.yaml', 'template.html']
    for name in tests:
        path = os.path.join(cwd, name)
        if os.path.exists(path):
            return False
    return True

def setupStructure(cwd, folder):
    ''' Creates the structure of the blog '''
    createDirectories(cwd)
    makeFiles(cwd, folder)

def createSettings(cwd, blogname):
    ''' Creates the settings file '''
    path = os.path.join(cwd, 'settings.yaml')
    with open(path, 'w') as fout:
        fout.write("blog-name: " + blogname + "\n")
        fout.write("nav-max-posts: 10\n")
        fout.write("create-archive: yes\n")
        fout.write("home-max-posts: 3\n")

def createDirectories(cwd):
    ''' Creates the posts/ and blog/ directories '''
    mode = 0755
    for folder in ['posts', 'blog']:
        path = os.path.join(cwd, folder)
        if not os.path.exists(path):
            os.mkdir(path, mode)

def makeFiles(dst, folder):
    ''' Creates the template.html, posts.dat, 
    and main.css files '''
    src = os.path.join(folder, 'start_template')
    files = ['template.html', 'posts.dat', 'blog/main.css']
    for name in files:
        srcpath = os.path.join(src, name)
        dstpath = os.path.join(dst, name)
        shutil.copyfile(srcpath, dstpath)

if __name__ == '__main__':
    main(sys.argv[1:])
