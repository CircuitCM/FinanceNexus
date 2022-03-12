from asyncpg import create_pool,Pool
from asyncpg.pool import PoolAcquireContext, PoolConnectionProxy
from asyncpg.connection import Connection
from asyncio import sleep,get_event_loop

_MAX_CONNECTIONS = 16


# def _init_pgclient():
#     lp=asyncio.get_event_loop()
#     return lp.run_until_complete(a_init_pgclient())

_client = create_pool(user='postgres',password='charith22?',database='Nexus Data',command_timeout=None,
                       max_cached_statement_lifetime=0,statement_cache_size=256,
                       min_size=2,max_size=_MAX_CONNECTIONS)


async def init_pgclient():
    return create_pool(user='postgres',password='charith22?',database='Nexus Data',command_timeout=None,
                       max_cached_statement_lifetime=0,statement_cache_size=256,
                       min_size=2,max_size=_MAX_CONNECTIONS)


async def _init_pgclient():
    global _client
    _client = await _client


get_event_loop().run_until_complete(_init_pgclient())



def pgClient()->Pool:
    return _client


async def set_pg_pool(pool):
    global _client
    if not _client._closing:
        while not _client._closed:
            await sleep(.25)
        _client = await pool()


async def new_pg_pool():
    await set_pg_pool(init_pgclient)

async def close_pgclient():
    await _client.close()















































