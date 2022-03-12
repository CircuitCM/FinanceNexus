import re
from collections import defaultdict

def sub_strs(stri:str,sreg,ereg):
    fl = len(sreg)
    ll=len(ereg)
    fp=stri.find(sreg,0)
    while fp!=-1:
        lp = stri.find(ereg,fp+fl)
        yield stri[fp+fl:lp]
        fp=stri.find(sreg,lp+ll)

def subs_str(stri:str,sreg:list|str,ereg:list|str):
    if type(sreg)==str:
        fl = len(sreg)
        fp = stri.find(sreg, 0)
        if fp == -1: return None
    else:
        fp=0
        fl=0
        for i in sreg:
            fl=len(i)
            fp=stri.find(i,fp)
            if fp==-1:return None
            fp+=fl
    if type(ereg)==str:
        lp = stri.find(ereg, fp+fl)
        if lp == -1: return None
    else:
        lp = stri.find(ereg[0], fp+fl)
        if lp == -1:return None
        for i in ereg[1:]:
            #ll = len(i)
            lp = stri.rfind(i,0, lp)
            if lp == -1: return None
    return stri[fp:lp]


def keyed_conversion(dtt:dict[str,list],dc:dict[str,tuple]):
    for k,v in dtt.items():
        cv=dc.get(k,(lambda x:x,''))
        nv=[_tr(cv,vt) if vt is not None else cv[1] for vt in v]
        if len(v)==1 and type(cv[1]) is not list:
            dtt[k]=nv[0]
        else:
            dtt[k]=nv

def _tr(cv,v):
    try:
        return cv[0](v)
    except:
        return cv[1]









