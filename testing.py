import asyncio as aio
import sys
import time as t
from types import NoneType

from bs4 import BeautifulSoup

from data import http,postgres,edgar
from util import xml

# async def test_yield():
#     for i in range

async def testing():
    await edgar.update_edgar_archive()
    await postgres.close_pgclient()
    await http.httpClient().connector.close()
    await http.httpClient().close()


def test_str():
    return'''
<SEC-DOCUMENT>0001816616-21-000007.txt : 20211112
<SEC-HEADER>0001816616-21-000007.hdr.sgml : 20211112
<ACCEPTANCE-DATETIME>20211112153335
ACCESSION NUMBER:		0001816616-21-000007
CONFORMED SUBMISSION TYPE:	13F-HR
PUBLIC DOCUMENT COUNT:		2
CONFORMED PERIOD OF REPORT:	20210930
FILED AS OF DATE:		20211112
DATE AS OF CHANGE:		20211112
EFFECTIVENESS DATE:		20211112

FILER:

	COMPANY DATA:	
		COMPANY CONFORMED NAME:			NZS Capital, LLC
		CENTRAL INDEX KEY:			0001816616
		IRS NUMBER:				841821721
		STATE OF INCORPORATION:			CO
		FISCAL YEAR END:			1231

	FILING VALUES:
		FORM TYPE:		13F-HR
		SEC ACT:		1934 Act
		SEC FILE NUMBER:	028-20310
		FILM NUMBER:		211402988

	BUSINESS ADDRESS:	
		STREET 1:		1756 PLATTE STREET
		CITY:			DENVER
		STATE:			CO
		ZIP:			80202
		BUSINESS PHONE:		720-551-7113

	MAIL ADDRESS:	
		STREET 1:		1756 PLATTE STREET
		CITY:			DENVER
		STATE:			CO
		ZIP:			80202
</SEC-HEADER>
<DOCUMENT>
<TYPE>13F-HR
<SEQUENCE>1
<FILENAME>primary_doc.xml
<TEXT>
<XML>
<?xml version="1.0" encoding="UTF-8"?>
    <edgarSubmission xmlns="http://www.sec.gov/edgar/thirteenffiler" xmlns:com="http://www.sec.gov/edgar/common">
      <headerData>
        <submissionType>13F-HR</submissionType>
        <filerInfo>
          <liveTestFlag>LIVE</liveTestFlag>
          <flags>
            <confirmingCopyFlag>false</confirmingCopyFlag>
            <returnCopyFlag>true</returnCopyFlag>
            <overrideInternetFlag>false</overrideInternetFlag>
          </flags>
          <filer>
            <credentials>
              <cik>0001816616</cik>
              <ccc>XXXXXXXX</ccc>
            </credentials>
          </filer>
          <periodOfReport>09-30-2021</periodOfReport>
        </filerInfo>
      </headerData>
      <formData>
        <coverPage>
          <reportCalendarOrQuarter>09-30-2021</reportCalendarOrQuarter>
          <filingManager>
            <name>NZS Capital, LLC</name>
            <address>
              <com:street1>1756 PLATTE STREET</com:street1>
              <com:city>DENVER</com:city>
              <com:stateOrCountry>CO</com:stateOrCountry>
              <com:zipCode>80202</com:zipCode>
            </address>
          </filingManager>
          <reportType>13F HOLDINGS REPORT</reportType>
          <form13FFileNumber>028-20310</form13FFileNumber>
          <provideInfoForInstruction5>N</provideInfoForInstruction5>
        </coverPage>
        <signatureBlock>
          <name>Adam Schor</name>
          <title>President, CCO</title>
          <phone>720-551-7113</phone>
          <signature>Adam Schor</signature>
          <city>DENVER</city>
          <stateOrCountry>CO</stateOrCountry>
          <signatureDate>11-12-2021</signatureDate>
        </signatureBlock>
        <summaryPage>
          <otherIncludedManagersCount>0</otherIncludedManagersCount>
          <tableEntryTotal>68</tableEntryTotal>
          <tableValueTotal>1012805</tableValueTotal>
          <isConfidentialOmitted>false</isConfidentialOmitted>
        </summaryPage>
      </formData>
    </edgarSubmission>
</XML>
</TEXT>
</DOCUMENT>
<DOCUMENT>
<TYPE>INFORMATION TABLE
<SEQUENCE>2
<FILENAME>13FNZS_Q32021.xml
<TEXT>
<XML>
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <ns1:informationTable xmlns:ns1="http://www.sec.gov/edgar/document/thirteenf/informationtable">
        <ns1:infoTable>
            <ns1:nameOfIssuer>AUTODESK INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>052769106</ns1:cusip>
            <ns1:value>11216</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>39332</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>39332</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>AMPHENOL CORP NEW</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL A</ns1:titleOfClass>
            <ns1:cusip>032095101</ns1:cusip>
            <ns1:value>31709</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>433001</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>433001</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>BALL CORP</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>058498106</ns1:cusip>
            <ns1:value>16633</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>184871</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>184871</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>CADENCE DESIGN SYSTEM INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>127387108</ns1:cusip>
            <ns1:value>14919</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>98516</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>98516</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>CHIPOTLE MEXICAN GRILL INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>169656105</ns1:cusip>
            <ns1:value>6710</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>3692</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>3692</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>SALESFORCE COM INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>79466L302</ns1:cusip>
            <ns1:value>55747</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>205543</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>205543</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>FASTENAL CO</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>311900104</ns1:cusip>
            <ns1:value>5627</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>109021</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>109021</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>LAM RESEARCH CORP</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>512807108</ns1:cusip>
            <ns1:value>31666</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>55637</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>55637</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>MICROCHIP TECHNOLOGY INC.</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>595017104</ns1:cusip>
            <ns1:value>41796</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>272304</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>272304</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>MICROSOFT CORP</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>594918104</ns1:cusip>
            <ns1:value>72801</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>258233</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>258233</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>CLOUDFLARE INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL A COM</ns1:titleOfClass>
            <ns1:cusip>18915M107</ns1:cusip>
            <ns1:value>10378</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>92124</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>92124</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>NVIDIA CORPORATION</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>67066G104</ns1:cusip>
            <ns1:value>25161</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>121458</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>121458</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>REDFIN CORP</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>75737F108</ns1:cusip>
            <ns1:value>9497</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>189554</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>189554</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>SAILPOINT TECHNOLOGIES HLDGS</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>78781P105</ns1:cusip>
            <ns1:value>17069</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>398065</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>398065</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>SHOPIFY INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL A</ns1:titleOfClass>
            <ns1:cusip>82509L107</ns1:cusip>
            <ns1:value>10997</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>8111</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>8111</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>SQUARE INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL A</ns1:titleOfClass>
            <ns1:cusip>852234103</ns1:cusip>
            <ns1:value>13861</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>57793</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>57793</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>T-MOBILE US INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>872590104</ns1:cusip>
            <ns1:value>30985</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>242523</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>242523</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>TESLA INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>88160R101</ns1:cusip>
            <ns1:value>8485</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>10942</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>10942</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>TAIWAN SEMICONDUCTOR MFG LTD</ns1:nameOfIssuer>
            <ns1:titleOfClass>SPONSORED ADS</ns1:titleOfClass>
            <ns1:cusip>874039100</ns1:cusip>
            <ns1:value>14109</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>126364</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>126364</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>TWITTER INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>90184L102</ns1:cusip>
            <ns1:value>13373</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>221451</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>221451</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>TEXAS INSTRS INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>882508104</ns1:cusip>
            <ns1:value>41935</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>218174</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>218174</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>VIACOMCBS INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL B</ns1:titleOfClass>
            <ns1:cusip>92556H206</ns1:cusip>
            <ns1:value>15657</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>396269</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>396269</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>WORKDAY INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL A</ns1:titleOfClass>
            <ns1:cusip>98138H101</ns1:cusip>
            <ns1:value>37506</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>150089</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>150089</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>AIRBNB INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM CL A</ns1:titleOfClass>
            <ns1:cusip>009066101</ns1:cusip>
            <ns1:value>5905</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>35202</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>35202</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>AFFIRM HLDGS INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM CL A</ns1:titleOfClass>
            <ns1:cusip>00827B106</ns1:cusip>
            <ns1:value>4123</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>34606</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>34606</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>AMAZON COM INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>023135106</ns1:cusip>
            <ns1:value>29969</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>9123</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>9123</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>ANSYS INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>03662Q105</ns1:cusip>
            <ns1:value>7703</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>22626</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>22626</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>ASML HOLDING N V</ns1:nameOfIssuer>
            <ns1:titleOfClass>N Y REGISTRY SHS</ns1:titleOfClass>
            <ns1:cusip>N07059210</ns1:cusip>
            <ns1:value>13741</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>18441</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>18441</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>CROWN CASTLE INTL CORP NEW</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>22822V101</ns1:cusip>
            <ns1:value>24277</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>140070</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>140070</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>COUPA SOFTWARE INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>22266L106</ns1:cusip>
            <ns1:value>5719</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>26092</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>26092</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>CREE INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>225447101</ns1:cusip>
            <ns1:value>4790</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>59329</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>59329</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>CONSTELLIUM SE</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL A SHS</ns1:titleOfClass>
            <ns1:cusip>F21107101</ns1:cusip>
            <ns1:value>4819</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>256598</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>256598</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>CATALENT INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>148806102</ns1:cusip>
            <ns1:value>3985</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>29945</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>29945</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>CYBERARK SOFTWARE LTD</ns1:nameOfIssuer>
            <ns1:titleOfClass>SHS</ns1:titleOfClass>
            <ns1:cusip>M2682V108</ns1:cusip>
            <ns1:value>14045</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>88996</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>88996</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>DISNEY WALT CO</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>254687106</ns1:cusip>
            <ns1:value>21399</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>126494</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>126494</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>GINKGO BIOWORKS HOLDINGS INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL A SHS</ns1:titleOfClass>
            <ns1:cusip>37611X100</ns1:cusip>
            <ns1:value>443</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>38258</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>38258</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>FISERV INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>337738108</ns1:cusip>
            <ns1:value>16361</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>150796</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>150796</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>FARFETCH LTD</ns1:nameOfIssuer>
            <ns1:titleOfClass>ORD SH CL A</ns1:titleOfClass>
            <ns1:cusip>30744W107</ns1:cusip>
            <ns1:value>5002</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>133465</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>133465</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>ALPHABET INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CAP STK CL C</ns1:titleOfClass>
            <ns1:cusip>02079K107</ns1:cusip>
            <ns1:value>69685</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>26145</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>26145</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>ILLUMINA INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>452327109</ns1:cusip>
            <ns1:value>437</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>1078</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>1078</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>INTUITIVE SURGICAL INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM NEW</ns1:titleOfClass>
            <ns1:cusip>46120E602</ns1:cusip>
            <ns1:value>2622</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>2637</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>2637</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>KEYSIGHT TECHNOLOGIES INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>49338L103</ns1:cusip>
            <ns1:value>11242</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>68430</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>68430</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>KLA CORP</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM NEW</ns1:titleOfClass>
            <ns1:cusip>482480100</ns1:cusip>
            <ns1:value>24386</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>72900</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>72900</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>MELI KASZEK PIONEER CORP</ns1:nameOfIssuer>
            <ns1:titleOfClass>CLASS A ORD</ns1:titleOfClass>
            <ns1:cusip>G5S74L106</ns1:cusip>
            <ns1:value>1658</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>150000</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>150000</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>MERCADOLIBRE INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>58733R102</ns1:cusip>
            <ns1:value>9393</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>5593</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>5593</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>MOMENTIVE GLOBAL INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>60878Y108</ns1:cusip>
            <ns1:value>2953</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>150648</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>150648</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>MICRON TECHNOLOGY INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>595112103</ns1:cusip>
            <ns1:value>18079</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>254711</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>254711</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>NEXTERA ENERGY INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>65339F101</ns1:cusip>
            <ns1:value>5968</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>76009</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>76009</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>OKTA INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL A</ns1:titleOfClass>
            <ns1:cusip>679295105</ns1:cusip>
            <ns1:value>11578</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>48783</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>48783</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>PELOTON INTERACTIVE INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL A COM</ns1:titleOfClass>
            <ns1:cusip>70614W100</ns1:cusip>
            <ns1:value>7514</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>86318</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>86318</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>PAYPAL HLDGS INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>70450Y103</ns1:cusip>
            <ns1:value>18935</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>72768</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>72768</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>SILICON LABORATORIES INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>826919102</ns1:cusip>
            <ns1:value>7928</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>56564</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>56564</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>SNAP INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL A</ns1:titleOfClass>
            <ns1:cusip>83304A106</ns1:cusip>
            <ns1:value>10267</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>138981</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>138981</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>SONY GROUP CORPORATION</ns1:nameOfIssuer>
            <ns1:titleOfClass>SPONSORED ADR</ns1:titleOfClass>
            <ns1:cusip>835699307</ns1:cusip>
            <ns1:value>5597</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>50611</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>50611</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>SUN CMNTYS INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>866674104</ns1:cusip>
            <ns1:value>12521</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>67643</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>67643</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>THOR INDS INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>885160101</ns1:cusip>
            <ns1:value>2465</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>20079</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>20079</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>TRANE TECHNOLOGIES PLC</ns1:nameOfIssuer>
            <ns1:titleOfClass>SHS</ns1:titleOfClass>
            <ns1:cusip>G8994E103</ns1:cusip>
            <ns1:value>5150</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>29829</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>29829</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>TYLER TECHNOLOGIES INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>902252105</ns1:cusip>
            <ns1:value>10830</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>23612</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>23612</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>UNITY SOFTWARE INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>91332U101</ns1:cusip>
            <ns1:value>1692</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>13401</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>13401</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>WORKIVA INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM CL A</ns1:titleOfClass>
            <ns1:cusip>98139A105</ns1:cusip>
            <ns1:value>4095</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>29048</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>29048</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>ZILLOW GROUP INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL C CAP STK</ns1:titleOfClass>
            <ns1:cusip>98954M200</ns1:cusip>
            <ns1:value>4446</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>50448</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>50448</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>ZENDESK INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>98936J101</ns1:cusip>
            <ns1:value>12932</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>111108</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>111108</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>APPLE INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>037833100</ns1:cusip>
            <ns1:value>29465</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>208234</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>208234</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>CROWDSTRIKE HLDGS INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CL A</ns1:titleOfClass>
            <ns1:cusip>22788C105</ns1:cusip>
            <ns1:value>1430</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>5819</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>5819</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>ALPHABET INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>CAP STK CL A</ns1:titleOfClass>
            <ns1:cusip>02079K305</ns1:cusip>
            <ns1:value>5179</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>1937</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>1937</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>ON SEMICONDUCTOR CORP</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>682189105</ns1:cusip>
            <ns1:value>5972</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>130473</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>130473</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>TAKE-TWO INTERACTIVE SOFTWAR</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>874054109</ns1:cusip>
            <ns1:value>5346</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>34699</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>34699</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
        <ns1:infoTable>
            <ns1:nameOfIssuer>NETFLIX INC</ns1:nameOfIssuer>
            <ns1:titleOfClass>COM</ns1:titleOfClass>
            <ns1:cusip>64110L106</ns1:cusip>
            <ns1:value>2922</ns1:value>
            <ns1:shrsOrPrnAmt>
                <ns1:sshPrnamt>4787</ns1:sshPrnamt>
                <ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
            </ns1:shrsOrPrnAmt>
            <ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
            <ns1:votingAuthority>
                <ns1:Sole>4787</ns1:Sole>
                <ns1:Shared>0</ns1:Shared>
                <ns1:None>0</ns1:None>
            </ns1:votingAuthority>
        </ns1:infoTable>
    </ns1:informationTable>
</XML>
</TEXT>
</DOCUMENT>
</SEC-DOCUMENT>'''

def t2():
    return'''
<SEC-DOCUMENT>0001144204-13-026736.txt : 20130507
<SEC-HEADER>0001144204-13-026736.hdr.sgml : 20130507
<ACCEPTANCE-DATETIME>20130507130216
ACCESSION NUMBER:		0001144204-13-026736
CONFORMED SUBMISSION TYPE:	13F-HR
PUBLIC DOCUMENT COUNT:		1
CONFORMED PERIOD OF REPORT:	20130331
FILED AS OF DATE:		20130507
DATE AS OF CHANGE:		20130507
EFFECTIVENESS DATE:		20130507

FILER:

	COMPANY DATA:	
		COMPANY CONFORMED NAME:			ITHAKA GROUP LLC
		CENTRAL INDEX KEY:			0001484043
		IRS NUMBER:				262269925
		STATE OF INCORPORATION:			DE
		FISCAL YEAR END:			1231

	FILING VALUES:
		FORM TYPE:		13F-HR
		SEC ACT:		1934 Act
		SEC FILE NUMBER:	028-13786
		FILM NUMBER:		13818994

	BUSINESS ADDRESS:	
		STREET 1:		3 BETHESDA METRO CENTER
		CITY:			BETHESDA
		STATE:			MD
		ZIP:			20814
		BUSINESS PHONE:		240 395 5000

	MAIL ADDRESS:	
		STREET 1:		3 BETHESDA METRO CENTER
		CITY:			BETHESDA
		STATE:			MD
		ZIP:			20814
</SEC-HEADER>
<DOCUMENT>
<TYPE>13F-HR
<SEQUENCE>1
<FILENAME>v344165_13fhr.txt
<DESCRIPTION>13F-HR
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
<CAPTION>
                                                        FORM 13F INFORMATION TABLE

                                                           VALUE   SHARES/  SH/ PUT/ INVSTMT    OTHER          VOTING AUTHORITY
        NAME OF ISSUER          TITLE OF CLASS    CUSIP   (x$1000) PRN AMT  PRN CALL DSCRETN   MANAGERS     SOLE    SHARED    NONE
------------------------------ ---------------- --------- -------- -------- --- ---- ------- ------------ -------- -------- --------
<S>                            <C>              <C>        <C>       <C>    <C>  <C> <C>      <C>          <C>      <C>       <C>
ARM Holdings plc               COM               42068106   8878     209527 SH       Sole                   187907            21620
Alexion Pharmaceuticals        COM               15351109   3889      42210 SH       Sole                    37445             4765
Allergan Inc.                  COM               18490102   6673      59774 SH       Sole                    53455             6319
Amazon.com Inc.                COM               23135106  14668      55043 SH       Sole                    48557             6486
American Tower Corporation     COM              03027X100   6585      85611 SH       Sole                    74121            11490
Apple Inc.                     COM               37833100  15403      34796 SH       Sole                    30355             4441
B/E Aerospace, Inc.            COM               73302101  12564     208420 SH       Sole                   181703            26717
Caterpillar Inc                COM              149123101   6019      69212 SH       Sole                    60679             8533
Chipotle Mexican Grill         COM              169656105   4038      12391 SH       Sole                    11130             1261
Coach Inc                      COM              189754104   8364     167318 SH       Sole                   149935            17383
Cummins Inc.                   COM              231021106   8038      69403 SH       Sole                    61626             7777
F5 Networks Inc.               COM              315616102   5206      58443 SH       Sole                    51202             7241
Facebook, Inc. cl A            COM              30303M102   3512     137282 SH       Sole                   124967            12315
General Electric Company       COM              369604103    208       9000 SH       Sole                                      9000
Gilead Sciences Inc.           COM              375558103   3198      65337 SH       Sole                    57657             7680
Google Inc                     COM              38259P508    382        481 SH       Sole                       71              410
Intuitive Surgical, Inc.       COM              46120E602  11198      22798 SH       Sole                    19562             3236
Johnson Controls, Inc.         COM              478366107   7365     210000 SH       Sole                                    210000
Las Vegas Sands Corp.          COM              517834107   6033     107055 SH       Sole                    96662            10393
LinkedIn Corp cl A             COM              53578A108  17432      99013 SH       Sole                    88509            10504
Mastercard Inc.                COM              57636Q104  21087      38968 SH       Sole                    34297             4671
Michael Kors Holdings Ltd      COM              G60754101   5725     100812 SH       Sole                    88976            11836
Microsoft Corporation          COM              594918104    356      12445 SH       Sole                     2445            10000
National Oilwell Varco Inc     COM              637071101   9848     139196 SH       Sole                   121331            17865
Precision Castparts Corp       COM              740189105   9804      51704 SH       Sole                    45381             6323
Priceline.com Inc.             COM              741503403  12153      17660 SH       Sole                    15558             2102
Procter & Gamble Co.           COM              742718109    308       4000 SH       Sole                                      4000
Qualcomm Inc.                  COM              747525103  11759     175668 SH       Sole                   155587            20081
Red Hat, Inc.                  COM              756577102   4971      98319 SH       Sole                    87570            10749
Regeneron Pharmaceuticals      COM              75886F107   4343      24617 SH       Sole                    22133             2484
Salesforce.com Inc             COM              79466L302  11297      63173 SH       Sole                    55312             7861
Schlumberger Ltd.              COM              806857108    339       4530 SH       Sole                      360             4170
Starbucks Corporation          COM              855244109  10822     190030 SH       Sole                   167741            22289
T Rowe Price Group Inc         COM              74144T108    240       3200 SH       Sole                                      3200
Transdigm Group, Inc.          COM              893641100   6878      44981 SH       Sole                    39839             5142
Ulta Salon, Cosmetics          COM              90384S303   5518      67878 SH       Sole                    60298             7580
Under Armour, Inc. Cl A        COM              904311107   5843     114127 SH       Sole                   102061            12066
VISA Inc.                      COM              92826C839  12700      74775 SH       Sole                    62662            12113
VMware, Inc. Cl A              COM              928563402   3652      46296 SH       Sole                    40548             5748
Whole Foods Market Inc.        COM              966837106   7224      83277 SH       Sole                    73937             9340
eBay Inc.                      COM              278642103   8935     164790 SH       Sole                   147195            17595
</TABLE>
</TEXT>
</DOCUMENT>
</SEC-DOCUMENT>
    '''

if __name__=="__main__":
    tm=t.time()
    sps=xml.xml_soups(test_str())
    _N = xml.TKeys.IGNORE
    _A = xml.TKeys.ADD
    tbls=xml.get_table_layers(sps,k_proc={'submissionType':_N,'cik':_N,'periodOfReport':_N,'name':_N,'street1':_N,'street2':_N,
      'city':_N,'stateOrCountry':_N,'zipCode':_N,'form13FFileNumber':_N,'filingManager':_N,
      'signatureBlock':_A})
    print((t.time()-tm)*1000.)
    # for i in sps:
    #     pass
    #     print(list(i.children)[0].prettify())
        #print(i.children.prettify())
    for k,v in tbls.items():
        print(f'{k} : {v}')

    # print(sps[1].infoTable.nameOfIssuer.text)
    # print([i.name for i in sps[1].informationTable.findChildren(recursive=False)])
    # print([i.name for i in sps[1].recursiveChildGenerator()])
    #sps[1].
    # sp=BeautifulSoup(test_str(), 'xml')
    # print(sp.prettify())

    # import asyncio
    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(testing())
    # finally:
    #     pass
    #     #loop.close()