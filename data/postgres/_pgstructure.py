from types import NoneType

from ._client import pgClient,Connection
from ._pgdata import connect_wrapper
from datetime import date, datetime
from typing import Union

async def execute(name:str):
    await pgClient().execute(name)

async def executemany(name:str,args, timeout=None):
    await pgClient().executemany(name, args, timeout=timeout)

@connect_wrapper
async def create_index(name,table,con:Connection,ind_type='',column=''):
    if ind_type=='':
        ind = f'CREATE INDEX {name} ON {table} ({column});'
    else:
        ind = f'CREATE INDEX {name} ON {table} USING {ind_type} ({column});'
    if con is None:
        await execute(ind)
    else:
        await con.execute(ind)


@connect_wrapper
async def drop_table(name,con:Connection):
    await con.execute(f'DROP TABLE IF EXISTS {name};')


@connect_wrapper
async def lookup_table(table:str,schema:str='public',con:Connection=None):
    return await con.fetch(f'''
    SELECT
        a.attname as "Column",
        pg_catalog.format_type(a.atttypid, a.atttypmod) as "Datatype"
    FROM
        pg_catalog.pg_attribute a
    WHERE
        a.attnum > 0
        AND NOT a.attisdropped
        AND a.attrelid = (
            SELECT c.oid
            FROM pg_catalog.pg_class c
                LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relname = '{table}'
				AND n.nspname='{schema}'
                AND pg_catalog.pg_table_is_visible(c.oid)	
        );
    ''')


_TYPE_CONV={int:'integer',date:'date',datetime:'timestamp',float:'float',str:'text'}
_CONV_TYPE={v:k for k,v in _TYPE_CONV.items()}
_TYPE_CONV|={NoneType:'text',None:'text',list:'list'}

def _get_t_conv():
    return _TYPE_CONV

def _sample_types(columns:set,sample:dict):
    typs={}
    for i in columns:
        spp=sample.get(i,None)
        if spp is None:continue
        tp = type(spp)
        r=_TYPE_CONV.get(tp,0)
        if r==0: raise 'Unkown type'
        if r =='list':
            r = _g_t0(spp)+'[]'
        typs[i]=r
    return typs

def _g_t0(lt:tuple|list):
    tp =type(lt[0])
    r = _TYPE_CONV.get(tp, 0)
    if r == 0: raise 'Unkown type'
    if r is None:
        res=_g_t0(lt[0])
        return res+'[]'
    else:
        return r


def default_value_formatter(obj):
    tp = type(obj)
    if tp == str:
        try:return int(obj)
        except:
            try: return float(obj)
            except:
                try: return str(obj)
                except: return None
    else:
        try:
            ln=len(obj)
        except:
            return obj
        try:return [int(i) for i in obj]
        except:
            try:return [float(i) for i in obj]
            except:
                try:return [str(i) for i in obj]
                except:
                    return None


class TableFormat():

    __slots__ = ('table_name', 'columns', 'sample','types','table_called','keys','constraints')

    def __init__(self,table_name:str=None,columns:dict|set=None,sample:dict=None,keys:dict=None,constraints:set=None):
        #lazy
        table_name=table_name.replace('-','_').replace('/','_').replace('\\','_').replace('.','_').replace(',','_').replace(' ','_')
        self.table_name: str = '_'+table_name if table_name[0].isdigit() else table_name
        #if columns is dict assume manually entered types
        if type(columns) == dict:
            self.columns:set={*columns.keys()}
            self.types:dict=columns
            self.sample:dict= {}
        else:
            self.columns:set = {*sample.keys()} if columns is None else columns
            self.types:dict={}
            self.sample:dict = sample
        self.table_called:bool=False
        self.keys:dict=keys if keys is not None else {}
        self.constraints:set=constraints if constraints is not None else set()

    def alter_by_sample(self,sample:dict,dropping=False)->str|None:
        #old sample types take priority in case of manual setting
        stps ={*sample.keys()}
        ntps = stps - self.columns
        if len(ntps)==0: return None
        tps = _sample_types(ntps, sample)
        self.sample = sample | self.sample  # old sample types take priority in case of manual setting
        self.columns |= ntps
        self.types|=tps
        als=[]
        als.append(f'ALTER TABLE {self.table_name}')
        for k,v in tps.items():
            als.append(f' ADD COLUMN {k} {v}')
            als.append(f',')
        als.pop()
        als.append(';')
        return ''.join(als)

    def format_n_check(self,sample:dict,pre_conditioned=False,formatter=default_value_formatter,alter_type=False):
        #will try to format by tables types of existing columns, if fails will throw error/cancel, assumes depth of arrays are just 1.
        #if unkown columns exist will use the default conversion procedure for the columns
        #for the future if using dataframes or other maybe make wrapper class
        if not pre_conditioned:
            #assumes list of depth one only
            for k,v in sample.items():
                tp=self.types.get(k,None)
                if tp is None:
                    fmt = formatter(v)
                    if fmt is None: raise f"Couldn't format value {k}, data type {type(v)} is unkown."
                    else:sample[k]=fmt
                elif '[]' in tp:
                    nt = _CONV_TYPE.get(tp[:tp.find('[]')],None)
                    if nt is None: print("Shouldn't be possible.")
                    #for performance ignore if type string
                    if nt is not str:
                        try: sample[k]=[nt(i) for i in v]
                        except: raise f"Couldn't format value {k}, data check failed."
                else:
                    nt = _CONV_TYPE.get(tp, None)
                    if nt is None: print("Shouldn't be possible.")
                    # for performance ignore if type string
                    if nt is not str:
                        try:sample[k] = nt(v)
                        except:raise f"Couldn't format value {k}, data check failed."
        else:
            typs = _sample_types(self.columns,sample)
            for k,v in typs.items():
                if k in self.types:
                    if not self.types[k]==v:
                        s=f"Pre-conditioned sample does not match tables column {k} : [{self.types[k]}, {v}]"
                        print(s)
                        raise s


            # if not all(self.types[k]==v if k in self.types else True for k,v in typs.items()):
            #     raise "Pre-conditioned sample does not match tables column"
        return self.alter_by_sample(sample)

    def create_table_template(self, keys:dict=None, constraints: list | set=None)->str|None:
        self.table_called=True
        tbls=[]
        tbls.append(f'CREATE TABLE IF NOT EXISTS {self.table_name}(')
        #order needs to be preserved for this one
        tps=_sample_types(self.columns, self.sample)
        if len(self.types)==0:self.types|= {k:tps[k] for k in self.sample.keys()}
        if len(self.types)==0: return None
        if keys is not None: self.keys|=keys
        if constraints is not None: self.constraints|=set(constraints)
        for nm,tp in self.types.items():
            v=self.keys.get(nm,None)
            tbls.append(f'{nm} {tp}{f" {v}" if v is not None else ""}')
            tbls.append(', ')
        for i in self.constraints:
            tbls.append(i)
            tbls.append(', ')
        tbls.pop() #removes last comma
        tbls.append(');')
        tb=''.join(tbls)
        return tb

    def insert_template(self, ignore_conflict=True):
        s=f'insert into {self.table_name}({",".join(i for i in self.types.keys())}) '\
        f'VALUES ({",".join(f"${i}" for i in range(1,len(self.columns)+1))}){" ON CONFLICT DO NOTHING" if ignore_conflict else ""};'
        return s

    def fetch_template(self,elements:str='*',conditions:str=None):
        if conditions is None:
            s=f'select {elements} from {self.table_name};'
        else:
            s=f'select {elements} from {self.table_name} where {conditions};'
        return s

    def row_update_template(self,where:str):
        return f'update {self.table_name}({",".join(i for i in self.types.keys())}) = ({"".join(f"${i}" for i in range(1,len(self.columns)+1))}) where {where};'

    def partial_update_template(self):
        pass
        #implement when needed

    def format_row(self,data:dict):
        return (data.get(i,None) for i in self.types.keys())

    def format_rows(self,datas:iter):
        for data in datas:
            yield tuple(data.get(i,None) for i in self.types.keys())

    async def aformat_rows(self, datas: aiter):
        async for data in datas:
            yield (data.get(i, None) for i in self.types.keys())