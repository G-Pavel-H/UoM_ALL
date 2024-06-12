# Exercise: Caching Simulation

This exercise asks you to explore the results of applying caching
strategies.

The exercise is *summative*: the mark given contributes to your mark
for the unit.

In the formative exercise, you will have implemented two different
strategies for caching: including Cyclic and Least Recently Used.

For this exercise, your task is to run some experiments against
implementations of caching and report the results as a ```Jupyter```
notebook.

Code is provided here for the implementations of Cyclic and LRU. This
means that you don't have to have completed the formative exercise --
although we strongly encourage you to do so. 

You have the following files:

* ```memory.py``` This is a python file that defines a memory object
```Memory```. This provides access without caching. The object is initialised with
an array of data that corresponds to the information stored. Objects of this class provide a
method ```lookup(location)``` that returns the results of a memory
lookup. There is also a method ```get_memory_hit_count()``` that returns the
number of times the actual memory has been accessed.

* ```cache.py``` This is a python file that defines caching
  strategies. There are subclasses of ```Memory``` that each redefine the
lookup function:  
```CyclicCache``` A cache using cyclic eviction  
```LRUCache``` A cache using least recently used eviction  

As an example of usage:

```
from memory import Memory
data = [1,2,3,4]
mem = Memory(data)
print(mem.lookup(1))
print(mem.lookup(1))
print(mem.lookup(1))
print(mem.get_memory_hit_count())
```

This code creates a new memory simulation that uses the default
implementation. It then prints the results of three memory accesses
followed by the number of times that the actually memory has been
accessed. This should be ```3``` as the location is read from memory
each time (no caching).

If we contrast with the following:

```
from memory import Memory
from cache import CyclicCache, LRUCache
data = [1,2,3,4]
mem = CyclicCache(data)
print(mem.lookup(1))
print(mem.lookup(1))
print(mem.lookup(1))
print(mem.get_hit_count())
```

The final result should be ```1``` as the ```CyclicCache```
implementation will read once from memory and then cache the
result. 

## The Task

Your task is to write a Jupyter notebook that runs a series of
experiments against these implementations and compares the
results. The questions that you will be looking to answer are

* How often does a lookup result in memory access?
* Are there differences between the behaviour of the strategies?

To answer these questions you will need to develop some test data
(lists of memory allocations to access) and then report on the results
of passing this test data to the objects.

A sample note book is given in ```Experiment.ipynb```. This is not an
example of good practice, and would be given a low mark. 

### Stretch Goals

The implementations of the caches can have their size adjusted. An
additional parameter ```size=N``` can be passed into the constructor
(the default is 4). You can experiment with changing this and see what
impact it has.

You could add additional caching strategies to compare. See the
instructions for the ```caching``` exercise for suggestions around
other strategies. 

You may also want to look at presenting the results in a nice way, for
example using graphs or histograms.

## Submission

Code should be submitted through ```git``` as usual. You should tag
the version that you would like to be marked with the tag
```ex1-experiment```. The notebook should be called
```CachingExperiment.ipynb``` so that it is clear what should be
marked. We expect to see a trail of commits in your log. Submissions
appearing fully formed in one commit will attract suspicions of
academic malpractice.



