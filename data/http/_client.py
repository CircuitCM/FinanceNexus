from aiohttp import ClientSession, TCPConnector
import asyncio
_client = ClientSession(connector=TCPConnector(limit=100,limit_per_host=10,force_close=True,enable_cleanup_closed=True), headers={
            "Connection": "keep-alive",
            "User-Agent": "The Ithaka Group LLC cmarks@ithakagroup.com",
        }, raise_for_status=True)


def httpClient()->ClientSession:
    return _client


async def set_http_client(client:ClientSession):
    global _client
    await _client.close()
    _client = client


async def change_user_agent(agent:str):
    #will wait for all connections to finish
    await set_http_client(ClientSession(connector=TCPConnector(limit_per_host=10),headers={
            "Connection": "keep-alive",
            "User-Agent": agent,
        },raise_for_status=True))




