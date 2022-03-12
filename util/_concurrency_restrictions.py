import asyncio as aio
from inspect import isasyncgenfunction
from typing import Union
import time as t
async def _r_delay(afunc,delay:float):
    await aio.sleep(delay)
    return await afunc
#--- all functions below return what ever completes first

def delayed_round_robin(gen:Union[aiter,iter],delay:float=0.101,batch:int=1,isasync:bool=True):
    if isasync:
        async def n(bt:int=batch):
            ti = 0.
            tm = t.time()
            async for g in gen:
                yield _r_delay(g, ti)
                bt-=1
                if bt==0:
                    bt=batch
                    tn = t.time()
                    ti += tm + delay*batch - tn
                    tm = tn
        return completion_funnel(n())
    else:
        bt=batch
        ti = 0.
        tm = t.time()
        ls =[]
        for g in gen:
            ls.append(_r_delay(g, ti))
            bt -= 1
            if bt == 0:
                bt = batch
                tn = t.time()
                ti += tm + delay * batch - tn
                tm = tn
        return aio.as_completed(ls)


def completion_funnel(gen:aiter,timeout=None):
    #what I want, as the tasks come in want them to be launched while simultaneously yielding whatever comes out
    #how it will be done: return a sync iterator func while launching a aio.ensure future
    #---modified from asyncio.as_completed
    done = aio.queues.Queue()
    cont = [True,]
    todo=set()

    def _on_completion(f):
        if not todo:
            return  # _on_timeout() was here first.
        todo.remove(f)
        done.put_nowait(f)
        if not todo and timeout_handle is not None:
            timeout_handle.cancel()

    def _on_timeout():
        for f in todo:
            f.remove_done_callback(_on_completion)
            done.put_nowait(None)  # Queue a dummy value for _wait_for_one().
        todo.clear()  # Can't do todo.remove(f) in the loop.

    async def g():
        async for f in gen:
            ft = aio.ensure_future(f)
            todo.add(ft)
            ft.add_done_callback(_on_completion)
        cont[0]=False
    aio.create_task(g())
    timeout_handle = None
    if timeout is not None:
        timeout_handle = aio.get_event_loop().call_later(timeout, _on_timeout)

    async def _wait_for_one():
        f = await done.get()
        if f is None:
            # Dummy value from _on_timeout().
            raise aio.exceptions.TimeoutError
        return f.result()  # May raise f.exception().

    while cont[0] or todo:
        #have to await these
        yield _wait_for_one()



