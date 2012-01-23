
SSPB - Super Simply Python Blog
===============================

!!! NOTE: this is not yet in a working state !!!

The main idea of SSPB is that you write you blog posts in markdown
files, and use this script to convert those files, along with your
template files, into HTML files that constitute your blog. 

You then copy (or rsync) those files to your server. 


Setup
-----

### Installation

This requires Python and Python-Markdown 
(see http://www.freewisdom.org/projects/python-markdown/Installation)

To set up this program, download this repository and store it wherever
you like. It is recommended, for convenience, that you add their sspb
directory to your $PATH.

### Setting up a blog

To create a new blog, make a directory for it, move into that
directory, and run

    $ sspb start <blog name>

This will create:

- settings.yaml, a settings file containing things like the blog name

- posts.dat, a file where sspb will store information about past posts

- template.html, the page template (more on modifying this later)

- posts/, the directory where you can put your markdown files for your
  posts

- blog/, the directory where the HTML files will be created

- blog/main.css, a simple CSS file for you to modify

An index page in blog/ will be created when you first run sspb new.


### Modifying template.html

If you look inside template.html, you will see things like
${title}. These are replaced by the template engine with the
appropriate value when creating the HTML pages. 

You can create any HTML structure you want, just put these tags in
where you want them:

- $(title} - title of the post or page

- ${name} - the name of the blog

- ${nav} - navigation links. These go to recent posts on the home
  page, or previous posts on entry pages.

- ${content} - the content of the page. Depending on the type of page,
this can be one post, many post summaries, or an archive listing of
links to all pages. 

- ${date} - the date of the post


### Modifying settings.yaml

These are some settings you can modify in settings.yaml. 

- blog-name
  Set the name of the blog.

- nav-max-posts
  Set this to 0 to show no posts in the nav links, or to -1 to show
  all posts.

- home-max-posts
  Set the maximum number of posts to show on the home page. 


Creating a post
---------------

To create a new post, create a file under the posts/ directory. Write
your blog post in this directory in markdown. 

The name of the file becomes the URL of the post (with spaces
replaced with underscores, and the .markdown extension removed).
The first top-level heading becomes its title.  

When you are done writing the post, run (from the blog's directory):

    $ sspb new posts/post_name.markdown <title>

This will update the contents of the blog/ directory, which you can
then copy or rsync to the server.


Removing a post
---------------

To remove an existing post, run

    $ sspb remove posts/post_name.markdown


Editing a post
--------------

If you edit an existing post, you will need to run

    $ sspb update posts/post_name.markdown [title]

in order to have the change reflected in the blog/
directory. Including a new title is optional. If none is given, the
old title will be used.  


Changing settings or the template
---------------------------------

If you updated the template or changed the settings, run

    $ sspb update

to apply the change to whole blog.






