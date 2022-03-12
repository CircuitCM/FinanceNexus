from pandas import DataFrame
from pandas._libs.missing import NAType
import pandas as pd
from datetime import date,datetime,time,timedelta
import plotly.graph_objects as grap
from plotly import subplots as sub
import cwdmaker as crd
import os
import asyncio



async def _tester():
    pd.set_option('max_rows',None)
    pd.set_option('max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('max_colwidth', None)
    rf,univ = await _get_data(['ADLVX.O','ACEAX.O'], ['TR.FdSecurityOwnedRIC.date','TR.FdSecurityOwnedRIC','TR.FdSecurityOwnedName','TR.FdInvestorPctPortfolio','TR.FdInvestorValueHeld'],{'SDate':0,'EDate':-1000000000,'Frq':'F','EndNum':0,'Curn':'USD'})
    #{'SDate':0,'EDate':-1000000000,'Frq':'F','EndNum':0,'CH':'date'}
    #"SDate=0 EDate=-1000000000 Frq=F EndNum=0 CH=date"
    #{'SDate':0,'EDate':-1000000000,'Frq':'F','EndNum':0,'CH':'date'}'CH':'Fd','RH':'Date'
    rf:FundamentalResponse
    print(rf._request_message)
    #print(rf._response.json())
    #print(rf._response.text)
    frm=rf.data.df
    print(frm)
    await close_session()

def try_float_bns(tp):
    try:
        return f'$ {"{:.1f}".format(float(tp)/(10**9))} Bn'
    except:
        return tp

def rm_nan(df:DataFrame):
    return df[~df.isnull()]

async def export_plots(ls,ndr):
    pd.set_option('max_rows', None)
    pd.set_option('max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('max_colwidth', None)
    td=date.today()
    ld=date(td.year-5,td.month,td.day)
    #shd=date(ld.year-1,ld.month,ld.day)
    params={'SDate': ld.isoformat(), 'EDate': td.isoformat(),'Period':'NTM','Curn':'USD'}
    r1,sp,nm = await get_ricnames(ls,ld,td)
    r1.infer_objects()
    sp.infer_objects()
    nm.infer_objects()
    nst= {k:v[0:25 if len(v)>25 else len(v)] if type(v)!= NAType else v for k,v in zip(nm.iloc[:, 0],nm.iloc[:, 1])}
    sectr = {k:v[0:30 if len(v)>30 else len(v)] if type(v)!= NAType else v for k, v in zip(nm.iloc[:, 0], nm.iloc[:, 3])}
    mktcp = {k: try_float_bns(v) for k, v in zip(nm.iloc[:, 0], nm.iloc[:, 2])}
    print('here')
    #TR.FCFPSSmartEst
    #TR.FreeCashFlow/TR.BasicWeightedAvgShares
    #TR.BasicWeightedAvgShares
    #TR.RevenueSmartEst
    #TR.BasicWeightedAvgShares(Period=LTM)
    #TR.EpsSmartEst
    #TR.PriceClose
    #TR.FwdPtoEPSSmartEst
    #TR.RevenueSmartEst/TR.BasicWeightedAvgShares(Period=LTM)
    ins =['TR.PriceClose.date','TR.PriceClose',
          'TR.FCFPSSmartEst.date','TR.FCFPSSmartEst',
          'TR.RevenueSmartEst.date','TR.RevenueSmartEst/TR.BasicWeightedAvgShares(Period=LTM,Frq=D)',
          'TR.EpsSmartEst.date','TR.EpsSmartEst', 'TR.CompanySharesOutstanding'
          #f'TR.BasicWeightedAvgShares(Period=LTM,SDate={shd.isoformat()}).date',f'TR.BasicWeightedAvgShares(Period=LTM,SDate={shd.isoformat()})']
          ]
    #TR.TtlCmnSharesOut
    g='rgb(0,190,0)'
    b='rgb(0,0,190)'
    ps=0
    fdir=crd.CURDR+ndr+'/'
    if not os.path.exists(fdir):
        os.mkdir(fdir)
    async for i,univ in yield_data(separate_universe(ls,ins,params)):
        ps+=1
        if i is not None or i.data is not None or i.data.df is not None: dat=i.data.df
        else:
            print(f'No results found for {univ} skipping.')
            continue
        try:
            #improves throughput of awaitable tasks b4 high process task
            await asyncio.sleep(0)
            dat.columns=[dat.columns[0],*ins]
            #spd =spd.rename(columns={k:v for k,v in zip(spd.columns[1:],ins)}, errors="raise")

            #dat:DataFrame =dat.apply(lambda *args,**kwargs:pd.to_numeric(*args,**(kwargs|{'errors':'ignore'})))
            dat:DataFrame=dat.infer_objects()
            dat['TR.PriceClose']=dat['TR.PriceClose'].astype(float,copy=False,errors='ignore')
            dat['TR.FCFPSSmartEst']=dat['TR.FCFPSSmartEst'].astype(float, copy=False, errors='ignore')
            dat['TR.RevenueSmartEst/TR.BasicWeightedAvgShares(Period=LTM,Frq=D)']=dat['TR.RevenueSmartEst/TR.BasicWeightedAvgShares(Period=LTM,Frq=D)'].astype(float, copy=False, errors='ignore')
            dat['TR.EpsSmartEst']=dat['TR.EpsSmartEst'].astype(float, copy=False, errors='ignore')
            #print(len(dat.index))
            #print(dat)
            #print(dat.dtypes)
            #print(spd.iloc[5:10,2:3])
            dat.set_index('TR.PriceClose.date')
            sp.set_index('TR.FwdPtoEPSSmartEst.date')
            r1.set_index('TR.PriceClose.date')
            datname = nst[dat["instrument"][0]]
            datname = 'Unkown' if type(datname) != str else datname
            secn= sectr[dat["instrument"][0]]
            secn = 'Unkown' if type(secn) != str else secn
            mktn=mktcp[dat["instrument"][0]]
            mktn = 'Unkown' if type(mktn) != str else mktn

            plt =sub.make_subplots(rows=4,cols=1)
            dfts=dict(line_width=2.75,line_shape='linear')
            rf=r1[r1['TR.PriceClose.date'].isin(dat['TR.PriceClose.date'])]
            #print(rf)
            #print(spd.iloc[:,1:2])
            plt.add_trace(grap.Scatter(
                x=rm_nan(rf.iloc[:,1]),y=rm_nan(rf.iloc[:,2]/(1*rf.iloc[0,2])).ewm(alpha=0.5).mean(),
                name=f'Price {nst[r1["instrument"][0]]}',
                line_color=b,
                legendrank=2,
                legendgroup='l1',**dfts),row=1,col=1)

            #print(dat)
            plt.add_trace(grap.Scatter(
                x=rm_nan(dat.iloc[:, 1]), y=rm_nan(dat.iloc[:, 2] / (1 * dat.iloc[0, 2])).ewm(alpha=0.5).mean(),
                name=f'Price {datname}',
                line_color=g,
                legendrank=1,
                legendgroup='l1',**dfts), row=1, col=1)
            plt.update_yaxes(type="log",row=1,col=1)
            #print(dat.dtypes)
            #print(((dat.iloc[:,2]/dat.iloc[:,8])/sp.iloc[:,2]))
            dc=dat[dat['TR.PriceClose.date'].isin(sp['TR.FwdPtoEPSSmartEst.date'])]
            dc.index = dc['TR.PriceClose.date']
                #pd.RangeIndex(len(dc.index))
            #print(dc)
            spn=sp[sp['TR.FwdPtoEPSSmartEst.date'].isin(dat['TR.PriceClose.date'])]
            #print(sp)
            spn.index = spn['TR.FwdPtoEPSSmartEst.date']
            #pd.RangeIndex(len(spn.index))
            #print(spn)
            #print(((dc['TR.PriceClose']/dc['TR.EpsSmartEst'])/spn['TR.FwdPtoEPSSmartEst']))
            #print(((dc.iloc[:,2]/dc.iloc[:,8])/spn.iloc[:,2]).ewm(alpha=0.01).mean())
            plt.add_trace(grap.Scatter(x=rm_nan(dc.iloc[:,7]),
            y=rm_nan(((dc['TR.PriceClose']/dc['TR.EpsSmartEst'])/spn['TR.FwdPtoEPSSmartEst'])).ewm(alpha=0.15).mean(),
                                       name=f'({datname} P/E)/(P/E S&P)',
                                       line_color=g,
                                       legendrank=3,
                                       legendgroup='l2',**dfts),row=2, col=1)
            #.ewm(alpha=0.2).mean()
            plt.add_trace(grap.Scatter(x=rm_nan(dc.iloc[:, 7]), y=rm_nan((dc.iloc[:, 2] / dc.iloc[:, 8])).ewm(alpha=0.2).mean(),
                                       name=f'P/E {datname}',
                                       line_color=g,
                                       legendrank=4,
                                       legendgroup='l3',**dfts), row=3, col=1)
            plt.add_trace(grap.Scatter(x=rm_nan(spn.iloc[:, 1]), y=rm_nan(spn.iloc[:, 2]).ewm(alpha=0.2).mean(),
                                       name=f'P/E {nst[sp["instrument"][0]]}',
                                       line_color=b,
                                       legendrank=5,
                                       legendgroup='l3',**dfts), row=3, col=1)
            plt.update_yaxes(type="log", row=3, col=1)
            #plt.update_coloraxes()
            plt.add_trace(grap.Scatter(x=rm_nan(dat.iloc[:, 3]), y=rm_nan(dat.iloc[:, 4]),
                                       name=f'FCFPS {datname}',
                                       line_color=b,
                                       legendrank=8,
                                       legendgroup='l4',**dfts),row=4, col=1)
            plt.add_trace(grap.Scatter(x=rm_nan(dat.iloc[:, 5]), y=rm_nan(dat.iloc[:, 6]),
                                       name=f'Total Revenue PS (TRPS) {datname}',
                                       line_color=g,
                                       legendrank=6,
                                       legendgroup='l4',**dfts),row=4, col=1)
            plt.add_trace(grap.Scatter(x=rm_nan(dat.iloc[:, 7]), y=rm_nan(dat.iloc[:, 8]),
                                       name=f'EPS {datname}',
                                       line_color='Purple',
                                       legendrank=7,
                                       legendgroup='l4',**dfts),row=4, col=1)
            #plt.update_yaxes(type="log", row=4, col=1)
            plt.update_yaxes(showline=True,linewidth=1,gridcolor='rgb(190,190,190)')
            plt.update_xaxes(showline=True, linewidth=1, gridcolor='rgb(190,190,190)')
            #dtick='Y<n>'
            #dtick=365*86400000
            #tick0=dat.iloc[0,1]
            plt.update_xaxes(tickmode='linear',tickformat = '%Y',dtick='M12')
            #plt.update_traces(legendgrouptitle='Testing Legend group', selector=dict(legendgroup='l1'))
            #plt.update_xaxes(tickformatstops=[dict(dtickrange=["M12", None], value="%Y")])
            #plt.update_layout(legend=dict(orientation='h'))
            lix=dict(nticks=6,tickmode='auto')
            lox=dict(nticks=6,tickmode='auto')
            plt.update_layout(
                height=950,
                width=1400,
                title_text=f'<b>Performance Analysis {univ[0]}</b>',
                #title_size=18,
                title_x=.39,
                yaxis1=lox,
                yaxis2=lix,
                yaxis3=lox,
                yaxis4=lix,
                title_xanchor='center',
                #xaxis1_title='Priced Standardized',
                yaxis1_title='Growth Multiple',
                #xaxis2_title='P/E relative to Market (S&P)',
                yaxis2_title='Multiple',
                #xaxis3_title='P/E',
                #yaxis3_title='Multiple',
                #xaxis4_title='Cash Values Per Share',
                #yaxis4_title='Multiple',
                legend_tracegroupgap=177,
                #yaxis1_range=[50, 90],
            )
            ftd=dict(size=16,family='Sans-Serif')
            plt.add_annotation(text='<b>Price Standardized</b>',
                               xref="paper", yref="paper",
                               x=.5, y=1.035, font=ftd, showarrow=False)
            plt.add_annotation(text='<b>P/E relative to Market (S&P)</b>',
                               xref="paper", yref="paper",
                               x=.5, y=.765, font=ftd, showarrow=False)
            plt.add_annotation(text='<b>P/E</b>',
                               xref="paper", yref="paper",
                               x=.5, y=.48, font=ftd, showarrow=False)
            plt.add_annotation(text='<b>Cash Values Per Share</b>',
                               xref="paper", yref="paper",
                               x=.5, y=.19, font=ftd, showarrow=False)
            plt.add_annotation(text=f'<b>Sector: {secn}</b>',
                               xref="paper", yref="paper",
                               x=1, y=1.07, font=ftd, showarrow=False)
            plt.add_annotation(text=f'<b>Market cap: {mktn}</b>',
                               xref="paper", yref="paper",
                               x=1, y=1.04, font=ftd, showarrow=False)
            #plt.show()
            plt.write_image(fdir+str(ps)+'.png')
        except:
            print(f'Something went wrong while trying to find {univ}, skipping.')
            import traceback as tb
            print(tb.format_exc())
    print(f'Finished: {ndr}')
    return create_task(paginate_htmlfiles(ndr))


async def paginate_htmlfiles(drn):
    loop=asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None, lambda : paginate_imgs(drn))
    return result


def paginate_imgs(drn):
    try:
        dn=crd.CURDR+drn+'/'
        #from xhtml2pdf import pisa
        hfs=os.listdir(dn)
        #print([dn+h for h in hfs])
        imgs = []
        import img2pdf
        for fname in hfs:
            if not fname.endswith(".png"):
                continue
            path = os.path.join(dn, fname)
            if os.path.isdir(path):
                continue
            imgs.append(path)
        #print(imgs)
        with open(dn+drn+".pdf", "w+b") as f:
            f.write(img2pdf.convert(imgs))
        for i in hfs:
            try:
                os.remove(dn+i)
            except:
                continue
    except:
        import traceback as tb
        print(tb.format_exc())

    #close_session()

async def get_ricnames(rcs:list,sd,ed):
    nms=['IWF','.SPX']
    r1000=['TR.PriceClose.date','TR.PriceClose']
    i=['TR.FwdPtoEPSSmartEst.date','TR.FwdPtoEPSSmartEst']
    r1s=create_task(_get_data(['IWF'],r1000,{'SDate':sd.isoformat(),'EDate':ed.isoformat()}))
    spx = create_task(_get_data(['.SPX'], i, {'SDate': sd.isoformat(), 'EDate': ed.isoformat(),'Period':'NTM'}))
    nms.extend(rcs)
    nl=['TR.CommonName','TR.CompanyMarketCap(ShType=DEF)','TR.TRBCEconomicSector']
    sn=create_task(_get_data(nms,nl,{'Curn':'USD'}))
    r1,univ=await r1s
    r1 = r1.data.df
    r1.columns = [r1.columns[0], *r1000]
    r1=r1.apply(lambda *args,**kwargs:pd.to_numeric(*args,**(kwargs|{'errors':'ignore'})))
    sp,univ=await spx
    sp=sp.data.df
    sp.columns = [sp.columns[0], *i]
    sp=sp.apply(lambda *args,**kwargs:pd.to_numeric(*args,**(kwargs|{'errors':'ignore'})))
    nm,univ=await sn
    nm = nm.data.df
    nm.columns = [nm.columns[0], *nl]
    # print(r1.dtypes)
    # print(sp.dtypes)
    # print(nm.dtypes)
    #print(len(r1.index))
    #print(len(sp.index))
    return r1,sp,nm
    #async for i in yield_data([DataPackage()])

async def test_plots():
    wt = await export_plots(crd.smd.replace('\r','').split('\n'),'Domestic Small Growth Charts')
    wt1 = await export_plots(crd.lgd.replace('\r', '').split('\n'), 'Domestic Large Growth Charts')
    wt2 = await export_plots(crd.lgf.replace('\r', '').split('\n'), 'Foreign Large Growth Charts')
    wt3 = await export_plots(crd.smfg.replace('\r', '').split('\n'), 'Foreign SMID Growth Charts')
    await asyncio.wait([wt,wt1,wt2,wt3],return_when=asyncio.ALL_COMPLETED)
    print('done')


if __name__=='__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    rClient()
    try:
        loop.run_until_complete(test_plots())
        # 'https://www.sec.gov/Archives/edgar/data/315066/0000315066-20-001924.txt'
    finally:
        loop.close()