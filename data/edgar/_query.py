from typing import Union
from util import parse
from data.postgres import Connection, connect_wrapper,drop_table,acquire,close_pgclient
from data import http
from format import link_accession, new_header_formats,extract_headers
from _edgar_tables import extraction_procedure, new_filing_table,get_filing_table
import datetime
import tempfile
import zipfile
from datetime import date
import asyncio as aio
import json



#CONSTRAINT con1 CHECK(accession not null AND accession UNIQUE)
# PARTITION BY RANGE (EXTRACT(YEAR FROM date_filed));
#ON CONFLICT ON CONSTRAINT (edgar_filing_index_accession_key) DO UPDATE SET cik=EXCLUDED.cik, form_type=EXCLUDED.form_type, date_filed=EXCLUDED.date_filed, accession=EXCLUDED.accession
#/\ shouldnt even be necessary
#SET CONSTRAINTS accession DEFERRED
EDGAR_INDEX='edgar_filing_index'
CIK_INDEX='cik_index'
TYPE_INDEX='filing_types'
FILING_TYPES=set()

@connect_wrapper
async def init_edgar_archive(con:Connection):
    FILING_TYPES.clear()
    await drop_table(EDGAR_INDEX,con)
    await drop_table(TYPE_INDEX,con)
    await drop_table(CIK_INDEX,con)
    tbl=f'''
        CREATE TABLE IF NOT EXISTS {EDGAR_INDEX}(
            cik         integer,
            form_type   text,
            date_filed  date,
            accession    text
        );'''
    #now I need to write it so inserts are unique in
    tbl1=f'''
        CREATE TABLE IF NOT EXISTS {CIK_INDEX}(
            cik     integer,
            title   text,
            ticker  text,         
            CONSTRAINT _unique UNIQUE (cik,title,ticker)
        );'''
    #if not await is_table(con,EDGAR_INDEX):
    #print(f'Table {EDGAR_INDEX} found not to exist,updating')
    nd={}
    # async def r():
    #     async for _ in yield_edgar_archives(nd):
    #         continue
    #     await aio.sleep(.1)
    #     return await get_cik_ids()
    await con.execute(tbl)
    await con.execute(f'CREATE TABLE IF NOT EXISTS {TYPE_INDEX}(types text);')
    #await con.copy_records_to_table(EDGAR_INDEX,records=yield_edgar_archives())
    await con.execute('''CREATE TEMPORARY TABLE _data(
            cik         integer,
            form_type   text,
            date_filed  date,
            accession    text
        );''')
    await con.copy_records_to_table('_data', records=yield_edgar_archives(nd))
    await con.execute(f'''
            INSERT INTO {EDGAR_INDEX}(cik, form_type, date_filed, accession)
            SELECT * FROM (SELECT DISTINCT ON (accession) * FROM _data) AS foo ORDER BY date_filed
        ''')
    print('Downloaded Archives')
    await aio.sleep(.1)
    #if not await is_table(con, CIK_INDEX):
    tiks = aio.tasks.create_task(get_cik_ids())
    await con.execute(
        f"CREATE INDEX IF NOT EXISTS brin_date ON {EDGAR_INDEX} USING BRIN(date_filed) WITH (autosummarize = on);")
    print('BRIN on dates completed.')
    await con.execute(
        f"CREATE INDEX CONCURRENTLY IF NOT EXISTS hash_cik ON {EDGAR_INDEX} USING HASH(cik);")
    print('HASH on cik completed.')
    #await con.execute(f"CREATE INDEX IF NOT EXISTS hash_cik ON {EDGAR_INDEX} USING HASH(cik);")
    #print('HASH on cik completed.')
    #await con.execute(f'CLUSTER {EDGAR_INDEX} USING brin_date')
    #await create_index('hash_cik',EDGAR_INDEX, 'HASH',con)
    #await create_index('brin_date', EDGAR_INDEX, 'BRIN', con)
    await con.execute(tbl1)
    jtiks = await tiks
    print('Downloaded cik index')
    jtiks=jtiks.values()
    await con.executemany(f'INSERT INTO {CIK_INDEX} (cik, title, ticker) VALUES ($1, $2, $3);',
    [(k[0],k[1],v) for k,v in ({(k,v):None for k,v in nd.items()}|{(v['cik_str'],v["title"]):v["ticker"] for v in jtiks}).items()])
    await _init_ftypes(con)
    print('Edgar archive created.')


async def _init_ftypes(con:Connection):
    await drop_table(TYPE_INDEX,con)
    await con.execute(f'CREATE TABLE IF NOT EXISTS {TYPE_INDEX}(types text);')
    await con.executemany(f'INSERT INTO {TYPE_INDEX}(types) VALUES ($1);',[(t,)for t in FILING_TYPES])


@connect_wrapper
async def repartition_edgar_archive(con:Connection):
    #await con.execute(f'CLUSTER {EDGAR_INDEX} USING brin_date;')
    await con.execute('''CREATE TABLE IF NOT EXISTS _data(
                cik         integer,
                form_type   text,
                date_filed  date,
                accession   text
            );''')
    #always order dates first
    await con.execute(f'''
                INSERT INTO _data (cik, form_type, date_filed, accession)
                SELECT * FROM (SELECT DISTINCT ON (accession) * FROM {EDGAR_INDEX}) AS foo ORDER BY date_filed
            ''')
    print('Table reordering complete.')
    #completed ordered insert
    #await con.execute("ALTER TABLE _data ADD unique_files UNIQUE INITIALLY DEFERRED (accession);")
    await con.execute(
        f"CREATE INDEX CONCURRENTLY IF NOT EXISTS brin_date ON _data USING BRIN(date_filed) WITH (autosummarize = on);")
    print('BRIN on dates completed.')
    await con.execute(
        f"CREATE INDEX CONCURRENTLY IF NOT EXISTS hash_cik ON _data USING HASH(cik);")
    print('HASH on cik completed.')
    #await con.execute(f"ALTER TABLE _data RENAME TO {EDGAR_INDEX};")
    await con.execute(f"DROP TABLE IF EXISTS {EDGAR_INDEX};")
    await con.execute(f"ALTER TABLE _data RENAME TO {EDGAR_INDEX};")
    print('Edgar archive repartitioned.')


@connect_wrapper
async def update_edgar_archive(con:Connection,yrs_b=0):
    #await _init_procedures(con)
    nd = {}
    lin = len(FILING_TYPES)
    async def r():
        ls = []
        async for i in yield_edgar_archives(nd,yrs_b=yrs_b):
            ls.append(i)
        ls.sort(key=lambda x: x[2],reverse=False)
        return ls
    yds = aio.tasks.create_task(r())
    async with con.transaction():
        y = await yds
        fd=y[0][2]
        await con.execute(f'''delete from {EDGAR_INDEX} where date_filed>=$1''',fd)
        print('Old rows deleted.')
        tiks = aio.tasks.create_task(get_cik_ids())
        await con.executemany(f'''
        insert into {EDGAR_INDEX}(cik,form_type,date_filed,accession)
        VALUES ($1,$2,$3,$4)''',y)
        print('Filings updated.')
        jtiks = await tiks
        jtiks = jtiks.values()
        tb =[(k[0],k[1],v) for k,v in ({(k,v):None for k,v in nd.items()}|{(v['cik_str'],v["title"]):v["ticker"] for v in jtiks}).items()]
        await con.executemany(f'''insert into {CIK_INDEX}(cik, title, ticker)
        VALUES ($1,$2,$3) ON CONFLICT DO NOTHING''',tb)
        print('ciks updated.')
    if lin<len(FILING_TYPES): await _init_ftypes(con)
    print('Edgar archive updated.')


async def FilingTypes(con: Connection = None):
    global FILING_TYPES
    if len(FILING_TYPES)==0:
        if con is None:
            async with acquire() as con:
                con:Connection
                rc = await con.fetch(f'SELECT types FROM {TYPE_INDEX};')
                FILING_TYPES= {r[0] for r in rc}
        else:
            rc = await con.fetch(f'SELECT types FROM {TYPE_INDEX};')
            FILING_TYPES = {r[0] for r in rc}
    return FILING_TYPES


#will pull values for corresponding date range check in python if they are the same


async def get_cik_ids():
    return json.loads(await anext(http.yield_txt("https://www.sec.gov/files/company_tickers.json")))


EDGAR_PREFIX = "https://www.sec.gov/Archives/"


def _quarterly_idx_list(since_year=1993,yrs_b:Union[None,int]=None):
    """
    Generate the list of quarterly zip files archived in EDGAR
    since 1993 until this previous quarter, if qtrs_b is not none then use quarters back instead
    """
    ty=datetime.date.today().year
    if yrs_b is not None:
        since_year=ty - yrs_b
    #logging.debug("downloading files since %s" % since_year)
    years = range(since_year, ty + 1)
    quarters = ["QTR1", "QTR2", "QTR3", "QTR4"]
    history = [(y, q) for y in years for q in quarters]
    history.reverse()

    quarter = "QTR%s" % ((datetime.date.today().month - 1) // 3 + 1)

    while history:
        _, q = history[0]
        if q == quarter:
            break
        else:
            history.pop(0)

    return [EDGAR_PREFIX + "edgar/full-index/%s/%s/master.zip" % (x[0], x[1]) for x in history]


def dsplit(st:str):
    li=0
    for i in range(0,len(st)):
        if st[i] == '|':
            yield st[li:i]
            li=i+1
    yield st[li:]


async def yield_edgar_archives(ids:dict,since_year=1993,yrs_b:Union[None,int]=None):
    lqts=_quarterly_idx_list(since_year,yrs_b)
    lk = None
    async for i in http.yield_txt(lqts,decode_default=None):
        if i is None:
            print('WARNING: expected edgar archive but not found.')
            continue
        await aio.sleep(0)
        with tempfile.TemporaryFile(mode="w+b") as tmp:
            tmp.write(i)
            with zipfile.ZipFile(tmp).open("master.idx") as z:
                await aio.sleep(0)
                #skips header
                for _ in range(0, 1):
                    z.readline()
                print(z.readline())
                for _ in range(0, 9):
                    z.readline()
                lns=z.read().decode("latin-1")
                await aio.sleep(0)
                #print(lns)
                for ln in lns.split('\r\n'):
                    if len(ln)==0:
                        break
                    #nx = dsplit(ln)
                    ls=ln.split('|')
                    try:
                        cik=int(ls[0])
                    except:
                        continue
                    if lk!=cik:
                        lk=cik
                        if cik not in ids:
                            ids[cik]=ls[1]#the name
                    #tpl =(cik,ls[2],date.fromisoformat(ls[3]),ls[4])
                    #print(tpl)
                    if ls[2] not in FILING_TYPES: FILING_TYPES.add(ls[2])
                    yield (cik,ls[2],date.fromisoformat(ls[3]),link_accession(ls[4]))

_H_FILINGS,_H_COMPS=new_header_formats()
@connect_wrapper
async def download_sec_filings(links:Union[str,aiter,iter],con:Connection):
    #assumes
    ftypes=await FilingTypes(con)
    if not (_H_FILINGS.table_called or _H_COMPS.table_called):
        await con.execute(_H_FILINGS.create_table_template())
        await con.execute(_H_COMPS.create_table_template())
    async with con.transaction():
        async for resp in http.yield_txt(links,r_delay=.101):
            hs=parse.subs_str(resp,['HEADER>','\n'],['HEADER>','\n'])
            if hs is None:
                print('No header found skipping edgar file.')
                continue
            compcols,filcols=extract_headers(hs)
            f_type,accession,cik=filcols.get('filing_type',None),filcols.get('accession',None),compcols.get('cik',None)
            if f_type is None or f_type not in ftypes:
                print('Filing type unknown, skipping edgar file.')
                continue
            if cik is None:
                print('CIK unknown, skipping edgar file.')
                continue
            if accession is None:
                print('Accession unknown, skipping edgar file.')
                continue
            dt=filcols.get('date_filed',filcols.get('period',date(1,1,1)))
            compcols['last_update']=dt
            upd=await con.fetchval(_H_COMPS.fetch_template('last_update',f'cik={cik}'))
            if upd is None:
                print(f'New company inserted {compcols.get("name",cik)}')
                await con.execute(_H_COMPS.insert_template(),*_H_COMPS.format_row(compcols))
            elif upd<dt:
                print(f'Company updated {compcols.get("name", cik)}')
                await con.execute(_H_COMPS.row_update_template(f'cik={cik}'),*_H_COMPS.format_row(compcols))
            await con.execute(_H_FILINGS.insert_template(),*_H_FILINGS.format_row(filcols))
            proc=extraction_procedure(f_type)
            ft = aio.create_task(get_filing_table(f_type,con))
            entry,precond= await proc(resp)
            #to preserve accession being first in column
            entry={'accession':accession}|entry
            # for k,v in entry.items():
            #     print(f'{k} : {v}')
            # print('----\n----')
            #continue
            ftable= await ft
            if ftable is None:
                ftable = await new_filing_table(f_type,entry,con)
                print(f'New filing table created for {f_type} : {ftable.table_name}')
            altr=ftable.format_n_check(entry,pre_conditioned=precond)
            if altr is not None:
                await con.execute(altr)
                print(f'Edgar table altered for {f_type}: ')
                print(altr)
            await con.execute(ftable.insert_template(),*ftable.format_row(entry))


async def tester():
    await download_sec_filings([
        'https://www.sec.gov/Archives/edgar/data/315066/0000315066-20-001924.txt',
        'https://www.sec.gov/Archives/edgar/data/820743/0001140361-11-053110.txt',
        'https://www.sec.gov/Archives/edgar/data/814149/0000814149-99-000010.txt',
        'https://www.sec.gov/Archives/edgar/data/73956/0000950123-20-004016.txt',
        'https://www.sec.gov/Archives/edgar/data/5108/0000899243-99-001027.txt',
        'https://www.sec.gov/Archives/edgar/data/315080/0000315080-20-000006.txt',
        'https://www.sec.gov/Archives/edgar/data/3520/0000930413-00-001451.txt'])
    await http.httpClient().close()
    await close_pgclient()

if __name__=='__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(tester())
        # 'https://www.sec.gov/Archives/edgar/data/315066/0000315066-20-001924.txt'
    finally:
        loop.close()






