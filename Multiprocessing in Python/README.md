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

