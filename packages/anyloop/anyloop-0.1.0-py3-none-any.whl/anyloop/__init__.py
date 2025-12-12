'''
Async loop in Sync Function.
'''
import asyncio

async def F(func,*args,**kwargs):
    new_args = []
    for arg in args:
        new_args.append(await arg if asyncio.iscoroutine(arg) else arg)
    new_kwargs = {}
    for kwarg in kwargs:
        new_kwargs[kwarg] = await kwargs[kwarg] if asyncio.iscoroutine(kwargs[kwarg]) else kwargs[kwarg]
    if asyncio.iscoroutinefunction(func):
        return await func(*new_args,**new_kwargs)
    return func(*new_args,**new_kwargs)

async def G(tasks):
    def check(data):
        return asyncio.iscoroutine(next(iter(data)))
    if type(tasks) == dict:
        new_dict = []
        for v in [
            tasks.keys(),
            tasks.values(),
        ]:
            data = await asyncio.gather(*v) if check(v) else v
            if check(data):
                data = await G(data)
            new_dict.append(data)
        return dict(zip(*new_dict))

    result = type(tasks)(await asyncio.gather(*tasks))
    return await G(result) if check(result) else result

def R(data):
    async def await_result(task):
        if asyncio.iscoroutine(task):
            return await await_result(await task)
        return task
    return asyncio.run(await_result(data))
