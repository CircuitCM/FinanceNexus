from data.postgres import connect_wrapper,Connection
from ._request import get_data, yield_data, ayield_data

from ._refinitiv_tables import get_refinitiv_table, new_refinitiv_table
from format import split_universe,parameters_to_fieldheader


async def fetch_as_dataframe(con: asyncpg.Connection, query: str, *args):
    stmt = await con.prepare(query)
    columns = [a.name for a in stmt.get_attributes()]
    data = await stmt.fetch(*args)
    return pandas.DataFrame(data, columns=columns)

#will take _request data and put into database, assume one field, and field headers (as fields)
async def load_data(universe, fields, parameters=None,field_name=None,closure=None,con:Connection=None):

    #check pa
    #if does, get field & parameters/field headers
    #else get
    instrument, fields, parameters, init_headers=parameters_to_fieldheader(fields,parameters)

    #check instrument as table exists




async def query_data(universe,args):
    pass


# async def tester():
#     await download_sec_filings([
#         'https://www.sec.gov/Archives/edgar/data/315066/0000315066-20-001924.txt',
#         'https://www.sec.gov/Archives/edgar/data/820743/0001140361-11-053110.txt',
#         'https://www.sec.gov/Archives/edgar/data/814149/0000814149-99-000010.txt',
#         'https://www.sec.gov/Archives/edgar/data/73956/0000950123-20-004016.txt',
#         'https://www.sec.gov/Archives/edgar/data/5108/0000899243-99-001027.txt',
#         'https://www.sec.gov/Archives/edgar/data/315080/0000315080-20-000006.txt',
#         'https://www.sec.gov/Archives/edgar/data/3520/0000930413-00-001451.txt'])
#     await http.httpClient().close()
#     await close_pgclient()
#
# if __name__=='__main__':
#     import asyncio
#     loop = asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(tester())
#         # 'https://www.sec.gov/Archives/edgar/data/315066/0000315066-20-001924.txt'
#     finally:
#         loop.close()