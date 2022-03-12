# This is a sample Python script.
#import refinitiv.data.content.fundamental_and_reference as fr
#import refinitiv.data as rd
from pydatastream import Datastream
#from refinitiv.data import session
import refinitiv.dataplatform as rdp
from refinitiv.dataplatform.content.data_grid._fundamental_class import Fundamental

import asyncpg



def test():
    #fr.Definition()
    res=fr.Definition(['AAPL.O'],['TR.PriceClose']).get_data()
    print(res.data.raw)


if __name__ == '__main__':
    #DS=Datastream('acolyer@ithakagroup.com','Scamper1')
    #data = DS.get_price('@AAPL', date_from='2008', date_to='2009')
    #print(data)
    #ses=session.platform.Definition(app_key='ae5449cf0ad64db19cb8ac60f2ee7e4902d5fefa',grant=session.platform.GrantPassword(username='cmarks@ithakagroup.com',password='charith22?')).get_session()
    #ses.open()
    #print(ses)
    #session.set_default(ses)
    # rd.open_session(app_key='27d499a6497b4850a21a9f159b4f592367df809f')
    # df = rd.get_data(
    #     universe=['IBM.N', 'VOD.L'],
    #     fields=['TR.Revenue']
    # )
    # print(df)
    #res=rd.get_data(['AAPL.O'],['TR.CompanyName'])
    #print(res)
    #rd.open_session()
    #sess.desktop.Definition(app_key='ae5449cf0ad64db19cb8ac60f2ee7e4902d5fefa').get_session()
    #ses= rd.open_session(app_key='ae5449cf0ad64db19cb8ac60f2ee7e4902d5fefa',name='platform')
    #rdp.open_desktop_session('ae5449cf0ad64db19cb8ac60f2ee7e4902d5fefa')
    rdp.open_platform_session(
        '2a2f8e4443b44860be25d4cfc607b1654e4dfc74',
        rdp.GrantPassword(
            'acolyer@ithakagroup.com',
            'Scamper1'
        )
    )
    rdp.get_data()
    fd = Fundamental()
    dt=fd.get_data(['AMD.O',"IBM", "GOOG.O", "MSFT.O"], ["TR.PriceClose", "TR.Volume", "TR.PriceLow"])
    print(dt.data.df)
    #print(dt)
    pp=rdp.get_historical_price_summaries(
        universe='AMD.O',
        interval=rdp.Intervals.DAILY,
        fields=['BID', 'ASK', 'OPEN_PRC', 'HIGH_1', 'LOW_1', 'TRDPRC_1', 'NUM_MOVES', 'TRNOVR_UNS']
    )
    print(pp)
    rdp.close_session()
    #test()
    #print(ses)
    #rd.close_session()
    # sess = dt.open_session()
    # dt.get_data()
    # sess.
    # sess.http_request_async()
    # dt.open_session()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
