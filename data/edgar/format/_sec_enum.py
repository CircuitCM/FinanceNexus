import sys

from typing import ClassVar, Type
import re
from datetime import date, datetime
from data.postgres import _get_t_conv


class SecHeader():
    header_ref: ClassVar[dict] = {}
    company_columns = {}
    filing_columns= {}
    #reg = re.compile(r'[a-zA-Z0-9]+([\s\-][a-zA-Z0-9]+)*[><: \t]')
    #lspt = re.compile('\n+')
    rspl = re.compile(r'[>:]+[ \t]*|(?=:)[\D\W]+|\n+\s*')
    __slots__ = ('id','col_name','conv_func','col_type')
    def __init__(self,*args,col_name:str=None,conv_func:callable=str,col_type:str=None):
        self.id:list[str] = [*args]
        if col_name is None:
            self.col_name=self.id[0]
        else:
            self.col_name=col_name
        self.conv_func:callable =conv_func
        for i in self.id:
            SecHeader.header_ref[i]=self
        if col_type is None:
            tn=_get_t_conv().get(conv_func,None)
            if tn is not None:
                self.col_type=tn
            else:
                self.col_type='text'
        else:
            self.col_type=col_type

    @classmethod
    def line_get(cls,ln_str):
        #lns =cls.lspt.split()
        #vls = [*filter(lambda x: x not in {'',' '},cls.rspl.split(ln_str))]

        vls=cls.rspl.split(ln_str)
        if vls[0]=='':
            s = 1
        else:
            s=0
        for i in range(s,len(vls)-1,2):
            vs = vls[i]
            vl = cls.header_ref.get(vs,None)
            if vl == None:
                vs=vs.upper()
                print(f'Warning found non-matching header {vs}, trying all.')
                for k,v in cls.header_ref.items():
                    if k in vs:
                        print(f'found {k}')
                        vl=v
                        break
            if vl == None:
                print(f'Unkown header item found {vs}: {vls[i+1]}')
                continue
            #if vls[i+1]
            #print([vs,vls[i+1]])
            yield vl,vls[i+1]
        #first try dict get for first to last, then in get first last

    @classmethod
    def get_columns(cls):
        return cls.company_columns,cls.filing_columns

    def line_value(self,ln:str):
        pass

def _num_datetime(st:str):
    try:
        return datetime(int(st[0:4]), int(st[4:6]), int(st[6:8]), int(st[8:10]),int(st[10:12]),int(st[12:14]))
    except:
        return None

def _num_date(st:str):
    try:
        return date(int(st[0:4]),int(st[4:6]),int(st[6:8]))
    except:
        return None

_PRG = re.compile('\d+') #might need to change
def _sic(st:str):
    try:
        return int(_PRG.search(st).group())
    except:
        return None

def _fisc_yr(st:str):
    try:
        return f'{st[0:2]}-{st[2:4]}'
    except:
        return None


def _phone(st:str):
    try:
        return ''.join(_PRG.findall(st))
    except:
        return None

class SecHeaders():
    ACCEPTANCE_TIME = SecHeader('<ACCEPTANCE-DATETIME','ACCEPTANCE-DATETIME',col_name='time_accepted',conv_func=_num_datetime,col_type='timestamp')
    ACCESSION = SecHeader('ACCESSION NUMBER','ACCESSION',col_name='accession')
    _FILING_TYPE = SecHeader('CONFORMED SUBMISSION TYPE',col_name='filing_type')
    DOCUMENT_COUNT = SecHeader('PUBLIC DOCUMENT COUNT','DOCUMENT COUNT',col_name='document_count',conv_func=int)
    REPORT_PERIOD = SecHeader('CONFORMED PERIOD OF REPORT','PERIOD',col_name='period',conv_func=_num_date,col_type='date')
    DATE_FILED = SecHeader('FILED AS OF DATE','FILED',col_name='date_filed',conv_func=_num_date,col_type='date')
    EFFECT_DATE = SecHeader('EFFECTIVENESS DATE',col_name='effect_date',conv_func=_num_date,col_type='date')
    _gd1 = SecHeader('DATE AS OF CHANGE',col_name='date_changed',conv_func=_num_date,col_type='date')
    CONFORMED_NAME = SecHeader('COMPANY CONFORMED NAME','CONFORMED NAME',col_name='name')

    _FILER = SecHeader('FILER',col_name='ignore')
    _COMPANY_DATA = SecHeader('COMPANY DATA',col_name='ignore')
    CIK = SecHeader('CENTRAL INDEX KEY','CIK',col_name='cik',conv_func=int)
    SIC = SecHeader('STANDARD INDUSTRIAL CLASSIFICATION','SIC',col_name='sic',conv_func=_sic,col_type='integer')
    IRS_NUM = SecHeader('IRS NUMBER','IRS',col_name='irs_num',conv_func=int)
    STATE_INCORP = SecHeader('STATE OF INCORPORATION',col_name='state_incorp')
    F_YR = SecHeader('FISCAL YEAR END','YEAR END',col_name='fiscal_year',conv_func=_fisc_yr)

    _FILING_VALS = SecHeader('FILING VALUES',col_name='ignore')
    FILING_TYPE = SecHeader('FORM TYPE', col_name='filing_type')
    SEC_ACT = SecHeader('SEC ACT', col_name='sec_act')
    SEC_FILE_NUM = SecHeader('SEC FILE NUMBER', col_name='file_num')
    FILM_NUM = SecHeader('FILM NUMBER', col_name='film_num',conv_func=int)

    BUSINESS_ADR = SecHeader('BUSINESS ADDRESS', col_name='ignore')
    STREET_1 = SecHeader('STREET 1',col_name='street_1')
    STREET_2 = SecHeader('STREET 2',col_name='street_2')
    CITY = SecHeader('CITY',col_name='city')
    STATE = SecHeader('STATE',col_name='state')
    ZIP = SecHeader('ZIP',col_name='zip')
    PHONE = SecHeader('BUSINESS PHONE','PHONE',col_name='phone',col_type='text')
    MAIL_ADR = SecHeader('MAIL ADDRESS',col_name='mail_address')

    _FORMER_COMPANY = SecHeader('FORMER COMPANY',col_name='ignore')
    FORMER_NAME = SecHeader('FORMER CONFORMED NAME','FORMER NAME',col_name='former_name',col_type='text[]')
    NAME_CHANGE_DATE = SecHeader('DATE OF NAME CHANGE',col_name='name_change_date',conv_func=_num_date,col_type='date[]')
    _LAST_UPDATE = SecHeader('last update, shouldnt be found or accessed in header text',col_name='last_update',conv_func=_num_date,col_type='date')

    TO_COLLATE = {MAIL_ADR}
    TO_ARRAY = {FORMER_NAME,NAME_CHANGE_DATE}
    #NONE = SecHeader('',col_name='ignore')
    IGNORE = {_FILING_TYPE, _gd1, _FORMER_COMPANY,BUSINESS_ADR,_FILER,_COMPANY_DATA,_FILING_VALS,EFFECT_DATE}
    FOR_COMPANY = {CONFORMED_NAME,CIK,SIC,STATE_INCORP,F_YR,IRS_NUM,STREET_1,STREET_2,CITY,STATE,ZIP,PHONE,MAIL_ADR,
                   FORMER_NAME,NAME_CHANGE_DATE,_LAST_UPDATE}
    FOR_FILINGS = {ACCEPTANCE_TIME,ACCESSION,_FILING_TYPE,FILING_TYPE,SEC_ACT,SEC_FILE_NUM,REPORT_PERIOD,DATE_FILED,
                   DOCUMENT_COUNT,FILM_NUM}



def _init_columns():
    for v in SecHeader.header_ref.values():
        cn = v.col_name
        if cn=='ignore' or v in SecHeaders.IGNORE:
            continue
        if v in SecHeaders.FOR_COMPANY:
            SecHeader.company_columns[cn]=v.col_type
        if v in SecHeaders.FOR_FILINGS:
            SecHeader.filing_columns[cn]=v.col_type

_init_columns()

if __name__=="__main__":
    print(type(None))
    print(None)
    sys.exit()
    import time as t
    print(SecHeaders.CONFORMED_NAME in SecHeaders.FOR_COMPANY)
    tm = t.time()
    SecHeader.line_get('''<ACCEPTANCE-DATETIME>20190125170551
ACCESSION NUMBER:		0000056701-19-000006
CONFORMED SUBMISSION TYPE:	10-Q
PUBLIC DOCUMENT COUNT:		57
CONFORMED PERIOD OF REPORT:	20181231
FILED AS OF DATE:		20190125
DATE AS OF CHANGE:		20190125

FILER:

	COMPANY DATA:	
		COMPANY CONFORMED NAME:			KOSS CORP
		CENTRAL INDEX KEY:			0000056701
		STANDARD INDUSTRIAL CLASSIFICATION:	HOUSEHOLD AUDIO & VIDEO EQUIPMENT [3651]
		IRS NUMBER:				391168275
		STATE OF INCORPORATION:			DE
		FISCAL YEAR END:			0630

	FILING VALUES:
		FORM TYPE:		10-Q
		SEC ACT:		1934 Act
		SEC FILE NUMBER:	000-03295
		FILM NUMBER:		19543201

	BUSINESS ADDRESS:	
		STREET 1:		4129 N PORT WASHINGTON AVE
		CITY:			MILWAUKEE
		STATE:			WI
		ZIP:			53212
		BUSINESS PHONE:		4149645000

	MAIL ADDRESS:	
		STREET 1:		4129 N PORT WASHINGTON AVE
		CITY:			MILWAUKEE
		STATE:			WI
		ZIP:			53212

	FORMER COMPANY:	
		FORMER CONFORMED NAME:	KOSS ELECTRONICS INC
		DATE OF NAME CHANGE:	19721005

	FORMER COMPANY:	
		FORMER CONFORMED NAME:	REK O KUT CO INC
		DATE OF NAME CHANGE:	19680124''')
    print((t.time() - tm) * 1000.)