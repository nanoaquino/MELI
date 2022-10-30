import configparser
import os


class Config:
    '''
    Clase para leer la configuración
    '''
    def __init__(self):
        try:
            config_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'best_seller.ini'))
            if not os.path.exists(config_file):
                raise SystemExit('No existe el archivo best_seller.ini')

            config = configparser.ConfigParser()
            config.read(config_file)
            #URLs
            self.url_search = config['URLS']['url_search']
            self.url_item = config['URLS']['url_item']
            self.url_dolar = config['URLS']['url_dolar']
            #ATTRs
            self.item_attributes = config['ATTR']['item_attributes']
            self.search_attributes = config['ATTR']['search_attributes']
            
            self.chunk = config['ATTR']['chunk']
            self.offset_max = config['ATTR']['offset_max']
            self.offset = config['ATTR']['offset']
        
            #BD
            self.host = config['BD']['host']
            self.user = config['BD']['user']
            self.password = config['BD']['password']
            self.db = config['BD']['db']

        except KeyError as e:
            raise SystemExit(f'No existe el key: {e}') 
        except configparser.Error as e:
            print(f'Error con el archivo de configuración: {e}')
            raise SystemExit(e.message) 