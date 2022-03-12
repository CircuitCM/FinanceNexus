from pandas import DataFrame
from pandas._libs.missing import NAType
from typing import AsyncIterable
from _client import rclient_wrapper,ryield_wrapper,DataAsync,FundamentalResponse,close_session,rClient
import util
from asyncio import sleep, create_task,Queue, as_completed
import time as t
from format import DataPackage, split_universe

class Rlimit():
    #requests per second limit
    RPS = 5
    R_INTER = 1./RPS

#data volume limit per minute, dont worry about rn
class Vlimit():
    PM=52428800


class DPlimit():
    #Refinitiv datapoint limit per request
    GD_LIM = 10000 #10k datapoints per request, split requests if more
    TM_IN = 3000 #3k dp per interday timeseries request
    TM_OUT = 50000 #50K dp per >day timeseries request
    N_HEAD = 100 #news headlines per request
    N_STORY = 1 #news stories per request

class CustomLimit():
    #Custom limiters to not tempt the obnoxious black box
    UNIV = 500 #universe limiter, if number of cusips/rics/etc are greater than UNIV split to seperate get data request


_rque = Queue(maxsize=1)
_rque.put_nowait(True)

async def _lim_ender(slp=0.):
    if slp>0.:await sleep(slp)
    _rque.put_nowait(True)

@rclient_wrapper
async def get_data(universe, fields, parameters=None,field_name=None,closure=None,rclient:DataAsync=None)->FundamentalResponse:
    #nothing different
    resp,univ=await _get_data(universe, fields, parameters,field_name,closure,rclient)
    return resp



@ryield_wrapper
async def yield_data(dp:list[DataPackage],rclient:DataAsync=None)->AsyncIterable[tuple[FundamentalResponse,str|list[str]]]:
    for n in as_completed([create_task(_get_data(i.universe,
                                     i.fields,
                                     i.parameters,
                                     i.field_name,
                                     i.closure,
                                     rclient)) for i in dp]):
        res = await n
        yield res


@ryield_wrapper
async def ayield_data(dp:aiter,rclient:DataAsync=None)->AsyncIterable[tuple[FundamentalResponse,str|list[str]]]:
    async def yf():
        ts=t.time()
        async for i in dp:
            #i:DataPackage
            yield _get_data(i.universe,i.fields,i.parameters,
                            i.field_name,i.closure,rclient,
                            Rlimit.R_INTER+ts-t.time())
    for n in util.completion_funnel(yf()):
        res = await n
        yield res


async def _get_data(universe, fields, parameters=None,field_name=None,closure=None,rclient:DataAsync=None,dly=Rlimit.R_INTER)->tuple[FundamentalResponse,str|list[str]|set]:
    if _rque.empty():await _rque.get()
    else:_rque.get_nowait()
    create_task(_lim_ender(dly))
    res=await rclient.get_data(universe,fields,parameters,field_name,closure)
    return res, universe




