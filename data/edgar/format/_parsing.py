from types import NoneType

from util import xml
from data.postgres import TableFormat
from ._sec_enum import SecHeader,SecHeaders
import re

def filing_link(cik:int,ac_num:str):
    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{ac_num}.txt"

def _link_accession(link:str):
    #slower assuming not static tail
    return link[link.rfind('/')+1:link.rfind('.')]

def link_accession(link:str):
    #faster assuming static tail
    ll=len(link)
    return link[ll-24:ll-4]

def construct_filing_entry(filg:str):
    sps = xml.xml_soups(filg)
    pass


def extract_headers(hdr:str):
    #ccols,fcols=SecHeader.get_columns()
    ccols,fcols={},{}
    colk =None
    colk:SecHeader
    coll=[]
    for k,v in SecHeader.line_get(hdr):
        k:SecHeader
        ign= k in SecHeaders.IGNORE
        if colk is not None:
            if ign:
                colls=', '.join(coll)
                coll.clear()
                if colk in SecHeaders.FOR_COMPANY:
                    ccols[colk.col_name]=colls
                if colk in SecHeaders.FOR_FILINGS:
                    fcols[colk.col_name]=colls
                colk=None
            elif v!='':
                coll.append(str(k.conv_func(v)))
            #finish up coll
            #k in SecHeaders.IGNORE:continue
        elif not ign:
            if colk is None and k in SecHeaders.TO_COLLATE:
                colk=k
            elif v!='':
                if k is None or k is NoneType:
                    print(type(k))
                    print(type(v))
                v =k.conv_func(v)
                if k in SecHeaders.TO_ARRAY:
                    #because some might be in both for the future
                    if k in SecHeaders.FOR_COMPANY:
                        ls=ccols.get(k.col_name,None)
                        if ls is None:
                            ls=[]
                            ccols[k.col_name]=ls
                        ls.append(v)
                    if k in SecHeaders.FOR_FILINGS:
                        ls = fcols.get(k.col_name, None)
                        if ls is None:
                            ls = []
                            fcols[k.col_name] = ls
                        ls.append(v)
                else:
                    if k in SecHeaders.FOR_COMPANY:
                        ccols[k.col_name]=v
                    if k in SecHeaders.FOR_FILINGS:
                        fcols[k.col_name]=v
    #print('\n'.join(f'{k} : {v}'for k,v in ccols.items()))
    #print('---')
    #print('\n'.join(f'{k} : {v}' for k, v in fcols.items()))

    return ccols, fcols

_HF = re.compile(r'[ \t]{2,}') #for findalling
_FSP = re.compile(r':[ \t]*|(?=:)[\D\W]+|\n+[-\s]*') #for splitting should ignore dashes already?
def drop_corner_empty(ls:list):
    ll=len(ls)
    md=ll%2
    if ls[0]=='':
        if md==1:
            return ls[1:]
        elif ls[ll-1]=='':
            return ls[1:ll-1]
        else:
            return ls[1:]
    elif md==1:
        if ls[ll-1]=='':
            return ls[:ll-1]
    else: return ls

def text_13fsections(txt:str):
    tl=[]
    txt=txt.title()
    p=txt.find('Report For The ')
    np=txt.find('\n',p)
    if np-p>30:
        tl.extend(drop_corner_empty(_FSP.split(txt[p:np])))
    p=txt.find('Name:',txt.find('Behalf Of Reporting Manager:',np))
    np = txt.find('\nSignature',p)
    if np-p > 17:
        #tl.extend(_FSP.split(txt[p:np]))
        tl.extend(drop_corner_empty(_FSP.split(txt[p:np])))
    p=txt.find('\n',np+1)+1
    np=txt.find('\n',p)
    while np - p < 5 and np!=-1:
        p = np+1
        np = txt.find('\n', p)
    if np-p>10:
        els = _HF.split(txt[p:np])
        if len(els)<2:
            ad = txt[p:np].split(', ',maxsplit=3)
            if len(ad)==4:
                vs = ['Signature', 'City', 'State', 'Date']
                ad[2]=ad[2].upper()
                for k, v in zip(vs, ad):
                    tl.append(k)
                    tl.append(v)
        else:
            ad=els[1].split(', ')
            els[1]=ad[0]
            if len(ad)>1:
                els.insert(2,ad[1].upper())
                vs =['Signature','City','State','Date']
            else:
                vs =['Signature','City','Date']
            for k,v in zip(vs,els):
                tl.append(k)
                tl.append(v)

    p = txt.find('\n',txt.find('Report Summary:', np))+1
    np=txt.find(' (',p)
    if np==-1:
        np=txt.find('\n',txt.find('List Of Other Included Managers',p))
    if np==-1: np=len(txt)
    if np-p>100:
        tl.extend(drop_corner_empty(_FSP.split(txt[p:np])))
    return tl

_SPL = re.compile(r'<[\d\w]+>')
_HFND = re.compile(r'\s{2,}')
_SPF = re.compile(r'\S+(\s\S+)*')

#returns list of lists
def text_table13f(tbs:str,):
    tbls=[*filter(lambda x:len(x)>10,tbs.split('\n'))]
    #ms = max(len(tbls[i]) for i in range(0,9 if 9<=len(tbls) else len(tbls)))
    spos=-1
    tbl:list[list[re.Match]]=[]
    for i in range(0,12 if len(tbls)>=14 else len(tbls)):
        tbl.append([*_SPL.finditer(tbls[i])])
        if len(tbl[i])>5:
            spos=i
            break
    if spos==-1:
        nif=False
        fr=0
        for i in range(0,len(tbls)):
            if not nif:
                if tbls[i].upper().find('CUSIP')!=-1:
                    nif=True
            else:
                ut=tbls[i].upper()
                if ut.find(' SH ')!=-1 or ut.find(' PRN ')!=-1:
                    fr = i
                    break
        if fr==0: return []
        fls = _HFND.split(tbls[fr])
        df=[[] for _ in range(0,len(fls))]
        for sl in range(0, len(fls)):
            df[sl].append(fls[sl])
        for st in tbls[fr+1:]:
            fls=_HFND.split(st)
            for sl in range(0,len(fls)):
                df[sl].append(fls[sl])
        #first split shares assuming always one space apart
        nl=[i.split(' ') for i in df[4]]
        df[4]=[i[0] for i in nl]
        df.insert(5,[i[1] for i in nl])
        if len(df) < 12:
            df.insert(7, [None for _ in range(0, len(df[0]))])
        if len(df) < 12:
            df.insert(6, [None for _ in range(0, len(df[0]))])
        # if len(df)<12:
        #     df.insert(7,[None for _ in range(0,len(nl))])
        # if len(df)<12:
        #     df.insert(6, [None for _ in range(0, len(nl))])
    else:
        mn=tbl[spos][0].group().find('<')
        spl=[m.start()-mn for m in tbl[spos]]
        df=[[] for _ in range(0,len(spl))]
        for s in tbls[spos+1:]:
            n=-1
            for n in range(0,len(spl)-1):
                mt=_SPF.search(s,spl[n],spl[n+1])
                if mt is None:
                    #print(s[spl[n]:spl[n+1]])
                    df[n].append(None)
                else:
                    df[n].append(mt.group())
            mt = _SPF.search(s, spl[n+1])
            if mt is None:
                df[n+1].append(None)
            else:
                df[n+1].append(mt.group())
        if len(df) < 12:
            df.insert(6, [None for _ in range(0, len(df[0]))])
        if len(df) < 12:
            nl = [i.rsplit(' ', 1) for i in df[7]]
            df[7]=[n[0] for n in nl]
            df.insert(8, [None if len(n)<2 else n[1] for n in nl])
    if len(df)<12: return None
    #if all(m is None for m in df[8]): df.pop(8)
    #if all(m is None for m in df[6]): df.pop(6)
    return df


def header_substr(hd:str):
    pass

def new_header_formats():
    return TableFormat('header_edgar_filings',SecHeader.filing_columns,keys={'accession':'PRIMARY KEY'}),\
           TableFormat('header_edgar_companies',SecHeader.company_columns,keys={'cik':'PRIMARY KEY'})

if __name__=='__main__':
    t1='''
UNITED STATES
SECURITIES AND EXCHANGE COMMISSION
WASHINGTON, D.C. 20549
FORM 13F
FORM 13F COVER PAGE
REPORT FOR THE CALENDAR YEAR OR QUARTER ENDED: SEPTEMBER 30, 1999
INSTITUTIONAL INVESTMENT MANAGER FILING THIS REPORT:
NAME:  BENEFIT CAPITAL MANAGEMENT CORPORATION
ADDRESS:  39 OLD RIDGEBURY ROAD, E-2
          DANBURY, CT  06817-0001
13F FILE NUMBER:  28-2036
THE INSTITUTIONAL INVESTMENT MANAGER FILING THIS REPORT AND
THE PERSON BY WHOM IT IS SIGNED HEREBY REPRESENT THAT THE
PERSON SIGNING THE REPORT IS AUTHORIZED TO SUBMIT IT, THAT ALL
INFORMATION CONTAINED HEREIN IS TRUE, CORRECT, AND COMPLETE,
AND THAT IT IS UNDERSTOOD THAT ALL REQUIRED ITEMS, STATEMENTS,
SCHEDULES, LISTS, AND TABLES ARE CONSIDERED INTEGRAL PARTS OF
THIS FORM.
PERSON SIGNING THIS REPORT ON BEHALF OF REPORTING MANAGER:
NAME:  ELIZABETH LEPPLA
TITLE:  CONTROLLER
PHONE: 203-794-7346
SIGNATURE, PLACE, AND DATE OF SIGNING:
ELIZABETH LEPPLA, DANBURY, CT, NOVEMBER 2, 1999
REPORT TYPE:
[X] 13F HOLDINGS REPORT.
LIST OF OTHER MANAGERS REPORTING FOR THIS MANAGER: NONE
I AM SIGNING THIS REPORT AS REQUIRED BY THE SECURITIES EXCHANGE
ACT OF 1934.
<PAGE>
FORM 13F SUMMARY PAGE
REPORT SUMMARY:
NUMBER OF OTHER INCLUDED MANAGERS: 0
FORM 13F INFORMATION TABLE ENTRY TOTAL: 87
FORM 13F INFORMATION TABLE VALUE TOTAL:  $2,189,335
LIST OF OTHER INCLUDED MANAGERS: NONE
'''
    t2='''
    <TEXT>
                                  UNITED STATES
                       SECURITIES AND EXCHANGE COMMISSION
                             Washington, D.C. 20549

                                    Form 13F
                               Form 13F COVER PAGE
Report for the Calendar Year or Quarter Ended: 9/30/2011
Check here if Amendment []; Amendment Number:
                                               -------
This Amendment (Check only one.):               [] is a restatement.
                                                [] adds new holdings entries.

Institutional Investment Manager Filing this Report:


Name:      Cramer Rosenthal McGlynn, LLC

Address:   520 Madison Ave
           New York, N.Y. 10022


Form 13F File Number: 028-02028


The institutional investment manager filing this report and the person by whom
it is signed hereby represent that the person signing the report is authorized
to submit it, that all information contained herein is true, correct and
complete, and that it is understood that all required items, statements,
schedules, lists, and tables, are considered integral parts of this submission.

Persons Signing this Report on Behalf of Reporting Manager:

Name:   Carmine Cerasuolo
Title:  Head of Operations
Phone:  212-415-0407

Signature,  Place,  and  Date  of  Signing:

/s/ Carmine Cerasuolo              New York, NY                       11/10/2011
---------------------------------  ---------------------------------  ----------
[Signature]                        [City, State]                      [Date]



Report  Type  (Check  only  one):

[X]     13F HOLDINGS REPORT. (Check here if all holdings of this reporting
        manager are reported in this report.)

[ ]     13F NOTICE. (Check here if no holdings reported are in this report,
        and all holdings are reported by other reporting manager(s).)

[ ]     13F COMBINATION REPORT. (Check here if a portion of the holdings for
        this reporting manager are reported in this report and a portion are
        reported by other reporting manager(s).)

List of Other Managers Reporting for this Manager:



<PAGE>
                              Form 13F SUMMARY PAGE

Report Summary:

Number of Other Included Managers:                    0

Form 13F Information Table Entry Total:             214

Form 13F Information Table Value Total:  $   10,635,102
                                         --------------
                                         (In Thousands)


List of Other Included Managers:

Provide a numbered list of the name(s) and 13F file number(s) of all
institutional investment managers with respect to which this report is filed,
other than the manager filing this report.
NONE




<PAGE>
    '''
    t3='''
    <TEXT>

                                  UNITED STATES
                       SECURITIES AND EXCHANGE COMMISSION
                             WASHINGTON, D.C. 20549

                                    FORM 13F

                               FORM 13F COVER PAGE

Report for the Calendar Year or Quarter Ended: 03/31/2013
                                               -------------------------

Check here if Amendment [ ]; Amendment Number:
                                               -------
This Amendment (Check only one.):     [ ] is a restatement.
                                      [ ] adds new holdings entries.

Institutional Investment Manager Filing this Report:
`
Name:    THE ITHAKA GROUP, LLC
         -------------------------------------------------
Address: 3 BETHESDA METRO CENTER
         -------------------------------------------------
         SUITE 700
         -------------------------------------------------
         BETHESDA, MD 20814
         -------------------------------------------------

Form 13F File Number: 28-13786
                      ---------

The institutional investment manager filing this report and the person by whom
it is signed hereby represent that the person signing the report is authorized
to submit it, that all information contained herein is true, correct and
complete, and that it is understood that all required items, statements,
schedules, lists, and tables, are considered integral parts of this form.

Person Signing this Report on Behalf of Reporting Manager:

Name:    ROBERT A. KATZEN
         -------------------------------------------------
Title:   COO, CFO & CCO
         -------------------------------------------------
Phone:   301-775-7409
         -------------------------------------------------

Signature, Place, and Date of Signing:

/s/ Robert A. Katzen                West Palm Beach, FL            05/07/13
-----------------------------   ----------------------------   -----------------
         [Signature]                   [City, State]                [Date]

Report Type (Check only one.):

[X]   13F HOLDINGS REPORT. (Check here if all holdings of this reporting manager
      are reported in this report.)

[ ]   13F NOTICE. (Check here if no holdings reported are in this report, and
      all holdings are reported by other reporting manager(s).)

[ ]   13F COMBINATION REPORT. (Check here if a portion of the holdings for this
      reporting manager are reported in this report and a portion are reported
      by other reporting manager(s).)

<PAGE>

                              FORM 13F SUMMARY PAGE


Report Summary:


Number of Other Included Managers:       0
                                         ---------------
Form 13F Information Table Entry Total:  41
                                         ---------------
Form 13F Information Table Value Total:  303,455
                                         ---------------
                                           (thousands)


List of Other Included Managers:  NONE

Provide a numbered list of the name(s) and Form 13F file number(s) of all
institutional investment managers with respectto which this report is filed,
other than the manager filing this report.

NONE
<PAGE>

The Ithaka Group, LLC
FORM 13F
                                    31-Mar-13


<TABLE>
    '''
    i1=text_13fsections(t1)
    print(i1)
    for i in range(0,len(i1)-1,2):
        print(f'{i1[i]} : {i1[i+1]}')
    print('---')
    i1 = text_13fsections(t2)
    print(i1)
    for i in range(0, len(i1) - 1, 2):
        print(f'{i1[i]} : {i1[i + 1]}')
    print('---')
    i1 = text_13fsections(t3)
    print(i1)
    for i in range(0, len(i1) - 1, 2):
        print(f'{i1[i]} : {i1[i + 1]}')
    # print('---')
    # import time as t
    # tm = t.time()
    # c1,c2=extract_headers('''<ACCEPTANCE-DATETIME>20190125170551
    # ACCESSION NUMBER:		0000056701-19-000006
    # CONFORMED SUBMISSION TYPE:	10-Q
    # PUBLIC DOCUMENT COUNT:		57
    # CONFORMED PERIOD OF REPORT:	20181231
    # FILED AS OF DATE:		20190125
    # DATE AS OF CHANGE:		20190125
    #
    # FILER:
    #
    # 	COMPANY DATA:
    # 		COMPANY CONFORMED NAME:			KOSS CORP
    # 		CENTRAL INDEX KEY:			0000056701
    # 		STANDARD INDUSTRIAL CLASSIFICATION:	HOUSEHOLD AUDIO & VIDEO EQUIPMENT [3651]
    # 		IRS NUMBER:				391168275
    # 		STATE OF INCORPORATION:			DE
    # 		FISCAL YEAR END:			0630
    #
    # 	FILING VALUES:
    # 		FORM TYPE:		10-Q
    # 		SEC ACT:		1934 Act
    # 		SEC FILE NUMBER:	000-03295
    # 		FILM NUMBER:		19543201
    #
    # 	BUSINESS ADDRESS:
    # 		STREET 1:		4129 N PORT WASHINGTON AVE
    # 		CITY:			MILWAUKEE
    # 		STATE:			WI
    # 		ZIP:			53212
    # 		BUSINESS PHONE:		4149645000
    #
    # 	MAIL ADDRESS:
    # 		STREET 1:		4129 N PORT WASHINGTON AVE
    # 		CITY:			MILWAUKEE
    # 		STATE:			WI
    # 		ZIP:			53212
    #
    # 	FORMER COMPANY:
    # 		FORMER CONFORMED NAME:	KOSS ELECTRONICS INC
    # 		DATE OF NAME CHANGE:	19721005
    #
    # 	FORMER COMPANY:
    # 		FORMER CONFORMED NAME:	REK O KUT CO INC
    # 		DATE OF NAME CHANGE:	19680124''')
    # print(c1)
    # print(c2)
    # for i in range(0, len(i1) - 1, 2):
    #     print(f'{i1[i]} : {i1[i + 1]}')
    # print((t.time() - tm) * 1000.)



def header_business_values():
    pass

def header_filing_values():
    pass

# if __name__=='__main__':
#     from util import parse
#     sub=parse.subs_str('''
#     -----BEGIN PRIVACY-ENHANCED MESSAGE-----
# Proc-Type: 2001,MIC-CLEAR
# Originator-Name: webmaster@www.sec.gov
# Originator-Key-Asymmetric:
#  MFgwCgYEVQgBAQICAf8DSgAwRwJAW2sNKK9AVtBzYZmr6aGjlWyK3XmZv3dTINen
#  TWSM7vrzLADbmYQaionwg5sDW3P6oaM5D3tdezXMm7z1T+B+twIDAQAB
# MIC-Info: RSA-MD5,RSA,
#  T32ob4HyTvgBdbKJ6f6JCaYayv1rxzzqc74nBMmRnObZ3E9akAwcadVj2Ms/nfbp
#  TqZLXWcy1bioVtR/FBCyRw==
#
# <SEC-DOCUMENT>0001144204-10-007801.txt : 20100216
# <SEC-HEADER>0001144204-10-007801.hdr.sgml : 20100215
# <ACCEPTANCE-DATETIME>20100216100929
# ACCESSION NUMBER:		0001144204-10-007801
# CONFORMED SUBMISSION TYPE:	13F-HR
# PUBLIC DOCUMENT COUNT:		1
# CONFORMED PERIOD OF REPORT:	20091231
# FILED AS OF DATE:		20100216
# DATE AS OF CHANGE:		20100216
# EFFECTIVENESS DATE:		20100216
#
# FILER:
#
# 	COMPANY DATA:
# 		COMPANY CONFORMED NAME:			ITHAKA GROUP LLC
# 		CENTRAL INDEX KEY:			0001484043
# 		IRS NUMBER:				262269925
# 		STATE OF INCORPORATION:			DE
# 		FISCAL YEAR END:			1231
#
# 	FILING VALUES:
# 		FORM TYPE:		13F-HR
# 		SEC ACT:		1934 Act
# 		SEC FILE NUMBER:	028-13786
# 		FILM NUMBER:		10602965
#
# 	BUSINESS ADDRESS:
# 		STREET 1:		3 BETHESDA METRO CENTER
# 		CITY:			BETHESDA
# 		STATE:			MD
# 		ZIP:			20814
# 		BUSINESS PHONE:		240 395 5000
#
# 	MAIL ADDRESS:
# 		STREET 1:		3 BETHESDA METRO CENTER
# 		CITY:			BETHESDA
# 		STATE:			MD
# 		ZIP:			20814
# </SEC-HEADER>
# <DOCUMENT>
# <TYPE>13F-HR
# <SEQUENCE>1
# <FILENAME>v174468_13f-hr.txt
# <DESCRIPTION>FORM 13F HOLDINGS REPORT
# <TEXT>
#
#                                   UNITED STATES
#                        SECURITIES AND EXCHANGE COMMISSION
#                              WASHINGTON, D.C. 20549
#
#                                     FORM 13F
#
#                                FORM 13F COVER PAGE
#
# Report for the Calendar Year or Quarter Ended: 12/31/2009
#     ''',['HEADER>','\n'],['HEADER>','\n'])
#     print(sub)