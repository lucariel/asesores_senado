#!/usr/bin/env python
# coding: utf-8

# In[1]:


#personal de cada senador 


import requests  
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd  
import numpy as np
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from genderize import Genderize
import re


# In[2]:


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1044x788")


prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2, 
                                'plugins': 2, 'popups': 2, 'geolocation': 2, 
                                'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                                'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                                'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                                'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                                'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                                'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                                'durable_storage': 2}}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")


# In[52]:


driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.senado.gov.ar/senadores/listados/listaSenadoRes")

r = driver.execute_script("return document.documentElement.outerHTML")
#driver.quit()

soup = bs(r) 
results = soup.find('table', attrs={'id':'senadoresTabla'})


# In[53]:


lg_data={}
for h in range(1,len(bs(str(results)).findAll('tr'))):
    s1 = bs(str(results)).findAll('tr')[h]
    links = [a['href'] for a in s1.select('a[href]')]


    web="https://www.senado.gov.ar"
    s_link= str(web+str(links[0]))
    #print(s_link)

    driver_s = webdriver.Chrome(options=chrome_options)
    driver.get(s_link)
    r_s = driver.execute_script("return document.documentElement.outerHTML")


    driver_s.quit()
    soup_s=bs(r_s)

    agent_table = soup_s.find('table', attrs={'summary':"Listado de Agentes."})
    nombre_de_asesores = []
    l = bs(str(agent_table)).findAll('td')

    for i in range(0,len(l),2):
        n = bs(str(agent_table)).findAll('td')[i].get_text()
        p = n.split('\n')[0]
        nombre_de_asesores.append(p)
    senadores = bs(str(results)).findAll('tr')
    nombre = bs(str(senadores[h])).findAll('td')[1].get_text()
    nombre = nombre.replace('\n', '').replace('\t','').strip()

    pcia =  bs(str(senadores[h])).findAll('td')[2].get_text()
    partido =  bs(str(senadores[h])).findAll('td')[3].get_text()
    legislador_data = {}
    legislador_data['nombre']=nombre
    legislador_data['pcia'] = pcia
    legislador_data['partido'] = partido
    legislador_data['nombre_asesor'] = nombre_de_asesores
    lg_data[str(nombre)]=legislador_data
    print(lg_data)
    
    


# In[54]:


df = pd.DataFrame(lg_data).transpose()
df['asesores_masculinos'] = 0
df['asesores_femeninos'] = 0


# In[55]:


for f in range(len(df.nombre_asesor)):
    asesor = [x.split(' ')[0] for x in df.nombre_asesor[f]]
    genders = Genderize().get(asesor)
    h = 0
    m = 0
    for j in range(len(genders)):
        if genders[j]['gender']=='female':
            m+=1
        elif genders[j]['gender']=='male':
            h+=1
    df.asesores_masculinos[f] = h
    df.asesores_femeninos[f] = m
    


# In[56]:


df.to_csv("datos_legisladores.csv")


# In[ ]:




