from imaplib import Time2Internaldate
import requests
import json
from timeit import default_timer
import sqlalchemy
#import odo
import pandas as pd
import time
#import profilehooks
#TODO hacer el test de insert con odo para chequear performance
import numpy as np
import readCfg
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, types
import datetime


 
def get_item_list(url, offset, offset_max, search_attributes):
    """
    Método q devuelve un df con la lista de items
    """

    try:

        df_items = pd.DataFrame()
        url_r = url + search_attributes
        response = requests.get(url_r).json()
        

        #armo un df con todos los id's de resultados
        df_items = pd.json_normalize(response, record_path =['results'])
        #TODO El offset máximo debería ser num_items - offset, pero la api no anda luego de un offset > 900
       

        #TODO ver por que con offset = 350 y 400 trae 49 reg. y no 50
        while int(offset) < int(offset_max):
            url_r = url + '&offset=' + str(offset) + search_attributes
            response = requests.get(url_r).json()
            df_items_aux = pd.json_normalize(response, record_path =['results'])
            df_items = pd.concat([df_items, df_items_aux], axis=0)
            offset += 50

    except KeyError as e:
        print(f"No se puede normalizar el json, verificar response: {json.dumps(response, indent=4)}")
        print("Se termina la ejecución")
        exit()
    
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('Error queriendo conectar con la API, verificar según el error:')
        raise SystemExit(e)

    return df_items


def chunks(lst, n):
    """
    Produce trozos sucesivos de tamaño n de la lista
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def df_to_list_chunk(df_items, chunk):
    """
    Arma una lista con todos los id's de resultados en base a un df
    """
    col_one_list = df_items['id'].tolist()  
    #item_list = ",".join(map(str, col_one_list))
    list_chunk = list(chunks(col_one_list, chunk))

    return list_chunk
    


def get_item_details(url_details, url_dolar, list_items, attributes):
    """
    Devuelve un df con los detalles de los items
    """

    try:    
        #Traigo el tipo de cambio en USD
        response_usd = requests.get(url_dolar).json()

        #Armo un df con la estructura q va a tener la tabla
        df = pd.DataFrame(columns=['id', 'seller_id', 'warranty', 'price', 'sold_quantity', 'usd_price', 'logistic_type', 'condition'])
            
        for item_list in list_items:
            item_csv = ",".join(map(str, item_list))
            url = url_details + item_csv + attributes
            response = requests.get(url).json()
            
            for i in response:
                df1 = pd.DataFrame({"id":[i['body']['id']], 
                                    'seller_id':[i['body']['seller_id']],
                                    'warranty':[i['body']['warranty']],
                                    'price':[i['body']['price']],
                                    'sold_quantity':[i['body']['sold_quantity']],
                                    'usd_price':[i['body']['price'] * response_usd['ratio']],
                                    'logistic_type':[i['body']['shipping']['logistic_type']],
                                    'condition':[i['body']['condition']],
                                                                       
                                    })
                df = df.append(df1, ignore_index = True)            
        return df
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('Error queriendo conectar con la API, verificar según el error:')
        raise SystemExit(e)   

def get_datetime():
    '''
    Devuelve la fecha en formato YYYYMMDD
    '''
    now = datetime.date.today()
    return now.strftime('%Y%m%d')


def date_processed(my_conn, dateproc):
    '''
    Verifica si el proceso fue ejecutado el día de la fecha
    '''
  
    q = "SELECT execution_id FROM executions WHERE dateproc = " + dateproc
    reg_count = my_conn.execute(q)    
    return reg_count.rowcount != 0


def main():
    
    try:
        #Leo el ini
        conf = readCfg.Config()
        
        my_conn = create_engine("mysql+mysqlconnector://root:admin@localhost/meli")        

        date_time = get_datetime()
        begin_time_app = default_timer()
        if date_processed(my_conn, date_time):
            raise SystemExit('Ya fue ejecutado el proceso en la fecha: ' + date_time)


        #armo el df con los items id
        begin_time = default_timer()
        df_item_list  = get_item_list(conf.url_search, int(conf.offset), int(conf.offset_max), conf.search_attributes)
        end_time = default_timer()
        item_list_time = (end_time - begin_time)

        #armo una lista con listas de 20 elementos max (la API no soporta más)    
        list_items = df_to_list_chunk(df_item_list, int(conf.chunk))


        #armo un df con los items y sus detalles
        begin_time = default_timer()
        df_item_details  = get_item_details(conf.url_item, conf.url_dolar, list_items, conf.item_attributes)
        end_time = default_timer()
        item_details_time = (end_time - begin_time)

    
        exec_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = my_conn.execute("INSERT INTO executions (exec_time_items, exec_time_details, dateproc, exec_timestamp) VALUES (" + 
                                 str(item_list_time) + ", "+ str(item_details_time) + ", "+ date_time + ", '"+ exec_timestamp +"')")
        #cambio la cantidad insertada por si varía el df en el insert
        #result = my_conn.execute("INSERT INTO executions (inserted, exec_time_items, exec_time_details, dateproc, exec_timestamp) VALUES (" + 
         #                       str(len(df_item_details)) +", " + str(item_list_time) + ", "+ str(item_details_time) + ", "+ date_time + ", '"+ exec_timestamp +"')")
       
        #Agrego la columna con el execution id
        df_item_details['execution_id'] = result.lastrowid

        #TODO revisar el casteo por tipo de datos
        #dtyp = {c:types.VARCHAR(df_item_details[c].str.len().max()) for c in df_item_details.columns[df_item_details.dtypes == 'object'].tolist()}
        begin_time = default_timer()
        inserted = df_item_details.to_sql('items', con=my_conn, if_exists='append', index=False)#, dtype=dtyp)
        end_time = default_timer()
        insert_time = (end_time - begin_time)

        end_time_app = default_timer()        
        total_time = (end_time_app - begin_time_app)

        my_conn.execute("UPDATE executions SET inserted= " + str(inserted) + 
                        ", total_time= " + str(total_time) + 
                        ", insert_time= " + str(insert_time) + 
                        " WHERE execution_id = "  + str(result.lastrowid) )
        
        

        #TODO implementar trans.rollback()
    except SQLAlchemyError as e:
        error=str(e.__dict__['orig'])
        print(error)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print('Inicio de la prueba')
    main()
  