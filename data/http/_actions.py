from ._client import httpClient
from asyncio import sleep, create_task,Queue
from inspect import isasyncgenfunction
from typing import Union
import time as t
from util import delayed_round_robin

def _q():
    q = Queue(maxsize=1)
    q.put_nowait(True)
    return q

_domain_limiter = {'www.sec.gov':_q(),
                   }
#next time do it like refinitiv _request
async def yield_txt(links:Union[str,aiter,iter],r_delay:float=.101,dlimit=True,decode_default="latin-1"):
    client = httpClient()
    if type(links)==str:
        fl=links
        lim = _domain_limiter.get(_domain_getter(fl), None)
        if lim is not None:
            if dlimit:
                if lim.empty(): await lim.get()
                else: lim.get_nowait()
            create_task(_lim_ender(lim,r_delay))
        ltx=await _get_link_txt(client, fl)
        yield ltx
    #assuming links come from the same domain per function
    elif isasyncgenfunction(links):
        #tm = t.time()
        #this feels wack even though it should work?
        if dlimit:
            fl = await anext(links)
            lim = _domain_limiter.get(_domain_getter(fl),None)
            if lim is not None:
                if lim.empty(): await lim.get()
                else: lim.get_nowait()
            async def gr():
                yield _get_link_txt(client, fl)
                async for i in links:
                    yield _get_link_txt(client, i)
                #delay handled by roundrobin
                if lim is not None: yield _lim_ender(lim)
        else:
            async def gr():
                li=''
                async for i in links:
                    yield _get_link_txt(client, i)
                    li=i
                lim = _domain_limiter.get(_domain_getter(li), None)
                if lim is not None:
                    yield _lim_ender(lim)
        for n in delayed_round_robin(gr(),delay=r_delay,isasync=True):
            res = await n
            tr = type(res)
            if tr == bytes and decode_default is not None:
                res = res.decode(decode_default)
            yield res
    else:
        if dlimit:
            links = iter(links)
            fl = next(links)
            lim = _domain_limiter.get(_domain_getter(fl), None)
            if lim is not None:
                if lim.empty(): await lim.get()
                else: lim.get_nowait()
            def gr():
                yield _get_link_txt(client, fl)
                print(fl)
                for i in links:
                    yield _get_link_txt(client, i)
                    print(i)
                if lim is not None: yield _lim_ender(lim)
        else:
            def gr():
                li=''
                for i in links:
                    yield _get_link_txt(client, i)
                    li=i
                lim = _domain_limiter.get(_domain_getter(li), None)
                if lim is not None:yield _lim_ender(lim)
        for n in delayed_round_robin(gr(),delay=r_delay,isasync=False):
            res= await n
            tr = type(res)
            #expecting always bytes
            if tr==bytes and decode_default is not None:
                res= res.decode(decode_default)
            yield res

async def _get_link_txt(client, link):
    async with await client.get(link) as res:
        return await res.read()

async def _lim_ender(lim,slp=0.):
    if slp>0.:await sleep(slp)
    lim.put_nowait(True)

async def yield_soup(links:Union[str,aiter,iter],r_delay:float=0):
    pass
    return yield_txt(links,r_delay) #cover in soup

async def get_text(link:str):
    return await anext(yield_txt(link))


async def _domain_waiter(lim):
    if lim.empty():
        await lim.get()


def _domain_getter(link:str):
    p=link.find('://')
    p=p+3 if p!=-1 else 0
    np=link.find('/', p)
    print(f'Domain found: {link[p:np]}')
    return link[p:np]