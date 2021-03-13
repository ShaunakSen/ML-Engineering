# Blogging with GitHub Pages + Jekyll

## Tips and tricks on how to create and maintain a simple blog

---

Notes on the tutorial by Bill Raymond: https://www.youtube.com/playlist?list=PLWzwUIYZpnJuT0sH4BN56P5oWTdHJiTNq

## Simple example

Say we have a repo `my_repo` and we have a [README.md](http://readme.md) file in that. If we configure GitHub st the master root folder is github pages it will serve that README file as a website

![https://i.imgur.com/VMfrS5d.png](https://i.imgur.com/VMfrS5d.png)

![https://i.imgur.com/bn3OFUZ.png](https://i.imgur.com/bn3OFUZ.png)

We can have [index.md](http://index.md) or index.html as the home pages as well

![https://i.imgur.com/8NvDaZX.png](https://i.imgur.com/8NvDaZX.png)

In a repo u can have an additional page and have your main index page link to that page. For example:

main page: [https://github.com/ShaunakSen/ML_Deployment](https://github.com/ShaunakSen/ML_Deployment)/README.md

In README.md:

```bash
[link to about section](About.md)
```

This will create a link to the about page for us

If we create the `gh-pages` branch the site automatically goes live using github pages. We do not have to do that manually

### Using Jekyll

We go into the directory of the repo we wat to work with. For me this is /ML_Deployment

We do:

```bash
PS C:\Users\shaun\Documents\my_projects\ML_Deployment> jekyll new . --force
```

This will basically setup jekyll inside this root directory that we specify with the "." and install a bunch of files for us

Next we can launch the local server like so:

```bash
PS C:\Users\shaun\Documents\my_projects\ML_Deployment> bundle exec jekyll serve
```

There we can initially already see a link, on clicking it we find:

> You’ll find this post in your `_posts` directory. Go ahead and edit it and re-build the site to see your changes. You can rebuild the site in many different ways, but the most common way is to `run jekyll serve`, which launches a web server and auto-regenerates your site when a file is updated.

We navigate to the _posts/ directory and sure enough there is the file

If we make any changes to these files, it will reflect on the frontend

All this building that we see Jekyll has done for us was automatically done when we used github pages

### Exploring the jekyll files

1. **_config.yml**

    Basically stores a bunch of settings for our site including its theme

2. **Gemfile**

    In this file it tells us to remove some lines and add some if we want to use github pages, so we have to take note of that.

    We basically comment out the line that specifies the version of jekyll to use:

    ```bash
    # gem "jekyll", "~> 4.2.0"
    ```

    We add this line:

    ```bash
    gem "github-pages", group: :jekyll_plugins
    ```

    Also we have to upgrade after updating this:

    ```bash
    To upgrade, run `bundle update github-pages`.
    ```

    But before doing that run:

    ```bash
    bundle update
    bundle install
    ```

What we have done so far is created a github repo cloned it in our local, initialized jekyll and setup a bunch of configurations. We need to get the changes back into github

Also remember how index.html → [index.md](http://index.md) → [README.md](http://readme.md) is the priority order. Since we already have an index.markdown, it will get the priority. 

index.markdown:

```bash
---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---
```

We will cover jekyll layouts later

### Config baseurl + url

In the config file we need to change:

```bash
baseurl: "/ML_Deployment" # the subpath of your site, e.g. /blog
url: "https://shaunaksen.github.io/ML_Deployment/" # the base hostname & protocol for your site, e.g. http://example.com
```

We commit all the changes and push to github

Now when we visit the URL: [https://shaunaksen.github.io/ML_Deployment/](https://shaunaksen.github.io/ML_Deployment/)  we do not see the README file, but the jekyll page

Also since we configured the urls, when we click on the post it takes us to the correct URL

### Creating the first post

Each post is located in the *posts directory and has the format: year-month-day-[post*name]