from bs4 import BeautifulSoup
from util import parse
from bs4.diagnose import diagnose

def xml_soups(stri:str,soup_sreg='<XML>\n',soup_ereg='</XML>\n')->list[BeautifulSoup]:
    return [get_xml_soup(i) for i in parse.sub_strs(stri,soup_sreg,soup_ereg)]

#_past_header(stri,spos=fp+fl)
# def _past_header(st:str,reg='<?xml',spos=0):
#     return st.find('\n',st.find(reg,spos)+len(reg))+1

def get_xml_soup(text:str)->BeautifulSoup:
    return BeautifulSoup(text,'xml')