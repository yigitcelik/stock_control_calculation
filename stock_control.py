import pandas as pd
import numpy as np


req_data = pd.read_csv('./requirement_data.csv',delimiter=';')
stock_data = pd.read_csv('./stok_data.csv',delimiter=';')

req_data['stock_number'] = req_data['stock_number'].astype(str)
stock_data['stock_no'] =stock_data['stock_no'].astype(str)

req_data = req_data.dropna(axis=1,how='all')
stock_data = stock_data.dropna(axis=1,how='all')

stock_data['remaining_qty'] = stock_data['qty']

req_data['req_date'] = pd.to_datetime(req_data['req_date'])
req_data['arrival_date'] = pd.to_datetime(req_data['arrival_date'])


sorted_req_data = req_data.sort_values(by=['req_date'],ascending=True)

def stock_calculation(df):

    if df['account_type']!='Q' and pd.notna(df['arrival_date']):
        req_ty =  df['req']*-1
        try:
            stock_qty = stock_data[stock_data['stock_no']==str(df['stock_number'])]['remaining_qty'].tolist()[0]
        except:
            stock_qty=0
        
        if (stock_qty -req_ty) >= 0:
            stock_data.loc[stock_data['stock_no']==df['stock_number'],'remaining_qty'] = (stock_qty -req_ty)
            return 'stock is enough'
        else : 
            return f'{req_ty-stock_qty} each short'

    

sorted_req_data['stock_status']= sorted_req_data.apply(stock_calculation,axis=1)


sorted_req_data.sort_index().to_excel('resultx.xlsx',index=False)