

"""
This is a python smm panel libary create by mahdi hasan shuvo
you can use this library to create a simple smm panel
you can add user, add post, add comment, 

"""
##------------------------------------#
__DEVOLPER__ = '___MAHDI HASAN SHUVO___'
__FACEBOOK__ =' https://www.facebook.com/bk4human'
__GitHub__ =  'MAHDI-HASAN-shuvo'
___V___= 1
__WHATSAPP___=8801616397082
#-----------------------------------------------------------#

import os

try:
    import requests
    from fb_atm import Page 
except:
    os.system('pip install fb-atm requests')
try:
    from api import API
    from scrapt import scrape
    from utlites import Botgp
except :
    from .api import API
    from .scrapt import scrape
    from .utlites import Botgp