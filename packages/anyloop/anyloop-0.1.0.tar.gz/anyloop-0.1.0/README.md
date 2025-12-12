# anyloop-project
Async Loop in Sync Function - Convert sync code to async without massive restructuring!

## How it works
For example, if we originally have a sync code like this:
```python
import time
def fetch(data):
    print(data)
    time.sleep(3)
    return data

print({
    i:fetch({
        j:fetch(j) for j in [4,5,6]
    })
    for i in [1,2,3]
})
```

We can convert it into an async version by using anyloop:
```python
from anyloop import F,G,R
import asyncio
async def fetch(data):
    print(data)
    await asyncio.sleep(3)
    return data

print(R(G({
    i:F(fetch,G({
        j:fetch(j) for j in [4,5,6]
    }))
    for i in [1,2,3]
})))
```
This requires no major changes to the existing code structure.


## Why we need this?
if we directly change it to an async version:
```python
import asyncio
async def fetch(data):
    print(data)
    await asyncio.sleep(3)
    return data

async def _temp_func():
    return {
        i:await fetch({
            j: await fetch(i+j) for j in [4,5,6]
        })
        for i in [1,2,3]
    }
print(asyncio.run(_temp_func()))
```
You will find it still works synchronously.

The official way to convert it to an async version would be:
```python
import asyncio
async def fetch(data):
    print(data)
    await asyncio.sleep(3)
    return data

async def _temp_func():
    keys = [(i,j) for i in [1,2,3] for j in [4,5,6]]
    values = await asyncio.gather(*[fetch(i+j) for i in [1,2,3] for j in [4,5,6]])
    temp = dict(zip(keys,values))
    
    keys = [i for i in [1,2,3]]
    values = await asyncio.gather(*[fetch({j:temp[m] for m in temp if m[0]==i for j in [4,5,6]}) for i in [1,2,3]])
    return dict(zip(keys,values))

print(asyncio.run(_temp_func()))
```
We are supposed to flatten the loop, which requires us to not only restructure the code but also write the loop multiple times.

It's not human-readable, not elegant, and not Pythonic.

That's why I developed this small project (anyloop) to help everyone.

## Detail Explain
We have 3 core function F, G, and R.

### F
F will await all the parameters it receives if they are coroutines, and return a new coroutine.

With F, we can covert all the sync function that need result of an async function into an async function as well.

### G
G will await all the items in a tuple/list/dict/set, and return a new coroutine.

### R
R will unwrap the final result from nested coroutines.

When an async function returns a coroutine, and that coroutine itself contains other coroutines, we end up with nested coroutines (coroutines within coroutines).

This nesting can become too complex for most use cases. Therefore, R is here to help - it will keep awaiting the coroutines until no inner coroutines remain, returning the actual final result.

### Magic Part!
With the help of F and G, we can covert every sync function and sync syntax into an async approach, while maintaining the appearance of sync code.

It solves a key challenge in async programming:

When we need the result of an awaitable, we have to use await. But when we use await, it blocks the current process, which is not what we want for concurrent execution.

Instead of using await to get results immediately, we transform the entire function into async. This allows us to await at the proper time when we want to collect all results.

Additionally, if we forget to use await in some places, R will ensure that all coroutines are properly awaited at the final stage.

## Practical Tips
So when and how should I use F, G, and R?

### F
While sync functions deal with real results, async functions always return coroutines. This difference often confuses us when converting sync functions to async. F helps here.

F will await its parameters, allowing you to use the results of async functions like sync functions, just as we normally do in sync code.

Therefore, we just need to use F on every function in the chain - it will convert the whole chain into async functions.

For example, instead of:

```python
import asyncio
async def fetch(data):
    print(data)
    await asyncio.sleep(3)
    return data

def sync_covert(data):
    return data

async def _main():
    return await fetch(sync_covert(await fetch(1)))

print(asyncio.run(_main()))
```
We can write it this way:
```python
from anyloop import F,G,R
import asyncio
async def fetch(data):
    print(data)
    await asyncio.sleep(3)
    return data

def sync_covert(data):
    return data

async def _main():
    return F(sync_covert,F(fetch,F(sync_covert,F(fetch,1))))

print(R(_main()))
```

### G
F converts sync to async but everything still runs in the same order - it doesn't accelerate execution speed.

Async functions are mainly beneficial for I/O-heavy tasks, which typically involve batch data fetching that normally we would use comprehensions or for-loops.

Traditional comprehensions or for-loops always work in a sync manner, and we want to make them async now.

G helps here.

We can still use comprehensions or for-loops, but with F's help, we quickly get a tuple/list/dict/set of coroutines.

G will asynchronously convert them into real results.

Check the previous examples - you'll notice that every tuple/list/dict/set is wrapped by a G.

### R
R is the final step - it converts coroutines into actual results.

Anything outside R returns to the normal sync world.

## Advanced Skills - Concurrency Control
Async is not always beneficial - we have to deal with concurrency control, which isn't an issue in sync programming.

Here are two solutions:
### Semaphore
The most official way to handle this issue.

Set a Semaphore at the outermost level and attach it to the async functions that need to be controlled.

Examples can be found in demo.py.

### Using await at Middle Layers of Nested Loops
Normally we avoid using await during loops because it blocks the current process.

However, when we need to limit concurrency, this approach becomes useful.

With anyloop, simply use await before G or F at an appropriate loop level - this will split the tasks into smaller groups and control concurrency.