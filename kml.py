# -*- coding: utf-8 -*-
"""
Created on Tue Jan  13 16:26:21 2021

@author: Breno
"""

from pykml import parser
from pandas import DataFrame
from datetime import datetime

class Kml:    
    
    cols = ["ID","CD_GEOCODIGO","TIPO",
            "CD_GEOCODBA","NM_BAIRRO","CD_GEOCODSD",
            "NM_SUBDISTRITO","CD_GEOCODDS","NM_DISTRITO",
            "CD_GEOCODMU","NM_MUNICIPIO","NM_MICRO",
            "NM_MESO","NM_UF","CD_NIVEL","CD_CATEGORIA",
            "NM_CATEGORIA","NM_LOCALIDADE","LONG","LAT","ALT"]
    
    def __init__(self, path):
        
        self.path = path
        self.doc = None
        self.df = DataFrame(columns=self.cols)

    def converter(self):        
        
        with open(self.path, 'rt', encoding='utf-8') as myfile:
    
            self.doc = parser.parse(myfile).getroot()    
      
        registros = self.doc.findall('.//{http://www.opengis.net/kml/2.2}Placemark')
        
        for i in registros:            
            
            carac = i.getchildren()[2]  
            
            d_carac = [i.pyval for i in carac.SchemaData.getchildren()]        
            
            dcti = dict(zip(self.cols,d_carac))
        
            self.df = self.df.append(dcti, ignore_index=True)

    def gravar(self):
        
        destino = self.path
        
        agora = datetime.now()
        
        data = '_'.join([str(agora.day),
                         str(agora.month),
                         str(agora.year)])
        
        arquivo = '_'.join(['kml', data]) + '.csv'
        
        self.df.to_csv('\\'.join(destino.split('\\')[:5]+[arquivo]),
                       sep=';',
                       decimal=',',
                       encoding='latin1',
                       index=False) 

teste = Kml("Atalho para o arquivo 'BR_Localidades_2010_v1.kml'")

teste.converter()

teste.gravar()

