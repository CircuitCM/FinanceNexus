from data.postgres import lookup_table,TableFormat,Connection
from asyncpg import Record
from util import xml,parse
from datetime import date
from format import text_13fsections, text_table13f
from collections import defaultdict


def type_wrapper(func):
     def _r(typ:str):
        async def _n(txt:str):
            #await aio.sleep(0)
            return await func(txt,typ)
        return _n
     return _r

_EDG_TB={}

#split up to, get table, if none try castings on sample record as table default, if exists, get types from tableformat try castings if fails dont add sheet and show what/where fails
async def filing_table_verify(filing_type:str,sample:dict,con:Connection):
    #assuming sample will contain accession
    ftp=_EDG_TB.get(filing_type,None)
    if ftp is None:
        rc:list[Record]=await lookup_table(filing_type,con=con)
        #c0 will be name, c1 will be type
        if len(rc)>0:
            fmt={}
            for i in rc:
                fmt[i[0]]=i[1]
            ftp=TableFormat(filing_type,fmt,keys={'accession':'PRIMARY KEY'})
            upd = ftp.alter_by_sample(sample)
            if upd is not None: await con.execute(upd)
            _EDG_TB[filing_type]=ftp
        else:
            print(f'Creating table for new filing type {filing_type}')
            ftp=TableFormat(filing_type,sample=sample,keys={'accession':'PRIMARY KEY'})
            ctbl=ftp.create_table_template()
            if ctbl is not None: await con.execute(ctbl)
            _EDG_TB[filing_type]=ftp
    else:
        upd = ftp.alter_by_sample(sample)
        if upd is not None: await con.execute(upd)
    return ftp


async def get_filing_table(filing_type:str,con:Connection):
    ftp = _EDG_TB.get(filing_type, None)
    if ftp is None:
        rc: list[Record] = await lookup_table(filing_type, con=con)
        # c0 will be name, c1 will be type
        if len(rc) > 0:
            fmt = {}
            for i in rc:
                fmt[i[0]] = i[1]
            ftp = TableFormat(filing_type, fmt, keys={'accession': 'PRIMARY KEY'})
            _EDG_TB[filing_type] = ftp
    return ftp

async def new_filing_table(filing_type:str,sample:dict,con:Connection):
    #print(f'Creating table for new filing type {filing_type}')
    ftp = TableFormat(filing_type, sample=sample, keys={'accession': 'PRIMARY KEY'})
    ctbl = ftp.create_table_template()
    if ctbl is not None: await con.execute(ctbl)
    _EDG_TB[filing_type] = ftp
    return ftp




_N=xml.TKeys.IGNORE
_A=xml.TKeys.ADD
_I=xml.TKeys.ID
_13f={'submissionType':_N,'periodOfReport':_N,'name':_N,'street1':_N,'street2':_N,
      'city':_N,'stateOrCountry':_N,'zipCode':_N,'form13FFileNumber':_N,'filingManager':_N,
      'signatureBlock':_A,'credentials':_N,'otherManager':_A,'putCall':_I}

_proc_fields={'13F-HR':_13f,'13F-HR/A':_13f,'13F-NT':_13f,'13F-NT/A':_13f}


#--- Just 13f
_tf_xmlf = {'Report For The Calendar Year Or Quarter Ended':'reportCalendarOrQuarter',
            'Name':'signatureBlock_name','Title':'signatureBlock_title',
            'Phone':'signatureBlock_phone','Signature':'signatureBlock_signature',
            'City':'signatureBlock_city','State':'signatureBlock_stateOrCountry',
            'Date':'signatureBlock_signatureDate','Number Of Other Included Managers':'otherIncludedManagersCount',
            'Form 13F Information Table Entry Total':'tableEntryTotal',
            'Form 13F Information Table Value Total':'tableValueTotal',
            'List Of Other Included Managers':None}#infer older ones if needed
_ftps = {0:'nameOfIssuer',1:'titleOfClass',2:'cusip',3:'value',4:'sshPrnamt',5:'sshPrnamtType',
         6:'putCall',7:'investmentDiscretion',8:'otherManager',9:'Sole',10:'Shared',11:'None'}
_13f_cvfl={#'reportCalendarOrQuarter':(str,date(year=1,month=1,day=1)),
           #'signatureBlock_signatureDate':(str,date(year=1,month=1,day=1)),
           'otherIncludedManagersCount':(parse.to_int,0),
           'tableEntryTotal':(parse.to_int,0),'tableValueTotal':(parse.to_int,0),'value':(parse.to_int,0),
           'sshPrnamt':(parse.to_int,0),'Sole':(parse.to_int,0),'Shared':(parse.to_int,0),'None':(parse.to_int,0),
            'sequenceNumber':(int,0),'otherManager_cik':(int,0),'putCall':(lambda x:x,['',])}
_13f_id = {'putCall':['cusip','value']}

@type_wrapper
async def _13F(txt:str,typ:str):
    sps = xml.xml_soups(txt)
    if len(sps)==0:
        dc=defaultdict(list)
        i1=text_13fsections(txt)
        for i in range(0, len(i1) - 1, 2):
            v =_tf_xmlf.get(i1[i],None)
            if v is not None:
                dc[v].append(i1[i+1])
        #print(txt)
        for sb in parse.sub_strs(txt,'TABLE>','TABLE>'):
           # print(sb)
            tb=text_table13f(sb)
           #danger of complete or incomplete tables oh well
            for i in range(0,len(tb)):
                v=_ftps.get(i,None)
                if v is not None:
                    dc[v].extend(tb[i])
        # manually check putcall, managers
        if all(m is None for m in dc['putCall']): dc.pop('putCall')
        if all(m is None for m in dc['otherManager']): dc.pop('otherManager')
        #assumptions last 3 positions of table will always be the voting authority
        #sh/prn will almost always be seperated by just one space
        #check if not equal to twelve then check by priority
    else:
        dc = xml.get_table_layers(sps,_proc_fields[typ],_13f_id)
    parse.keyed_conversion(dc,_13f_cvfl)
    return dc,True

_extraction_procedure={'13F-HR':_13F,'13F-HR/A':_13F,'13F-NT':_13F,'13F-NT/A':_13F}

#async funcs so I can use separate processes in future.
#procedures return if preconditioned or not as second arg
#will send the extracted dict, and mark if its preconditioned
def extraction_procedure(typ:str):
    return _extraction_procedure.get(typ, _default_extraction_procedure)(typ)

@type_wrapper
async def _default_extraction_procedure(txt, typ:str):
    return txt
    #else download file compress to zip save in column, make separate zip process

#type tuple pair is preconditioned or not
_conversion_procedure={'13F-HR':_13F,'13F-HR/A':_13F,'13F-NT':_13F}


if __name__=='__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(filing_table_verify('edgar_filing_index',{}))
    except:
        pass