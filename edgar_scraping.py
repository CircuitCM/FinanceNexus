import os
from secedgar import FilingType,CompanyFilings,ComboFilings,filings,client,cik_lookup
import edgar

def try_mkdir(mdr):
    try:
        os.mkdir(mdr)
    except:
        pass

def python_slash(pth: str) -> str:
    chry: [chr] = [ch for ch in pth]
    for i in range(0, len(chry)):
        if chry[i] == '\\':
            chry[i] = '/'
    return ''.join(chry)

def show_dict(dic:dict):
    print("\n".join(f'{k} : {v}' for k,v in dic.items()))

wdir = python_slash(__file__).rsplit('/', 1)[0]+'/'
F_INDX = wdir+'Edgar Filing Index/'
FLNG = wdir+'Edgar Filings/'
USER_AGENT="The Ithaka Group LLC cmarks@ithakagroup.com"

if __name__=="__main__":
    edgar.download()
    try_mkdir(F_INDX)
    try_mkdir(FLNG)
    #mp=cik_lookup.get_cik_map()
    #show_dict(mp)
    cli = client.NetworkClient("The Ithaka Group LLC cmarks@ithakagroup.com",rate_limit=9)
    # #flng = Fil
    edgar.download_index(F_INDX,2019,"The Ithaka Group LLC cmarks@ithakagroup.com")
    fl=filings('0001816616',client=cli)
    fl.filing_type=FilingType.FILING_13FNT
    #fl.save(FLNG)
    print(fl.get_urls())
    #fl.filing_type = FilingType.FILING_13FHR
    #fl.save(FLNG)
    #todo: get_urls comes from my database, same as kick/name lookup