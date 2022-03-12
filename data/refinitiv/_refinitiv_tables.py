from data.postgres import lookup_table,TableFormat,Connection
from asyncpg import Record

_REFIN_TB={}

# async def table_verify(filing_type:str,sample:dict,con:Connection):
#     #assuming sample will contain accession
#     ftp=_INS_TB.get(filing_type,None)
#     if ftp is None:
#         rc:list[Record]=await lookup_table(filing_type,con=con)
#         #c0 will be name, c1 will be type
#         if len(rc)>0:
#             fmt={}
#             for i in rc:
#                 fmt[i[0]]=i[1]
#             ftp=TableFormat(filing_type,fmt,keys={'accession':'PRIMARY KEY'})
#             upd = ftp.alter_by_sample(sample)
#             if upd is not None: await con.execute(upd)
#             _INS_TB[filing_type]=ftp
#         else:
#             print(f'Creating table for new filing type {filing_type}')
#             ftp=TableFormat(filing_type,sample=sample,keys={'accession':'PRIMARY KEY'})
#             ctbl=ftp.create_table_template()
#             if ctbl is not None: await con.execute(ctbl)
#             _INS_TB[filing_type]=ftp
#     else:
#         upd = ftp.alter_by_sample(sample)
#         if upd is not None: await con.execute(upd)
#     return ftp

async def get_refinitiv_table(instrument:str, con:Connection):
    ftp = _REFIN_TB.get(instrument, None)
    if ftp is None:
        rc: list[Record] = await lookup_table(instrument, con=con)
        # c0 will be name, c1 will be type
        if len(rc) > 0:
            fmt = {}
            for i in rc:
                fmt[i[0]] = i[1]
            ftp = TableFormat(instrument, fmt, keys={'accession': 'PRIMARY KEY'})
            _REFIN_TB[instrument] = ftp
    return ftp

async def new_refinitiv_table(instrument:str, sample:dict, con:Connection):
    #print(f'Creating table for new filing type {filing_type}')
    ftp = TableFormat(instrument, sample=sample, keys={'accession': 'PRIMARY KEY'})
    ctbl = ftp.create_table_template()
    if ctbl is not None: await con.execute(ctbl)
    _REFIN_TB[instrument] = ftp
    return ftp