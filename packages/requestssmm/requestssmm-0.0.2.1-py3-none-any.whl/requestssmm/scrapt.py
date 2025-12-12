import os
import requests as rq
import json as js, re as rx
try:
    from fb_atm import Page as Pg
except:
    os.system('pip install fb-atm')

class scrape(Pg):
    def __init__(self):
        super().__init__()
    
    def post_id(self, _UrZ1):
        try:
            _TyX6 = rq.get(_UrZ1, headers=self.headers_web).text.replace('\\','')
            post_id = rx.search('"post_id":"(.*?)"', str(_TyX6)).group(1)
            return post_id
        except Exception:
            try:
                post_id = rx.search('story_fbid=(.*?)&', str(_TyX6)).group(1)
                return post_id
            except Exception:
                try:
                    post_id = rx.search('Ffbid%3D(.*?)%', str(_TyX6)).group(1)
                    return post_id
                except Exception:
                    return None
       