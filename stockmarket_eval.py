import cx_Oracle as cx
from datetime import datetime,timedelta
import yfinance as yf
import pandas as pd
import requests
datetime.strftime(datetime.now(),'%Y-%m-%d')
def exec_sql(sql,par=None,k=None):
    con=cx.connect(user='user',password='pass',dsn='DESKTOP-HMNS:1521/XE') #give db details
    cur=con.cursor()

    try:
        if par and k is None:
            cur.executemany(sql,par)
            con.commit()
            return 1
        if k==2:
            o=cur.execute(sql,par)
            return o.fetchone()
        if k==3 and par is not None:
            return cur.callproc(sql,par)
        elif k==3 and par is None:
            return cur.callproc(sql)
        else:
            x=cur.execute(sql)
            
            return pd.DataFrame(data=x,columns=[i[0] for i in cur.description])
    except Exception as e:
        print(f"there is this error{e}")
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
def tick(t):
    x=yf.Ticker(f'{t}.NS')
    return float(x.history(period='1d').reset_index()['Close'].iloc[0])
def find_stock(stock,ex):
   if ex=='BSE':
        try:
            url=f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey=giveurown_apikey&outputsize=full' ##give api key
            r=requests.get(url)
            data=r.json()
            print(stock,float(data['Time Series (Daily)'][next(iter(data['Time Series (Daily)']))]['4. close']))
            return float(data['Time Series (Daily)'][next(iter(data['Time Series (Daily)']))]['4. close'])
        except Exception as e:
            print(e)
            return 0

   else:
       return tick(stock)

stock=exec_sql('select * from stock_code')
x=exec_sql('SELECT COUNT(*) FROM CURR_STOCKVAL WHERE CURRDATE=:1',(datetime.strftime(datetime.now(),'%d-%b-%Y'),),2)
print(x)
if x[0]>0:
    pass
else:
    exec_sql('truncate table curr_stockval',1)
    stock['curr_val']=stock.apply(lambda row:find_stock(row['CODE'],row['STOCK_EX']),axis=1)
    exec_sql('insert into curr_stockval values(:1,:2,null)',list(stock[['STOCK','curr_val']].itertuples(index=False,name=None)))
    exec_sql('update curr_stockval set CURRDATE=:1',[(datetime.strftime(datetime.now(),'%d-%b-%Y'),)])
exec_sql(sql='up_stock',k=3)

exec_sql('proc_insert_into_pl', [int(datetime.strftime(datetime.now(),'%Y%m%d'))],3)




