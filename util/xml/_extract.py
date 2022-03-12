from bs4 import BeautifulSoup
from collections import defaultdict
from enum import Enum, auto

# func will accept this for formatting rows correctly
def _try_int_float(st: str,bsn=None):
    try:
        return int(st)
    except:
        try:
            return float(st)
        except:
            return st


class TKeys(Enum):
    IGNORE = auto()
    ADD = auto()
    ID = auto()


def get_table_layers(bs:BeautifulSoup|list[BeautifulSoup],k_proc:dict=None,id_d:dict=None)->dict[str,list]:
    #assume id dict is not none when ID is used
    if type(bs)==list:
        bs.reverse()
        #so soup is done
        contl=bs
    else:
        contl=[bs]
    #assumes fields unique to tables
    fd=defaultdict(list)
    if k_proc is None: k_proc={}
    #only works with first parent after value layer
    adst={}
    while len(contl)>0:
        bs=contl.pop()
        bc = bs.findChildren(recursive=False)
        lbc=len(bc)
        bsn=bs.name
        if lbc==0:
            nms= adst.get(bs, None)
            bsn=bsn if nms is None else f'{nms}_{bsn}'
            ac = k_proc.get(bsn, None)
            if ac is not TKeys.IGNORE:
                if ac is TKeys.ID:
                    fd[bsn].append(', '.join([bs.text, *[f'{i}:{fd[i][-1]}' for i in id_d[bsn]]]))
                else:
                    fd[bsn].append(bs.text)
                    #if bsn=='sshPrnamtType':print(bs.text)
        else:
            bc.reverse() #cause bs4 being annoying
            ac = k_proc.get(bsn, None)
            if ac is TKeys.ADD:
                for sub in bc:
                    contl.append(sub)
                    adst[sub]=bsn
            elif ac is not TKeys.IGNORE:
                for sub in bc:
                    contl.append(sub)
    return fd


def get_table_series(bs:BeautifulSoup,recursive=True)->list[list]:
    bly=[]
    contl=[bs]
    while len(contl)>0:
        bs=contl.pop()
        bc = bs.findChildren(recursive=False)
        lbc=len(bc)
        if lbc==0:
            continue
        elif lbc==1:contl.append(bc[0])
        else:
            d = defaultdict(list)
            for sub in bc:
                d[sub.name].append(sub)
            for k,v in d.items():
                if len(v)>1:bly.append(v)
                else: contl.append(v[0])
    return bly

if __name__=='__main__':
    t1='''
    <HTML><HEAD>
<TITLE>SC 13D</TITLE>
</HEAD>
 <BODY BGCOLOR="WHITE">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="line-height:1.0pt;margin-top:0pt;margin-bottom:0pt;border-bottom:1px solid #000000">&nbsp;</P>
<P STYLE="line-height:3.0pt;margin-top:0pt;margin-bottom:2pt;border-bottom:1px solid #000000">&nbsp;</P> <P STYLE="margin-top:4pt; margin-bottom:0pt; font-size:18pt; font-family:Times New Roman" ALIGN="center"><B>UNITED STATES </B></P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:18pt; font-family:Times New Roman" ALIGN="center"><B>SECURITIES AND EXCHANGE COMMISSION </B></P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:12pt; font-family:Times New Roman" ALIGN="center"><B>Washington, D.C. 20549 </B></P> <P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P><center>
<P STYLE="line-height:6.0pt;margin-top:0pt;margin-bottom:2pt;border-bottom:1.00pt solid #000000;width:21%">&nbsp;</P></center> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:18pt; font-family:Times New Roman" ALIGN="center"><B>SCHEDULE 13D
</B></P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:12pt; font-family:Times New Roman" ALIGN="center"><B>Under the Securities Exchange Act of 1934 </B></P> <P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P><center>
<P STYLE="line-height:6.0pt;margin-top:0pt;margin-bottom:2pt;border-bottom:1.00pt solid #000000;width:21%">&nbsp;</P></center> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:22pt; font-family:Times New Roman" ALIGN="center"><B>Montage
Resources Corporation </B></P> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>(Name of Issuer) </B></P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>Common Stock, par value $0.01 per share </B></P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:8pt; font-family:Times New Roman" ALIGN="center"><B>(Title of Class&nbsp;of Securities) </B></P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>27890G 100 </B></P> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:8pt; font-family:Times New Roman" ALIGN="center"><B>(CUSIP
Number) </B></P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B><I>Copies to: </I></B></P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>Chris Lacy </B></P> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>Vice
President, General Counsel and Secretary </B></P> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>Southwestern Energy Company </B></P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>10000 Energy Drive </B></P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>Spring, Texas 77389 </B></P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>Telephone: (832) <FONT STYLE="white-space:nowrap">796-1000</FONT> </B></P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:8pt; font-family:Times New Roman" ALIGN="center"><B>(Name, Address and Telephone Number of Person Authorized to Receive Notices and Communications) </B></P>
<P STYLE="margin-top:24pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>August&nbsp;12, 2020 </B></P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:8pt; font-family:Times New Roman" ALIGN="center"><B>(Date of Event Which Requires Filing of this Statement) </B></P> <P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P><center>
<P STYLE="line-height:6.0pt;margin-top:0pt;margin-bottom:2pt;border-bottom:1.00pt solid #000000;width:21%">&nbsp;</P></center> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">If the filing person has
previously filed a statement on Schedule 13G to report the acquisition that is the subject of this Schedule 13D, and is filing this schedule because of <FONT STYLE="white-space:nowrap">&#167;&#167;&nbsp;240.13d-1(e),</FONT> <FONT
STYLE="white-space:nowrap">240.13d-1(f)</FONT> or <FONT STYLE="white-space:nowrap">240.13d-1(g),</FONT> check the following box.&nbsp;&nbsp;&#9744; </P> <P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<P STYLE="line-height:1.0pt;margin-top:0pt;margin-bottom:2pt;border-bottom:1px solid #000000">&nbsp;</P> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman"><B>Note:</B> Schedules filed in paper format shall
include a signed original and five copies of the schedule, including all exhibits. See Rule <FONT STYLE="white-space:nowrap">13d-7</FONT> for other parties to whom copies are to be sent. </P>
<P STYLE="font-size:4pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P> <P STYLE="line-height:3.0pt;margin-top:0pt;margin-bottom:2pt;border-bottom:1px solid #000000">&nbsp;</P> <P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="4%" VALIGN="top" ALIGN="left">*</TD>
<TD ALIGN="left" VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman; " ALIGN="left">The remainder of this cover page shall be filled out for a reporting person&#146;s initial filing on this form
with respect to the subject class of securities, and for any subsequent amendment containing information which would alter disclosures provided in a prior cover page. </P></TD></TR></TABLE>
<P STYLE="font-size:10pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P> <P STYLE="line-height:1.0pt;margin-top:0pt;margin-bottom:0pt;border-bottom:1px solid #000000">&nbsp;</P>
<P STYLE="line-height:3.0pt;margin-top:0pt;margin-bottom:2pt;border-bottom:1px solid #000000">&nbsp;</P>
</DIV></Center>


<p style="margin-top:1em; margin-bottom:0em; page-break-before:always">
<HR SIZE="3" style="COLOR:#999999" WIDTH="100%" ALIGN="CENTER">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">The information required on the remainder of this cover page shall not be deemed to be &#147;filed&#148; for
the purpose of Section&nbsp;18 of the Securities Exchange Act of 1934 (&#147;Act&#148;) or otherwise subject to the liabilities of that section of the Act but shall be subject to all other provisions of the Act (however, see the Notes). </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">CUSIP No.&nbsp;969490101 </P> <P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE CELLSPACING="0" CELLPADDING="0" WIDTH="100%" BORDER="0" STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt">


<TR>

<TD WIDTH="5%"></TD>

<TD VALIGN="bottom" WIDTH="1%"></TD>
<TD WIDTH="6%"></TD>

<TD VALIGN="bottom" WIDTH="1%"></TD>
<TD WIDTH="2%"></TD>

<TD VALIGN="bottom" WIDTH="1%"></TD>
<TD WIDTH="84%"></TD></TR>


<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="top" STYLE="BORDER-LEFT:1px solid #000000; BORDER-TOP:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-left:8pt"><FONT STYLE="font-size:10pt">&nbsp;&nbsp;1&nbsp;</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-TOP:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;</TD>
<TD VALIGN="top" COLSPAN="5" STYLE="BORDER-TOP:1px solid #000000; BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">NAME OF
REPORTING PERSON</P> <P STYLE="font-size:12pt; margin-top:0pt; margin-bottom:0pt">&nbsp;</P> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:12pt; font-family:Times New Roman">Southwestern Energy Company</P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top" STYLE="BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-left:8pt">&nbsp;&nbsp;2</TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;</TD>
<TD VALIGN="top" COLSPAN="5" STYLE="BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">CHECK THE APPROPRIATE BOX IF A MEMBER
OF A GROUP</P> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">(a)&nbsp;&nbsp;&#9744;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(b)&nbsp;&nbsp;&#9746;</P>
<P STYLE="font-size:12pt; margin-top:0pt; margin-bottom:1pt">&nbsp;</P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="top" STYLE="BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-left:8pt"><FONT STYLE="font-size:10pt">&nbsp;&nbsp;3</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;</TD>
<TD VALIGN="top" COLSPAN="5" STYLE="BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">SEC USE ONLY</P>
<P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:1pt">&nbsp;</P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="top" STYLE="BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-left:8pt"><FONT STYLE="font-size:10pt">&nbsp;&nbsp;4</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;</TD>
<TD VALIGN="top" COLSPAN="5" STYLE="BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">SOURCE OF FUNDS</P>
<P STYLE="font-size:12pt; margin-top:0pt; margin-bottom:0pt">&nbsp;</P> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:12pt; font-family:Times New Roman">N/A</P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="top" STYLE="BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-left:8pt"><FONT STYLE="font-size:10pt">&nbsp;&nbsp;5</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;</TD>
<TD VALIGN="top" COLSPAN="5" STYLE="BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">CHECK BOX IF DISCLOSURE OF LEGAL
PROCEEDINGS IS REQUIRED PURSUANT TO ITEM&nbsp;2(d) OR 2(e)</P> <P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:12pt; font-family:Times New Roman">&#9744;</P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="top" STYLE="BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-left:8pt"><FONT STYLE="font-size:10pt">&nbsp;&nbsp;6</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;</TD>
<TD VALIGN="top" COLSPAN="5" STYLE="BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">CITIZENSHIP OR PLACE OF
ORGANIZATION</P> <P STYLE="font-size:12pt; margin-top:0pt; margin-bottom:0pt">&nbsp;</P> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:12pt; font-family:Times New Roman">DELAWARE</P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="middle" COLSPAN="3" ROWSPAN="4" STYLE="BORDER-LEFT:1px solid #000000; padding-left:8pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center">NUMBER&nbsp;OF</P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center">SHARES</P> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center">BENEFICIALLY</P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center">OWNED&nbsp;BY</P> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center">EACH</P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center">REPORTING</P> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center">PERSON</P>
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center">WITH:</P> <P STYLE="font-size:10pt;margin-top:0pt;margin-bottom:1pt" align="left">&nbsp;</P></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;&nbsp;</TD>
<TD VALIGN="top" STYLE="BORDER-BOTTOM:1px solid #000000"><FONT STYLE="font-size:10pt">&nbsp;&nbsp;7&nbsp;</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;&nbsp;</TD>
<TD VALIGN="top" STYLE="BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">SOLE VOTING POWER</P>
<P STYLE="font-size:12pt; margin-top:0pt; margin-bottom:0pt">&nbsp;</P> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:12pt; font-family:Times New Roman">0</P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;&nbsp;</TD>
<TD VALIGN="top" STYLE="BORDER-BOTTOM:1px solid #000000"><FONT STYLE="font-size:10pt">&nbsp;&nbsp;8</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;&nbsp;</TD>
<TD VALIGN="top" STYLE="BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">SHARED VOTING POWER</P>
<P STYLE="font-size:12pt; margin-top:0pt; margin-bottom:0pt">&nbsp;</P> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:12pt; font-family:Times New Roman">0</P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;&nbsp;</TD>
<TD VALIGN="top" STYLE="BORDER-BOTTOM:1px solid #000000"><FONT STYLE="font-size:10pt">&nbsp;&nbsp;9</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;&nbsp;</TD>
<TD VALIGN="top" STYLE="BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">SOLE DISPOSITIVE POWER</P>
<P STYLE="font-size:12pt; margin-top:0pt; margin-bottom:0pt">&nbsp;</P> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:12pt; font-family:Times New Roman">0</P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000">&nbsp;&nbsp;</TD>
<TD VALIGN="top"><FONT STYLE="font-size:10pt">10</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000">&nbsp;&nbsp;</TD>
<TD VALIGN="top" STYLE="BORDER-RIGHT:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">SHARED DISPOSITIVE POWER</P>
<P STYLE="font-size:12pt; margin-top:0pt; margin-bottom:0pt">&nbsp;</P> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:12pt; font-family:Times New Roman">14,051,904 <SUP STYLE="font-size:85%; vertical-align:top">(1)</SUP></P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="top" STYLE="BORDER-LEFT:1px solid #000000; BORDER-TOP:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-left:8pt"><FONT STYLE="font-size:10pt">11</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-TOP:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;</TD>
<TD VALIGN="top" COLSPAN="5" STYLE="BORDER-TOP:1px solid #000000; BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt">
<P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">AGGREGATE AMOUNT BENEFICIALLY OWNED BY EACH REPORTING PERSON</P> <P STYLE="font-size:12pt; margin-top:0pt; margin-bottom:0pt">&nbsp;</P>
<P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:12pt; font-family:Times New Roman">14,051,904 <SUP STYLE="font-size:85%; vertical-align:top">(1)</SUP></P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="top" STYLE="BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-left:8pt"><FONT STYLE="font-size:10pt">12</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;</TD>
<TD VALIGN="top" COLSPAN="5" STYLE="BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">CHECK IF THE AGGREGATE AMOUNT IN ROW
(11) EXCLUDES CERTAIN SHARES</P> <P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:12pt; font-family:Times New Roman">&#9744;</P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="top" STYLE="BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-left:8pt"><FONT STYLE="font-size:10pt">13</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;</TD>
<TD VALIGN="top" COLSPAN="5" STYLE="BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">PERCENT OF CLASS REPRESENTED BY AMOUNT
IN ROW (11)</P> <P STYLE="font-size:12pt; margin-top:0pt; margin-bottom:0pt">&nbsp;</P> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:12pt; font-family:Times New Roman">39.0%<SUP STYLE="font-size:85%; vertical-align:top">
(1)</SUP></P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:12pt">
<TD VALIGN="top" STYLE="BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-left:8pt"><FONT STYLE="font-size:10pt">14</FONT></TD>
<TD VALIGN="bottom" STYLE=" BORDER-LEFT:1px solid #000000; BORDER-BOTTOM:1px solid #000000">&nbsp;</TD>
<TD VALIGN="top" COLSPAN="5" STYLE="BORDER-RIGHT:1px solid #000000; BORDER-BOTTOM:1px solid #000000; padding-right:2pt"> <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">TYPE OF REPORTING PERSON</P>
<P STYLE="font-size:12pt; margin-top:0pt; margin-bottom:0pt">&nbsp;</P> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:12pt; font-family:Times New Roman">CO</P></TD></TR>
</TABLE> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">(1) An aggregate of 14,051,904 shares of common stock of Montage Resources Corporation, a Delaware corporation (the
&#147;Issuer&#148;), held by the EnCap Stockholders (as defined below) are subject to the Support Agreement (as defined below), dated August&nbsp;12, 2020, entered into by Southwestern Energy Company, a Delaware corporation,
(&#147;Southwestern&#148;), and the EnCap Stockholders set forth on <U>Schedule B</U> hereto. Southwestern expressly disclaims beneficial ownership of any shares of Issuer common stock covered by the Support Agreement. The aggregate number of shares
of Issuer common stock covered by the Support Agreement represents approximately 39.0% of the outstanding shares of Issuer common stock based on 36,021,513 shares of Issuer common stock, $0.01 par value per share, issued and outstanding as of
August&nbsp;3, 2020, as set forth in the Quarterly Report on Form <FONT STYLE="white-space:nowrap">10-Q</FONT> of the Issuer filed with the U.S. Securities and Exchange Commission (the &#147;SEC&#148;) on August&nbsp;7, 2020. </P>
</DIV></Center>


<p style="margin-top:1em; margin-bottom:0em; page-break-before:always">
<HR SIZE="3" style="COLOR:#999999" WIDTH="100%" ALIGN="CENTER">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman"><B>Item&nbsp;1. Security and Issuer </B></P>
<P STYLE="margin-top:6pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">This Schedule 13D relates to the common stock, $0.01 par value per share (the &#147;Montage Common Stock&#148;) of Montage Resources Corporation, a Delaware
corporation (the &#147;Issuer&#148; or &#147;Montage&#148;). The address of the principal executive offices of the Issuer is 122 West John Carpenter Freeway, Suite 300, Irving, TX 75039. </P>
<P STYLE="margin-top:18pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman"><B>Item&nbsp;2. Identity and Background </B></P> <P STYLE="margin-top:6pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">This statement is
being filed pursuant to Rule <FONT STYLE="white-space:nowrap">13d-1</FONT> under the Securities Exchange Act of 1934, as amended (the &#147;Exchange Act&#148;), by Southwestern Energy Company, a Delaware corporation (&#147;Southwestern&#148; or the
&#147;Reporting Person&#148;). The address of the principal business and the principal office of the Reporting Person is 10000 Energy Drive, Spring, Texas 77389. Southwestern is an independent energy company engaged in natural gas, oil and NGL
exploration, development and production (&#147;E&amp;P&#148;). Southwestern is also focused on creating and capturing additional value through its marketing business (&#147;Marketing&#148;), which was previously referred to as &#147;Midstream&#148;
when it included the operation of gathering systems. Southwestern conducts most of its business through subsidiaries and operates principally in two segments: E&amp;P and Marketing. </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">The name, business address, present principal occupation or employment and citizenship of each director and executive officer of the Reporting Person is set
forth on <U>Schedule A</U>. During the last five years, none of the Reporting Person or, to the knowledge of the Reporting Person, any of the persons listed on <U>Schedule A</U> attached hereto, have been convicted in a criminal proceeding
(excluding traffic violations or similar misdemeanors) or been a party to a civil proceeding of a judicial or administrative body of competent jurisdiction and as a result of such proceeding was or is subject to a judgment, decree or final order
enjoining future violations of, or prohibiting or mandating activities subject to, federal or state securities laws or finding any violation with respect to such laws. </P>
<P STYLE="margin-top:18pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman"><B>Item&nbsp;3. Source and Amount of Funds or Other Consideration </B></P>
<P STYLE="margin-top:6pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">On August&nbsp;12, 2020, Southwestern entered into an Agreement and Plan of Merger (the &#147;Merger Agreement&#148;) with the Issuer, pursuant to which, among
other things and subject to the satisfaction or waiver of certain conditions precedent, the Issuer will merge with and into Southwestern (the &#147;Merger&#148;) and, subject to certain exceptions, each issued and outstanding share of Montage Common
Stock will be converted into and exchanged for 1.8656 shares of common stock, par value $0.01 per share, of Southwestern (&#147;Southwestern Common Stock&#148;), as provided in the Merger Agreement. </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">On August&nbsp;12, 2020, contemporaneously with the execution of the Merger Agreement, Southwestern and certain Issuer stockholders affiliated with EnCap
Investments L.P. set forth on <U>Schedule B</U> hereto (the &#147;EnCap Stockholders&#148;) entered into a Support Agreement, dated August&nbsp;12, 2020 (the &#147;Support Agreement&#148;), with respect to the Merger Agreement. </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">The shares of Montage Common Stock to which this Schedule 13D relates have not been purchased by the Reporting Person, and no funds were expended in
consideration for the execution of either the Merger Agreement or the Support Agreement. </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">The information set forth or incorporated by reference in
Item&nbsp;4 is incorporated by reference in this Item&nbsp;3. </P> <P STYLE="margin-top:18pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman"><B>Item&nbsp;4. Purpose of Transaction </B></P>
<P STYLE="margin-top:6pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">Under the terms of, and subject to the conditions set forth in, the Merger Agreement, at the effective time of the Merger (the &#147;Effective Time&#148;),
each share of Montage Common Stock issued and outstanding immediately prior to the Effective Time will be cancelled and extinguished and automatically converted into the right to receive 1.8656 shares of Southwestern Common Stock (the &#147;Merger
Consideration&#148; and such ratio, the &#147;Exchange Ratio&#148;), except for any shares of Montage Common Stock held in treasury or owned directly or indirectly by Montage or any of its wholly owned subsidiaries or by Southwestern or any of its
wholly owned subsidiaries (other than those held in a fiduciary capacity) which will be automatically cancelled and no consideration will be paid or delivered in exchange thereof. No fractional shares of Southwestern Common Stock will be issued in
the Merger, and holders of shares of Montage Common Stock will, instead, receive cash in lieu of a fraction of a share of Southwestern Common Stock, if any. </P>
</DIV></Center>


<p style="margin-top:1em; margin-bottom:0em; page-break-before:always">
<HR SIZE="3" style="COLOR:#999999" WIDTH="100%" ALIGN="CENTER">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">Pursuant to the terms of the Merger Agreement: </P>
<P STYLE="font-size:6pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="5%">&nbsp;</TD>
<TD WIDTH="3%" VALIGN="top" ALIGN="left">&#149;</TD>
<TD WIDTH="1%" VALIGN="top">&nbsp;</TD>
<TD ALIGN="left" VALIGN="top"> <P ALIGN="left" STYLE=" margin-top:0pt ; margin-bottom:0pt; font-family:Times New Roman; font-size:10pt">as of immediately prior to the Effective Time, each award of Montage restricted stock units that vests based on
continued service to Montage (other than Montage PSU Awards (defined below)) (&#147;Montage RSU Award&#148;) that is outstanding immediately prior to the Effective Time shall convert into an award (an &#147;Assumed RSU Award&#148;), with respect to
a number of shares of Southwestern Common Stock equal to the product obtained by multiplying (i)&nbsp;the applicable number of shares of Montage Common Stock subject to such Montage RSU Award immediately prior to the Effective Time by (ii)&nbsp;the
Exchange Ratio. For each holder of a Montage RSU Award, any fractional shares resulting from the conversion of his or her Montage RSU Awards shall be rounded to the nearest whole share. Except as otherwise provided in the Merger Agreement, each
Assumed RSU Award shall continue to be subject to the same terms and conditions that applied to the underlying Montage RSU Award immediately prior to the Effective Time, except that Southwestern (x)&nbsp;may modify terms rendered inoperative by
reason of the transactions contemplated by the Merger Agreement or for such other immaterial administrative or ministerial changes as in the reasonable and good faith determination of Southwestern are appropriate to effectuate the administration of
the Assumed RSU Award, and (y)&nbsp;may settle such awards upon vesting in Southwestern Common Stock or cash. </P></TD></TR></TABLE> <P STYLE="font-size:6pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="5%">&nbsp;</TD>
<TD WIDTH="3%" VALIGN="top" ALIGN="left">&#149;</TD>
<TD WIDTH="1%" VALIGN="top">&nbsp;</TD>
<TD ALIGN="left" VALIGN="top"> <P ALIGN="left" STYLE=" margin-top:0pt ; margin-bottom:0pt; font-family:Times New Roman; font-size:10pt">Montage shall take all necessary and appropriate actions so that, prior to the Effective Time, each then
outstanding award of restricted stock units which would, if relevant performance and other vesting conditions are met, result in the issuance of Montage Common Stock to the holder of such restricted stock unit award (&#147; Montage PSU Award&#148;)
shall be terminated and vested in accordance with its terms; provided, however, that the number of shares of Montage Common Stock deliverable in connection with such termination and vesting shall be determined by the Compensation Committee of the
Montage board of directors pursuant to the terms of the applicable Montage PSU Award as in effect on the date of the Merger Agreement and Montage shall not use discretion to increase the amount of consideration payable with respect to any Montage
PSU Award in connection with such termination and vesting. Southwestern may elect to settle the Montage PSU Award in cash instead of shares of Southwestern Common Stock. </P></TD></TR></TABLE>
<P STYLE="font-size:6pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="5%">&nbsp;</TD>
<TD WIDTH="3%" VALIGN="top" ALIGN="left">&#149;</TD>
<TD WIDTH="1%" VALIGN="top">&nbsp;</TD>
<TD ALIGN="left" VALIGN="top"> <P ALIGN="left" STYLE=" margin-top:0pt ; margin-bottom:0pt; font-family:Times New Roman; font-size:10pt">Montage shall take all necessary and appropriate actions so that prior to the Effective Time each award of
restricted shares of Montage Common Stock (&#147;Montage Restricted Stock Award&#148;) granted to Montage <FONT STYLE="white-space:nowrap">non-employee</FONT> directors shall vest. Shares of Montage Common Stock attributable to such Montage
Restricted Stock Awards shall be treated in the manner set forth in the Merger Agreement upon the Effective Time. </P></TD></TR></TABLE> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">On August&nbsp;12,
2020, contemporaneously with the execution of the Merger Agreement, the EnCap Stockholders entered into that certain Support Agreement (the &#147;Support Agreement&#148;) with Southwestern, pursuant to which, among other things, the EnCap
Stockholders agreed to vote all of their shares of Montage Common Stock (i)&nbsp;in favor of adoption of the Merger Agreement and approval of other matters that are required to be approved by the stockholders of the Issuer in order to effect the
Merger; (ii)&nbsp;against any merger agreement or merger (other than the Merger Agreement and the Merger) or other fundamental corporate transaction that is prohibited by the Merger Agreement, unless such transaction is approved in writing by
Southwestern, or any alternative acquisition proposal; and (iii)&nbsp;against any amendment of the Issuer&#146;s certificate of incorporation or bylaws or other proposal or transaction involving the Issuer or any of its subsidiaries, which amendment
or other proposal or transaction would in any manner delay, impede, frustrate, prevent or nullify the Merger, the Merger Agreement or any of the transactions contemplated thereby or change in any manner the voting rights of any outstanding class of
capital stock of the Issuer. The Support Agreement shall terminate upon the earliest to occur of: (a)&nbsp;the termination of the Merger Agreement in accordance with its terms; (b)&nbsp;the Effective Time; (c)&nbsp;the date of any modification,
waiver or amendment to the Merger Agreement effected without any EnCap Stockholder&#146;s consent that (y)&nbsp;decreases the amount or changes the form of consideration payable to all of the stockholders of the Issuer pursuant to the terms of the
Merger Agreement as in effect on the date of the Support Agreement or (z)&nbsp;otherwise materially adversely affects the interests of such EnCap Stockholder; (d) the mutual written consent of the parties to the Support Agreement, and (e) the
Termination Date (as defined in the Merger Agreement). As of August&nbsp;12, 2020, the EnCap Stockholders are the beneficial owner of approximately 39.0% of the outstanding Montage Common Stock based on 36,021,513 shares of Montage Common Stock
issued and outstanding as of August&nbsp;3, 2020, as set forth in the Quarterly Report on Form <FONT STYLE="white-space:nowrap">10-Q</FONT> of the Issuer filed with the U.S. Securities and Exchange Commission (the &#147;SEC&#148;) on August&nbsp;7,
2020. </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">The transactions contemplated by the Merger Agreement may, if consummated in accordance with its terms, result in any or all of the actions
contemplated by subparagraphs (a)-(j) of Item 4 of Schedule 13D, including, without limitation, (i)&nbsp;the Merger, as a result of which the Issuer would merge with and into the Reporting Person, with the
</P>
</DIV></Center>


<p style="margin-top:1em; margin-bottom:0em; page-break-before:always">
<HR SIZE="3" style="COLOR:#999999" WIDTH="100%" ALIGN="CENTER">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">
Reporting Person surviving the Merger, (ii)&nbsp;the cessation of each existing Issuer director&#146;s role as a director of Issuer, (iii)&nbsp;material changes in the capitalization, dividend
policy and corporate structure of the Issuer, (iv)&nbsp;the termination of the listing of the Montage Common Stock on NYSE, and (v)&nbsp;the termination of the registration of the Montage Common Stock under Section&nbsp;12(g)(4) of the Exchange Act.
</P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">The Merger Agreement is attached hereto as <U>Exhibit A</U> and is incorporated into this Item 4 by reference. The foregoing summary of the Merger
Agreement has been included to provide investors and security holders with information regarding the terms of the Merger Agreement and is qualified in its entirety by the terms and conditions of the Merger Agreement. It is not intended to provide
any other factual information about the Issuer, the Reporting Person or their respective subsidiaries and affiliates. The Merger Agreement contains representations and warranties by each of the parties to the Merger Agreement, which were made only
for purposes of the Merger Agreement and as of dates specified therein. The representations, warranties and covenants in the Merger Agreement were made solely for the benefit of the parties to the Merger Agreement; may be subject to limitations
agreed upon by the contracting parties, including being qualified by confidential disclosures made for the purposes of allocating contractual risk between the parties to the Merger Agreement instead of establishing these matters as facts; and may be
subject to standards of materiality applicable to the contracting parties that differ from those applicable to investors. Investors should not rely on the representations, warranties and covenants or any descriptions thereof as characterizations of
the actual state of facts or condition of the Issuer, the Reporting Person or any of their respective subsidiaries or affiliates. Moreover, information concerning the subject matter of the representations, warranties and covenants may change after
the date of the Merger Agreement, which subsequent information may or may not be fully reflected in the Issuer&#146;s or the Reporting Person&#146;s public disclosures. </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">The Support Agreement is attached hereto as <U>Exhibit</U><U></U><U>&nbsp;B</U> and is incorporated into this Item 4 by reference. The foregoing summary has
been included to provide investors and security holders with information regarding the terms of the Support Agreement and is qualified in its entirety by the terms and conditions of the Support Agreement. It is not intended to provide any other
factual information about the parties or their respective subsidiaries and affiliates. The Support Agreement contains representations and warranties by each of the parties to the Support Agreement, which were made only for purposes of the Support
Agreement and as of specified dates. The representations, warranties and covenants in the Support Agreement were made solely for the benefit of the parties to the Support Agreement; may be subject to limitations agreed upon by the contracting
parties, including being qualified by confidential disclosures made for the purposes of allocating contractual risk between the parties to the Support Agreement instead of establishing these matters as facts; and may be subject to standards of
materiality applicable to the contracting parties that differ from those applicable to investors. Investors should not rely on the representations, warranties and covenants or any descriptions thereof as characterizations of the actual state of
facts or condition of the parties or any of their respective subsidiaries or affiliates. Moreover, information concerning the subject matter of the representations, warranties and covenants may change after the date of the Support Agreement, which
subsequent information may or may not be fully reflected in the Issuer&#146;s or the Reporting Person&#146;s public disclosures. </P> <P STYLE="margin-top:18pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman"><B>Item&nbsp;5. Interest
in Securities of the Issuer </B></P> <P STYLE="margin-top:6pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">(a) and (b). &nbsp;&nbsp;&nbsp;&nbsp;The response of the Reporting Person to rows 7 through 13 on the cover page of this
Schedule&nbsp;13D are incorporated by reference herein. </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">As of the date hereof, the Reporting Person does not own any shares of Montage Common Stock.
However, as a result of the Support Agreement, the Reporting Person may be deemed to have shared voting and dispositive power with respect to up to an aggregate of 14,051,904 shares of Montage Common Stock, and thus, for the purpose of Rule <FONT
STYLE="white-space:nowrap">13d-3</FONT> promulgated under the Exchange Act, the Reporting Person may be deemed to be the beneficial owner of an aggregate of 14,051,904 shares of Montage Common Stock. The aggregate number of shares of Montage Common
Stock covered by the Support Agreement represents approximately 39.0% of the outstanding Montage Common Stock based on 36,021,513 shares of Montage Common Stock issued and outstanding as of August&nbsp;3, 2020, as set forth in the Quarterly Report
on Form <FONT STYLE="white-space:nowrap">10-Q</FONT> of the Issuer filed with the SEC on August&nbsp;7, 2020. </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; margin-right:2%; font-size:10pt; font-family:Times New Roman">The filing of this
statement on Schedule 13D shall not be construed as an admission that the Reporting Person is, for the purposes of Section&nbsp;13(d) or 13(g) of the Exchange Act, the beneficial owner of any shares of Montage Common Stock. Pursuant to <FONT
STYLE="white-space:nowrap">Rule&nbsp;13d-4,</FONT> the Reporting Person disclaims all such beneficial ownership. </P>
</DIV></Center>


<p style="margin-top:1em; margin-bottom:0em; page-break-before:always">
<HR SIZE="3" style="COLOR:#999999" WIDTH="100%" ALIGN="CENTER">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">(c). &nbsp;&nbsp;&nbsp;&nbsp;Except as set forth in this Schedule 13D with reference to the Merger Agreement
and the Support Agreement, neither the Reporting Person nor, to the Reporting Person&#146;s knowledge, any of the persons listed in Schedule A hereto, has effected any transaction in shares of Montage Common Stock during the past 60 days. </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">(d). &nbsp;&nbsp;&nbsp;&nbsp;The Reporting Person has no right to receive dividends from, or the proceeds from the sale of, any shares of Montage Common Stock
subject to the Support Agreement. The Reporting Person will have no pecuniary interest in any shares of Montage Common Stock unless and until the transactions contemplated by the Merger Agreement are consummated. </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">(e).&nbsp;&nbsp;&nbsp;&nbsp;Not applicable. </P> <P STYLE="margin-top:18pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman"><B>Item&nbsp;6.
Contracts, Arrangements, Understandings or Relationships with Respect to Securities of the Issuer </B></P> <P STYLE="margin-top:6pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">The information set forth or incorporated by
reference in Item 4 is incorporated by reference in this Item 6. </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">The Reporting Person entered into a Confidentiality Agreement, dated as of
February&nbsp;4, 2020 (the &#147;Confidentiality Agreement&#148;), with the Issuer pursuant to which each party agreed to certain restrictions with respect to certain nonpublic information regarding the other party. In addition, the Confidentiality
Agreement provides that, for a period of eighteen (18)&nbsp;months from the date of the Confidentiality Agreement, unless approved in advance in writing by the board of directors of the other party, each party agrees that neither it, its direct or
indirect subsidiaries nor any of its or their representatives acting on behalf of it will, directly or indirectly: </P> <P STYLE="font-size:6pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="4%">&nbsp;</TD>
<TD WIDTH="5%" VALIGN="top" ALIGN="left">a)</TD>
<TD ALIGN="left" VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman; " ALIGN="left">make any proposal to the other party&#146;s board of directors, representatives or stockholders regarding, or
make any public announcement, proposal or offer with respect to, or otherwise solicit, seek or offer to effect (i)&nbsp;any business combination, merger, tender offer, exchange offer or similar transaction involving the other party, (ii)&nbsp;any
restructuring, recapitalization, liquidation or similar transaction involving the other party, or (iii)&nbsp;any acquisition of (x)&nbsp;the other party&#146;s loans, debt securities or equity securities, (y)&nbsp;rights or options to acquire
interests in the other party&#146;s loans, debt securities or equity securities, or (z)&nbsp;a material portion of the assets of the other party, provided, that this clause (iii)(x)-(y) does not apply to any acquisition of securities by any employee
benefit plan in the ordinary course of business and clause (iii)(z) does not apply to portions of assets that the other party is actively marketing; </P></TD></TR></TABLE> <P STYLE="font-size:6pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="4%">&nbsp;</TD>
<TD WIDTH="5%" VALIGN="top" ALIGN="left">b)</TD>
<TD ALIGN="left" VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman; " ALIGN="left">knowingly instigate, encourage or assist any third party (including forming a &#147;group&#148; as defined by
the Exchange Act) to do, or enter into any discussions or agreements with any third party with respect to, any of the actions set forth in (a)&nbsp;above; </P></TD></TR></TABLE> <P STYLE="font-size:6pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="4%">&nbsp;</TD>
<TD WIDTH="5%" VALIGN="top" ALIGN="left">c)</TD>
<TD ALIGN="left" VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman; " ALIGN="left">take any action which would reasonably be expected to require the other party to make a public announcement
regarding any of the actions set forth in (a)&nbsp;above; </P></TD></TR></TABLE> <P STYLE="font-size:6pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="4%">&nbsp;</TD>
<TD WIDTH="5%" VALIGN="top" ALIGN="left">d)</TD>
<TD ALIGN="left" VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman; " ALIGN="left">otherwise act, alone or in concert with others, to seek representation on the board of directors of the other
party or otherwise seek to control or substantially influence the management, board of directors or policies of the other party; </P></TD></TR></TABLE> <P STYLE="font-size:6pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="4%">&nbsp;</TD>
<TD WIDTH="5%" VALIGN="top" ALIGN="left">e)</TD>
<TD ALIGN="left" VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman; " ALIGN="left">publicly request or propose any waiver, amendment or termination of these standstill provisions; or
</P></TD></TR></TABLE> <P STYLE="font-size:6pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="4%">&nbsp;</TD>
<TD WIDTH="5%" VALIGN="top" ALIGN="left">f)</TD>
<TD ALIGN="left" VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman; " ALIGN="left">acquire (or publicly propose or agree to acquire), of record or beneficially, by purchase or otherwise,
(i)&nbsp;any loans, debt securities or equity securities of the other party, (ii)&nbsp;any rights or options to acquire interests in the other party&#146;s loans, debt securities or equity securities, or (iii)&nbsp;a material portion of the assets
of the other party, provided that (f)(i) to (ii)&nbsp;do not apply to any acquisition of securities by any employee benefit plan in the ordinary course of business and (f)(iii) will not apply to portions of assets that the other party is actively
marketing. </P></TD></TR></TABLE> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">The foregoing does not restrict either party, its direct or indirect subsidiaries or any of its representatives from making
any proposal regarding a possible strategic transaction directly to the board of directors or chief executive officer of the other party on a confidential basis if such proposal would not reasonably be expected to require the other party to make a
public announcement regarding the Confidentiality Agreement, such possible strategic transaction or any of the matters set forth in these standstill provisions. </P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">The standstill restrictions listed above would be inoperative and of no force or effect with respect to a party if (i)&nbsp;any other person or
&#147;group&#148; acquires or publicly proposes to acquire more than 50% of the outstanding voting securities of the other party or (ii)&nbsp;such other party or any of its affiliates enters into an agreement with a person other than a party hereto
or any of its affiliates, providing for a merger, share exchange, asset or equity sale or other business </P>
</DIV></Center>


<p style="margin-top:1em; margin-bottom:0em; page-break-before:always">
<HR SIZE="3" style="COLOR:#999999" WIDTH="100%" ALIGN="CENTER">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">
combination transaction pursuant to which the voting securities of such other party outstanding immediately prior to such transaction would constitute less than 50% of the outstanding voting
securities of such other party immediately following such transaction (or if such other party would not be the survivor or successor owner of its material assets after the merger, share exchange, asset or equity sale or other business combination,
the voting securities of such other party outstanding immediately prior to such transaction would be converted into, or exchanged for, in such transaction, less than 50% of the outstanding voting securities of the survivor or successor or its
publicly traded direct or indirect parent company). </P> <P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">Except for the Confidentiality Agreement, Merger Agreement and the Support Agreement described above,
to the knowledge of the Reporting Person, there are no contracts, arrangements, understandings or relationships (legal or otherwise), including, but not limited to, transfer or voting of any of the securities, finder&#146;s fees, joint ventures,
loan or option arrangements, puts or calls, guarantees of profits, division of profits or loss, or the giving or withholding of proxies, among the persons named in Item 2 or between such persons and any other person, with respect to any securities
of Issuer, including any securities pledged or otherwise subject to a contingency the occurrence of which would give another person voting power or investment power over such securities other than standard default and similar provisions contained in
loan agreements. </P> <P STYLE="margin-top:18pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman"><B>Item&nbsp;7. Material to Be Filed as Exhibits </B></P> <P STYLE="font-size:6pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE CELLSPACING="0" CELLPADDING="0" WIDTH="100%" BORDER="0" STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" ALIGN="center">


<TR>

<TD WIDTH="9%"></TD>

<TD VALIGN="bottom" WIDTH="1%"></TD>
<TD WIDTH="90%"></TD></TR>


<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">&nbsp;&nbsp;Exhibit&nbsp;A</TD>
<TD VALIGN="bottom">&nbsp;</TD>
<TD VALIGN="bottom">Agreement and Plan of Merger, dated as of August&nbsp;12, 2020 by and between Southwestern Energy Company and Montage Resources Corporation (incorporated by reference to Exhibit 2.1 to Amendment No.&nbsp;1 to the Current Report
on Form <FONT STYLE="white-space:nowrap">8-K/A</FONT> filed by Southwestern Energy Company with the SEC on August&nbsp;12, 2020).</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="8"></TD>
<TD HEIGHT="8" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">&nbsp;&nbsp;Exhibit&nbsp;B</TD>
<TD VALIGN="bottom">&nbsp;</TD>
<TD VALIGN="bottom">Support Agreement, dated as of August&nbsp;12, 2020 by and among Southwestern Energy Company and certain stockholders affiliated with EnCap Investments L.P. (incorporated by reference to Exhibit 10.1 to the Current Report on Form
<FONT STYLE="white-space:nowrap">8-K</FONT> filed by Southwestern Energy Company with the SEC on August&nbsp;12, 2020).</TD></TR>
</TABLE>
</DIV></Center>


<p style="margin-top:1em; margin-bottom:0em; page-break-before:always">
<HR SIZE="3" style="COLOR:#999999" WIDTH="100%" ALIGN="CENTER">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B>Signature </B></P>
<P STYLE="margin-top:6pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">After reasonable inquiry and to the best of my knowledge and belief,&nbsp;I certify that the information set forth in this statement is true, complete and
correct. </P> <P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE CELLSPACING="0" CELLPADDING="0" WIDTH="100%" BORDER="0" STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt">


<TR>

<TD WIDTH="50%"></TD>

<TD VALIGN="bottom" WIDTH="1%"></TD>
<TD WIDTH="49%"></TD></TR>


<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="bottom">Date: August&nbsp;21, 2020</TD>
<TD VALIGN="bottom">&nbsp;</TD>
<TD VALIGN="bottom">SOUTHWESTERN ENERGY COMPANY</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="bottom"></TD>
<TD VALIGN="bottom">&nbsp;</TD>
<TD VALIGN="bottom"> <P STYLE="margin-top:0pt; margin-bottom:1pt; border-bottom:1px solid #000000; font-size:10pt; font-family:Times New Roman">/s/ Chris Lacy</P></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="bottom"></TD>
<TD VALIGN="bottom">&nbsp;</TD>
<TD VALIGN="bottom">Name: Chris Lacy</TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="bottom"></TD>
<TD VALIGN="bottom">&nbsp;</TD>
<TD VALIGN="bottom">Title: &nbsp;&nbsp;Vice President, General Counsel&nbsp;&amp; Secretary</TD></TR>
</TABLE>
</DIV></Center>


<p style="margin-top:1em; margin-bottom:0em; page-break-before:always">
<HR SIZE="3" style="COLOR:#999999" WIDTH="100%" ALIGN="CENTER">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B><U>SCHEDULE A </U></B></P>
<P STYLE="margin-top:12pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman"><B>1.&nbsp;&nbsp;&nbsp;&nbsp;SOUTHWESTERN ENERGY COMPANY </B></P>
<P STYLE="margin-top:6pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman">The name, business address, title, present principal occupation or employment of each of the directors and executive officers of Southwestern Energy Company
(&#147;Southwestern&#148;), are set forth below. If no business address is given, the director&#146;s or executive officer&#146;s business address is 10000 Energy Drive, Spring, Texas 77389. Unless otherwise indicated, each occupation set forth
opposite an individual&#146;s name refers to Southwestern. Unless otherwise indicated below, all of the persons listed below are citizens of the United States of America. </P> <P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE CELLSPACING="0" CELLPADDING="0" WIDTH="100%" BORDER="0" STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" ALIGN="center">


<TR>

<TD WIDTH="30%"></TD>

<TD VALIGN="bottom" WIDTH="1%"></TD>
<TD WIDTH="69%"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:8pt">
<TD VALIGN="bottom" NOWRAP> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; border-bottom:1.00pt solid #000000; display:table-cell; font-size:8pt; font-family:Times New Roman; "><B>Name</B></P></TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="bottom" ALIGN="center" STYLE="border-bottom:1.00pt solid #000000"> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:8pt; font-family:Times New Roman" ALIGN="center"><B>Present Principal Occupation Including Name and Address of
Employer</B></P></TD></TR>


<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="bottom"><I>Directors</I></TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="bottom"></TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Catherine A. Kehr</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top" ALIGN="center">Director</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">John D. Gass</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top" ALIGN="center">Director</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Greg D. Kerley</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top" ALIGN="center">Director</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Jon A. Marshall</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top" ALIGN="center">Director</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Patrick M. Prevost</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top" ALIGN="center">Director</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Anne Taylor</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top" ALIGN="center">Director</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Denis J. Walsh III, CFA</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top" ALIGN="center">Director</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Sylvester &#147;Chip&#148; Johnson</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top" ALIGN="center">Director</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Bill Way</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top" ALIGN="center">President&nbsp;&amp; Chief Executive Officer, Director</TD></TR>
</TABLE> <P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE CELLSPACING="0" CELLPADDING="0" WIDTH="100%" BORDER="0" STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" ALIGN="center">


<TR>

<TD WIDTH="30%"></TD>

<TD VALIGN="bottom" WIDTH="1%"></TD>
<TD WIDTH="69%"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:8pt">
<TD VALIGN="bottom" NOWRAP> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; border-bottom:1.00pt solid #000000; display:table-cell; font-size:8pt; font-family:Times New Roman; "><B>Name</B></P></TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="bottom" ALIGN="center" STYLE="border-bottom:1.00pt solid #000000"> <P STYLE="margin-top:0pt; margin-bottom:1pt; font-size:8pt; font-family:Times New Roman" ALIGN="center"><B>Present Principal Occupation Including Name and Address of
Employer</B></P></TD></TR>


<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="bottom"><I>Executive&nbsp;Officers&nbsp;(Who&nbsp;Are&nbsp;Not&nbsp;Directors)</I></TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="bottom"></TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Julian Bott</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top">Executive Vice President&nbsp;&amp; Chief Financial Officer</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Clay Carrell</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top">Executive Vice President&nbsp;&amp; Chief Operating Officer</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Jenny McCauley</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top">Senior Vice President - Administration</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Chris Lacy</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top">Vice President, General Counsel&nbsp;&amp; Corporate Secretary</TD></TR>
<TR STYLE="font-size:1pt">
<TD HEIGHT="16"></TD>
<TD HEIGHT="16" COLSPAN="2"></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top">Jason Kurtz</TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="top">Vice President - Marketing&nbsp;&amp; Transportation</TD></TR>
</TABLE>
</DIV></Center>


<p style="margin-top:1em; margin-bottom:0em; page-break-before:always">
<HR SIZE="3" style="COLOR:#999999" WIDTH="100%" ALIGN="CENTER">


<Center><DIV STYLE="width:8.5in" align="left">
 <P STYLE="margin-top:0pt; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman" ALIGN="center"><B><U>SCHEDULE B </U></B></P>
<P STYLE="font-size:12pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE CELLSPACING="0" CELLPADDING="0" WIDTH="68%" BORDER="0" STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" ALIGN="center">


<TR>

<TD WIDTH="83%"></TD>

<TD VALIGN="bottom" WIDTH="6%"></TD>
<TD></TD>
<TD></TD>
<TD></TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:8pt">
<TD VALIGN="bottom" NOWRAP> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; border-bottom:1.00pt solid #000000; display:table-cell; font-size:8pt; font-family:Times New Roman; "><B>Name of Stockholder</B></P></TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="bottom" COLSPAN="2" ALIGN="center" STYLE="border-bottom:1.00pt solid #000000"><B>No.&nbsp;Shares&nbsp;of<BR>Company<BR>Common&nbsp;Stock</B></TD>
<TD VALIGN="bottom">&nbsp;</TD></TR>


<TR BGCOLOR="#cceeff" STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; margin-left:1.00em; text-indent:-1.00em; font-size:10pt; font-family:Times New Roman">EnCap Energy Capital Fund VIII <FONT STYLE="white-space:nowrap">Co-Investors,</FONT> L.P.<SUP
STYLE="font-size:85%; vertical-align:top">(1)</SUP></P></TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="bottom">&nbsp;</TD>
<TD VALIGN="bottom" ALIGN="right">2,694,673</TD>
<TD NOWRAP VALIGN="bottom">&nbsp;</TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; margin-left:1.00em; text-indent:-1.00em; font-size:10pt; font-family:Times New Roman">EnCap Energy Capital Fund VIII,
L.P.<SUP STYLE="font-size:85%; vertical-align:top">(1)</SUP></P></TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="bottom">&nbsp;</TD>
<TD VALIGN="bottom" ALIGN="right">3,979,173</TD>
<TD NOWRAP VALIGN="bottom">&nbsp;</TD></TR>
<TR BGCOLOR="#cceeff" STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; margin-left:1.00em; text-indent:-1.00em; font-size:10pt; font-family:Times New Roman">EnCap Energy Capital Fund IX,
L.P.<SUP STYLE="font-size:85%; vertical-align:top">(1)</SUP></P></TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="bottom">&nbsp;</TD>
<TD VALIGN="bottom" ALIGN="right">4,856,485</TD>
<TD NOWRAP VALIGN="bottom">&nbsp;</TD></TR>
<TR STYLE="page-break-inside:avoid ; font-family:Times New Roman; font-size:10pt">
<TD VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; margin-left:1.00em; text-indent:-1.00em; font-size:10pt; font-family:Times New Roman">TPR Residual Assets, LLC<SUP STYLE="font-size:85%; vertical-align:top">(2)</SUP></P></TD>
<TD VALIGN="bottom">&nbsp;&nbsp;</TD>
<TD VALIGN="bottom">&nbsp;</TD>
<TD VALIGN="bottom" ALIGN="right">2,521,573</TD>
<TD NOWRAP VALIGN="bottom">&nbsp;</TD></TR>
</TABLE> <P STYLE="line-height:8.0pt;margin-top:0pt;margin-bottom:2pt;border-bottom:1px solid #000000;width:11%">&nbsp;</P> <P STYLE="font-size:6pt;margin-top:0pt;margin-bottom:0pt">&nbsp;</P>
<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="4%" VALIGN="top" ALIGN="left">(1)</TD>
<TD ALIGN="left" VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman; " ALIGN="left">EnCap Energy Capital Fund VIII, L.P., a Texas limited partnership (&#147;<U>EnCap Fund VIII</U>&#148;), EnCap
Energy Capital Fund IX, L.P., a Texas limited partnership (&#147;<U>EnCap Fund IX</U>&#148;), EnCap Energy Capital Fund VIII <FONT STYLE="white-space:nowrap">Co-Investors,</FONT> L.P., a Texas limited partnership (&#147;<U>EnCap Fund VIII <FONT
STYLE="white-space:nowrap">Co-Invest</FONT></U>&#148; and together with EnCap Fund VIII and EnCap Fund IX, the &#147;<U>EnCap Funds</U>&#148;), collectively directly hold the remaining shares of common stock. EnCap Partners GP, LLC (&#147;<U>EnCap
Partners GP</U>&#148;) is the sole general partner of EnCap Partners, LP (&#147;<U>EnCap Partners</U>&#148;), which is the managing member of EnCap Investments Holdings, LLC (&#147;<U>EnCap Holdings</U>&#148;), which is the sole member of EnCap
Investments Holdings Blocker, LLC (&#147;<U>EnCap Holdings Blocker</U>&#148;). EnCap Holdings Blocker is the sole member of EnCap Investments GP, L.L.C. (&#147;<U>EnCap Investments GP</U>&#148;), which is the sole general partner of EnCap
Investments L.P. (&#147;<U>EnCap Investments LP</U>&#148;). EnCap Investments LP is the sole general partner of EnCap Equity Fund VIII GP, L.P. (&#147;<U>EnCap Fund VIII GP</U>&#148;) and EnCap Equity Fund IX GP, L.P. (&#147;<U>EnCap Fund IX
GP</U>&#148;). EnCap Fund VIII GP is the sole general partner of each of EnCap Fund VIII and EnCap Fund VIII <FONT STYLE="white-space:nowrap">Co-Invest.</FONT> EnCap Fund IX GP is the sole general partner of EnCap Fund IX. Therefore, EnCap Partners
GP may be deemed to share the right to direct the voting and disposition of the Subject Shares held by the EnCap Funds. </P></TD></TR></TABLE>
<TABLE STYLE="BORDER-COLLAPSE:COLLAPSE; font-family:Times New Roman; font-size:10pt" BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="100%">
<TR style = "page-break-inside:avoid">
<TD WIDTH="4%" VALIGN="top" ALIGN="left">(2)</TD>
<TD ALIGN="left" VALIGN="top"> <P STYLE=" margin-top:0pt ; margin-bottom:0pt; font-size:10pt; font-family:Times New Roman; " ALIGN="left">TPR Residual Assets, LLC (&#147;<U>TPR Residual</U>&#148;) is member-managed by EnCap Fund IX. As a result,
EnCap Fund IX may be deemed to have the power to vote or direct the vote or to dispose or direct the disposition of the shares owned by TPR Residual. </P></TD></TR></TABLE>
</DIV></Center>

</BODY></HTML>'''
    tb=get_table_layers(BeautifulSoup(t1,'xml'))
    for k,v in tb.items():
        print(f'{k} : {v}')
