from ._client import pgClient, PoolAcquireContext, Connection, PoolConnectionProxy
from typing import Union
from inspect import isasyncgenfunction
import asyncio as aio
from util import completion_funnel

def acquire(timeout=None)->PoolAcquireContext:
    return pgClient().acquire(timeout=timeout)

#either connection is the last required arg followed by kwargs, or its an optional arg (kwarg)
def connect_wrapper(func):
    async def _r(*args,**kwargs):
        if len(args)>0:
            pcn = args[-1]
            if type(pcn)==PoolConnectionProxy:
                cn=pcn
            else:
                cn = kwargs.get('con',0)
        else:
            cn=None
        if cn is or cn==0:
            async with acquire() as nn:
                # async with con.transaction():
                return await func(*[*args,nn],**kwargs)
        else:
            return await func(*args,**kwargs)
    return _r


async def _release(connection, timeout=None):
    await pgClient().release(connection,timeout=timeout)


#when data query is huge, may help to keep memory overhead down
@connect_wrapper
async def yield_rows(c_text:Union[str,iter,aiter],con:Connection,prepare=None):
    #prepare is kinda pointless with asyncpg doing it
    if prepare is None:
        async with con.transaction():
            if type(c_text) is str:
                async for row in con.cursor(c_text):
                    yield row
            elif isasyncgenfunction(c_text):
                async for i in c_text:
                    async for row in con.cursor(i):
                        yield row
            else:
                for i in c_text:
                    async for row in con.cursor(i):
                        yield row
    else:
        #having prepare as a future should have no effect/make performance worse
        #assumes prepare is one string
        stmt = await con.prepare(c_text)
        async with con.transaction():
            for i in prepare:
                async for row in stmt.cursor(*i):
                    yield row

@connect_wrapper
async def yield_fetches(f_iter:Union[iter,aiter],con:Connection):
    #will yield fetches 1 by 1
    async with acquire() as con:
        async with con.transaction():
            if isasyncgenfunction(f_iter):
                async for i in f_iter:
                    f = await con.fetch(i)
                    yield f
            else:
                for i in f_iter:
                    f = await con.fetch(i)
                    yield f

async def bulk_fetch_yield(f_iter:Union[iter,aiter]):
    #assumes very high volume and (probably)different tables, as many connections as needed
    if isasyncgenfunction(f_iter):
        for d in completion_funnel(pgClient().fetch(i) async for i in f_iter):
            ans =await d
            yield ans
    else:
        for d in aio.as_completed(pgClient().fetch(i) for i in f_iter):
            ans =await d
            yield ans

