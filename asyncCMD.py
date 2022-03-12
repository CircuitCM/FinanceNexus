import asyncio as aio
import sys

import uvloop
import colorama
import termcolor
import os
import traceback as tb
from aioconsole import ainput,aprint
from inspect import signature, iscoroutine


def gp(msg, i:int=1):
    clr = 'red'
    if i == 1:
        clr = 'green'
    elif i == 2:
        clr = 'yellow'
    aio.ensure_future(aprint(termcolor.colored(msg, clr)))
    #print(termcolor.colored(msg, clr))

def _tryfunc(cls: [str], func):
    cml = len(cls)
    params = signature(func).parameters
    dflts=0
    tt= len(params)
    for n in range(0,cml):
        try:
            cls[n]=int(cls[n])
        except ValueError:
            try:
                cls[n]=float(cls[n])
            except ValueError:
                pass
    for par,v in params.items():
        if '=' not in str(v):
            dflts+=1
    #if digits convert to them
    if not (dflts<=cml<=tt):
        gp("Too many or too few arguments",3)
        return
    # if iscoroutinefunction(func):
    #     return func(*cls)
    # else:
    try:
        return func(*cls)
    except:
        gp(tb.format_exc()+"<<nb-n>>You might have used an incorrect argument for the command",3)

def _find_cmd(cmds: [str], cd: dict):
    cc = len(cmds)
    cls = []
    cl= len(cmds[0])
    for ks in cd.keys():
        if cmds[0] == ks[:cl]:
            if cmds[0]==' 'or cmds[0]=='':
                continue
            #gp('chars '+cmds[0]+' reckognized as '+ ks,2)
            cls.append(ks)
    l = len(cls)
    if l == 1:
        ncd = cd.get(cls[0],cd.get(''))
        if isinstance(ncd,dict):
            return _find_cmd(cmds[1:]if cc > 1 else ['-NULL'], ncd)
        else:
            #print('here')
            return _tryfunc(cmds[1:] if cc > 0 else [], ncd)
    elif l<1:
        fnc = cd.get('')
        if fnc is not None:
            if cmds[0]!='-NULL':
                return _tryfunc(cmds, fnc)
            else:
                return _tryfunc([], fnc)
        else:
            gp("No command", 3)
            return
    else:
        gp("Couldn't identify command", 3)
        return

def _sd(d: dict,k,v):
    d.setdefault(k,v)
    return d

async def gp_delay(msg:str,delay:float,col:int = 1):
    await aio.sleep(delay)
    gp(msg,col)

async def exit_complete():
    while len(aio.all_tasks()) > 2:
        await aio.sleep(.5)
    sys.exit()

_DEFAULT_CMDS = {'echo':
            _sd({'delay': gp_delay
                 },'',gp),
        'exit':_sd({'complete': exit_complete
                 },'',exit_complete)}

def python_slash(pth: str) -> str:
    chry: [chr] = [ch for ch in pth]
    for i in range(0, len(chry)):
        if chry[i] == '\\':
            chry[i] = '/'
    return ''.join(chry)


def _get_request(cmds:dict, tx:str):
    if "'" in tx:
        ps = tx.find("'")
        tl:list = tx[:ps].split(' ')
        cap = tx[ps + 1:]
        cpp = cap.rfind("'")
        np = cap[:cpp if cpp != -1 else len(cap)]
        tl.append(np)
        tl.extend(cap[cpp+1:].split(' '))
        tl = [i for i in filter(lambda i:i!='',tl)]
    else:
        tl = tx.split(" ")
    return _find_cmd(tl, cmds)


async def _await_cmd(cmds:dict, name:str,*tasks):
    for i in tasks: aio.ensure_future(i)
    while True:
        inp = await ainput(name)
        task = _get_request(cmds, inp)
        if iscoroutine(task):
            aio.ensure_future(task)

def start_cmdline(cmds:dict,name:str,*tasks):
    colorama.init(True)
    #uvloop.install()
    aio.run(_await_cmd(cmds |_DEFAULT_CMDS, name,*tasks))