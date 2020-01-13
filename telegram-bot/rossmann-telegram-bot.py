import pandas as pd
import json
import requests

# constants
DATA_PATH='/Users/meigarom/repos/DataScience_Em_Producao/'

def load_data( store_number ):
    # loading test dataset
    df10 = pd.read_csv( DATA_PATH + 'data/test.csv' )
    df_store_raw = pd.read_csv( DATA_PATH + '/data/store.csv' )

    # merge test dataset + store
    df_test = pd.merge( df10, df_store_raw, how='left', on='Store' )

    # choose store for prediction
    df_test = df_test[df_test['Store'] == store_number] 

    # remove closed days
    df_test = df_test[df_test['Open'] != 0]
    df_test = df_test[~df_test['Open'].isnull()]
    df_test = df_test.drop( 'Id', axis=1 )

    # convert Dataframe to json
    return json.dumps( df_test.to_dict( orient='records' ) )


def prediction( store_number ):
    # API Call
    url = 'https://rossmann-model-test.herokuapp.com/rossmann/predict'
    header = {'Content-type': 'application/json' }
    data = load_data( store_number )

    r = requests.post( url, data=data, headers=header )
    print( 'Status Code {}'.format( r.status_code ) )

    # results
    return pd.DataFrame( r.json(), columns=r.json()[0].keys() )



#    d2 = d1[['store', 'prediction']].groupby( 'store' ).sum().reset_index()
#
#    for i in range( len( d2 ) ):
#        print('Store Number {} will sell R${:,.2f} in the next 6 weeks'.format(
#                d2.loc[i, 'store'],
#                d2.loc[i, 'prediction'] ) )
