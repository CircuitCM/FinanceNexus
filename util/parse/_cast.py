import re
from datetime import date, datetime
def _conv_datetime(st:str):
    pass


def _conv_numeric(st:str):
    try:
        return float(st)
    except:
        try:
            return int(st)
        except:
            return 0

def _conv_int(st:str):
    try:
        return int(st)
    except:
        pass

_dv= re.compile('\d+')
def dollar_int(st:str):
    return int(''.join(_dv.findall(st.split('.')[0])))

def to_int(st:str):
    return int(''.join(_dv.findall(st)))

_nv= re.compile(r'(?<=-)\d+|\d+(?=-)')
#_dv= re.compile(r'(?<=/)\d+|\d+(?=/)')
def any_date(st:str):
    fi=[int(i) for i in _nv.findall(st)]
    lf = len(fi)
    if lf==3:
        dn=date(2000+fi[0] if fi[0]<100 else fi[0],fi[1],fi[2])
        return dn
    elif lf==2:
        fi=[int(i) for i in _nv.findall(st)]
        dn = date(2000 + fi[0] if fi[0] < 100 else fi[0], fi[1], 1)
        return dn
    else:
        pass
        #finish later

        #assume year month

# if __name__=='__main__':
#     print(any_date('21-10-10'))