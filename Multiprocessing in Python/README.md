## Multiprocessing with Python 

[tutorial by sentdex](https://pythonprogramming.net/multiprocessing-python-intermediate-python-tutorial/)


### Introduction

Let us take a moment to talk about the GIL. The GIL stands for Global Interpreter Lock. What the GIL does for us is... hmm... well it serves as a sort of memory management safeguard. Sounds like a good idea I guess, but not really. The real problem is that, since the GIL has existed, people have built infrastructure around it. There are better options today, but ripping out the GIL would be catastrophic.

Alright, so the GIL is here to stay for probably a while. What's that mean? Python is single threaded. Even if you use threading, Python runs on a single CPU. If you have 4 physical cores, your computer probably thinks you have 8, and you're using 1 of those 8, including when threading. All threading really lets you do is access idle threads, and nothing more. It's not using more power, its just using idle power. If you monitor your CPU %, you might see that you're only using 10 or 15%, instead of the desired 100%, or at least close to it.

Well that stinks! What can we do?! Enter multiprocessing! Multiprocessing is a package that helps you to literally spawn new Python processes, allowing full concurrency.

This can be a confusing concept if you're not too familiar. Basically, using multiprocessing is the same as running multiple Python scripts at the same time, and maybe (if you wanted) piping messages between them. Multiprocessing just provides a nice framework for you to do this, all while running just one script at a time, so things are a bit more organized. That said, if you were to look at running processes, you will see a ton of Python processes running, as if you were running a bunch of Python scripts.

Because we're using separate processes, we're, in a sense, circumventing the GIL. Each process is subject to the GIL still, but, if you can figure out how to parallelize your process, you're going to see major performance improvements.

Okay great, so how do we launch processes?

``` python

import multiprocessing

def spawn():
    print('Spawned')

if __name__ == '__main__':
    for i in range(5):
        p = multiprocessing.Process(target=spawn)
        p.start()
        p.join()

```

If you're working in IDLE, you cannot just press F5/run. Not sure about other editors. You need to run the program in a terminal/command prompt to see the output.

```
Spawned
Spawned
Spawned
Spawned
Spawned
```

This is just about as simple as I can make it. In this case, we're spawning 5 processes, and each of the five is just printing "spawned." Nothing too crazy, but, if we just did:

``` python
while True:
    print('Spawned')
```

...Python will only use a max of 15% of my CPU (may be different for you). What if we want to dedicate 100% of our CPU to this printing!?

Also, if you want to see the output, on Windows, open the task manager, click "more details," the scroll down to "background processes." From here, go to where "Python" would be alphabetically, then you might see it. On Linux, you can use top or htop to view running processes. Chances are, 5 went way too fast, try 100.

What's happening? We're not going any quicker really, and not using more of our CPU!? The .join is the culprit here. It's waiting for the process to end. Forget it! (for now)

For me, the highest % I saw there was 40%. If I change the range to 500, I go 0 to 100 real quick. You should also clearly see a bunch of Python processes spawning in your process lists.

Remember .join if you actually need to wait on a process. If you don't need to wait, then obviously you don't want to be using it.

Okay, now that we're content with things working, let's lower the range back to 5 so we're not beating up our processors for nothing. What if we want to pass arguments to this function?

``` python


def spawn(num, num2):
    print('Spawn # {} {}'.format(num, num2))

if __name__ == '__main__':
    for i in range(5):
        p = multiprocessing.Process(target=spawn, args=(i, i+1))
        p.start()
```

Notice that comma after the arg. If it's just one argument, you need a comma at the end. If you have two or more, this wont be necessary

Notice as well that these spawns aren't in any order. We're obviously retaining what i and i+1 is, but, otherwise, the processes might complete at different times. Again, if you need order, you should make use of .join

Okay, so that's useful-ish, but only if our processes don't need to communicate much with eachother. If each of the processes can truly be their own unique environment, then this is fine. For example, maybe you're an insurance company and you have an algorithm that you want to run against customer data. You can split the customer data up into chunks by customer, and then feed unique chunks to processes that all use the algorithm and then input the results to a database, or something like that. In this way, we can share some memory, but, many times, we want to much more quickly pass values. Maybe we use the processes to run some functions, but then we want to bring back the answers to our python program to do more work and maybe launch more processes. Thus, this is a challenge we're going to be discussing in the next tutorial.

### Getting Values from Multiprocessing Processes

In the previous multiprocessing tutorial, we showed how you can spawn processes. If these processes are fine to act on their own, without communicating with eachother or back to the main program, then this is fine. These processes can also share a common database, or something like that to work together, but, many times, it will make more sense to use multiprocessing to do some processing, and then return results back to the main program. That's what we're going to cover here.

To begin, we're going to import Pool

Pool allows us to create a pool of worker processes

Let's say we want to run a function over each item in an iterable. Let's just do:

``` python
def job(num):
    return num * 2
```

Simple enough, now let's set up the processes:

``` python

from multiprocessing import Pool

def job(num):
    return num*2

if __name__ == '__main__':
    p = Pool(processes=20) # set up the Pool object, which will have 20 processes
    data = p.map(job, [i for i in range(10000)])
    p.close()
    print (data)
```

In the above case, what we're going to do is first set up the Pool object, which will have 20 processes that we'll allow to do some work.

Next, we're going to map the job function to a list of parameters ([i for i in range(20)]). When done, we close the pool, and then we're printing the result. In this case, we get:

`[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38]`

### Multiprocessing Spider Example

Here, we're going to be covering the beginnings to building a spider, using the multiprocessing library. The idea here will be to quickly access and process many websites at the same time.

We will obviously be using multiprocessing, and we're going to use the Pool so we can access the returned values from a process. Next, we're going to make use of the Beautiful Soup library for parsing the HTML. If you're not familiar with Beautiful Soup, you can check out the Beautiful Soup miniseries. We'll be using random and string to generate random strings, and requests to actually make the request and grab the source code.

Now, with a spider, we need to figure out at least where to begin. Once with a starting point, a spider simply will continue crawling around, and then networking out to other websites via links. To figure out where to begin, we're going to write a function that generates a random combination of three characters, and then we'll slap an "http://" and a ".com" and we've got probably a decent starting place, since most 3 letter .com domain names have at least something. If one doesn't no matter, since we're going to start with parsing a handful of these.



``` python

def random_starting_url():
    # generate 3 random lowercase characters
    starting = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(3))
    url = ''.join(['http://', starting, '.com'])
    return url

```

Many times, websites will have local links, basically where the link doesn't actually start with http or https, and instead it starts with a slash, like /login/. A browser knows this is really a link to http://thewebsite.com/login/, but our program wont without us telling it:

``` python
def handle_local_links(url,link):
    if link.startswith('/'):
        return ''.join([url,link])
    else:
        return link
```

Now, we need to find those links!

``` python

def get_links(url):
    try:
        resp = requests.get(url)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        body = soup.body
        links = [link.get('href') for link in body.find_all('a')]
        links = [handle_local_links(url,link) for link in links]
        links = [str(link.encode("ascii")) for link in links]
        return links

    except TypeError as e:
        print(e)
        print('Got a TypeError, probably got a None that we tried to iterate over')
        return []
    except IndexError as e:
        print(e)
        print('We probably did not find any useful links, returning empty list')
        return []
    except AttributeError as e:
        print(e)
        print('Likely got None for links, so we are throwing this')
        return []
    except Exception as e:
        print(str(e))
        # log this error 
        return []
```

In this function, we're grabbing the source code, then parsing it with Beautiful Soup. That said, there could some issues. First, the domain may not have a server. If it does have a server, maybe there's nothing on it being returned. If they do have a website, maybe they don't allow bot connections. If we are able to connect and read the source code, we might not find any links at all. Thus, we have a few exceptions to handle for

The final exception could arguably be excluded and we could further handle the explicit errors. In general, it's a bad idea to just silently move along on errors. At the very least, you might want to log the error either in a plain text file or even using something like Python's logging standard library.

Now, using multiprocessing, let's put it all together:  

``` python

def main():
    how_many = 50
    p = Pool(processes=how_many)
    parse_us = [random_starting_url() for _ in range(how_many)]
    
    data = p.map(get_links, [link for link in parse_us])
    data = [url for url_list in data for url in url_list]
    p.close()

    with open('urls.txt','w') as f:
        f.write(str(data))

if __name__ == '__main__':
    main()

```


