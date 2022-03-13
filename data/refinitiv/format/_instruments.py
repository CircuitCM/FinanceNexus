import re
from types import NoneType



class DataPackage():
    #refinitiv data fields held in class
    __slots__ = ('universe', 'fields', 'parameters','field_name','closure')

    def __init__(self,universe,fields,parameters=None,field_name=None,closure=None):
        self.universe=universe
        self.fields=fields
        self.parameters=parameters
        self.field_name=field_name
        self.closure=closure

_gsp = re.compile(r'[\w,;]+')

#doesn't support math on instruments, do that separately in sql or dataframes
def split_universe(universe, fields, parameters=None, field_name=None, closure=None):
    if type(universe)==str:
        universe=_gsp.split(universe)

    return [DataPackage([i],fields,parameters,field_name,closure) for i in universe if i!='']

#find included header fields
def _field_finder(fieldnheaders: str | list[str] | set[str]):
    t=type(fieldnheaders)
    if t==str:
        fieldnheaders= [i for i in _gsp.split(fieldnheaders) if i!='']
    elif t==set:
        fieldnheaders=[*fieldnheaders]
    field = min(fieldnheaders,key=len)
    if any(any(ill in vs for ill in ('+','-','*','/','(',')')) or field != vs[:len(field)] for vs in fieldnheaders):
        return None,None,None
    headers = {v[len(field)+1:].lower():None for v in fieldnheaders if v!=field}
    return field, fieldnheaders, headers


def _mk_param_dict(parameters:list):
    pd = {}
    for i in parameters:
        loc = i.rfind('=')
        if loc != -1 or loc != 0:
            k = i[:loc].title()
            v = i[loc + 1:].upper()
            if len(v)>0:
                pd[k] = v
    return pd

#check for parameters that will mean adding required fields
_hsp = re.compile(r'[\w,]+')
def _parameter_format(parameters: str | list[str] | dict):
    #assume frequency will default to the smallest interval so no need to add or convert
    tp = type(parameters)
    if tp == list:
        parameters = _mk_param_dict(parameters)
    elif tp == str:
        parameters = _mk_param_dict([i for i in _hsp.split(parameters) if i != ''])
    return parameters


def parameters_to_fieldheader(fields:str|list[str]|set[str],parameters:str|list[str]|dict|NoneType):
    if type(fields) not in {str,list,set} and len(fields)==0:
        print('No fields or unsupported field types.')
        return None,None
    if type(parameters) not in {str,list,dict,NoneType}:
        print('Unsupported parameter types.')
        return None,None
    #turn needed fieldheaders from parameters, eg if sdate or edate in params field.date,sdate&edate freq=C
    #fields will be converted to list if string for ease of use
    #parameters to dict
    instrument, fields, init_headers = _field_finder(fields)
    fields:list
    if instrument is None:
        print('Fields contain illegal characters or more than one instrument type, math operations not supported and one instrument per data load.')
    if parameters is not None:
        parameters = _parameter_format(parameters)
        #maybe abstract this logic later
        iss,ise='Sdate' in parameters,'Edate' in parameters
        period,colheaders,rowheaders=parameters.get('Period',None),parameters.get('Ch',None),parameters.get('Rh',None)
        if iss or ise and 'date' not in init_headers:
            init_headers['date']=None
            fields.insert(0,f'{instrument}.date')
        if period is not None:
            init_headers['period']=period
        hdrs=set()
        if colheaders is not None:hdrs|={i for i in colheaders.lower().split(';') if i!=''}
        if rowheaders is not None: hdrs |= {i for i in rowheaders.lower().split(';') if i !=''}
        if len(hdrs)>0:
            hdrs-={'rfperiod','fperiod'}
            for i in hdrs:
                if i not in init_headers:
                    init_headers[i]=None
                    fields.append(f'{instrument}.{i}')
        #row or column headers not supported attach them as field/instrument headers
        parameters.pop('Ch'),parameters.pop('Rh'),parameters.pop('Null')
    return instrument, fields, parameters, init_headers


