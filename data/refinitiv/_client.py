import refinitiv.dataplatform as rdp
from refinitiv.dataplatform.content.data_grid._fundamental_class import Fundamental,FundamentalResponse


class DataAsync():
    __slots__ = ('fundamental',)

    def __init__(self,session):
        self.fundamental:Fundamental=Fundamental(session=session)

    async def get_data(self, universe, fields, parameters=None,field_name=None,closure=None)->FundamentalResponse:
        return await self.fundamental._get_data_async(universe,fields,parameters,field_name,closure)


_r_client = None
_r_sess:rdp.Session= None


def rClient()->DataAsync:
    global _r_client,_r_sess
    if _r_client is None:
        ses=rdp.open_platform_session(
            '2a2f8e4443b44860be25d4cfc607b1654e4dfc74',
            rdp.GrantPassword(
                'acolyer@ithakagroup.com',
                'Scamper1'))
        _r_client = DataAsync(ses)
        _r_sess=ses
    return _r_client

#must be used to close session open new with rClient (throw out old DataAsync)
def close_session():
     _r_sess.close()
     global _r_client
     _r_client=None

#either client is the last required arg or its one of the kwargs
def rclient_wrapper(func):
    async def _r(*args,**kwargs):
        cn=kwargs.get('rclient',0)
        if len(args)>0:
            pcn = args[-1]
            if type(pcn)==DataAsync:
                cn=pcn
        #connection is arg in cn
        if cn ==0:
            return await func(*args,**(kwargs|{'rclient':rClient()}))
        #connection is kwarg and required
        elif cn is None:
            return await func(*args,**(kwargs|{'rclient':rClient()}))
        else:
            return await func(*args,**kwargs)
    return _r

def ryield_wrapper(func):
    async def _r(*args,**kwargs):
        if len(args)>0:
            pcn = args[-1]
            if type(pcn)==DataAsync:
                cn=pcn
            else:
                cn = kwargs.get('rclient', 0)
        else:
            cn = kwargs.get('rclient', 0)
        #0 means no argument
        if cn ==0:
            fnc= func(*[*args,rClient()],**kwargs)
        #connection is kwarg and required
        elif cn is None:
            fnc=func(*args,**(kwargs|{'rclient':rClient()}))
        else:
            fnc=func(*args,**kwargs)
        async for i in fnc:
            yield i
    return _r


