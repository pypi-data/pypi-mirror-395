from mahdix import *
from re import search
from json import loads,dumps
from requests import get, post,Session
import secrets
import string
import random
from ..utlites import Cookees,__formate_coki__
x=Cookees()
def random_hex(length=64):
    return secrets.token_hex(length // 2)

def random_alphanumeric(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_digits(length=6):
    return ''.join(random.choices(string.digits, k=length))

headers_instagrams = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'dnt': '1',
    'dpr': '1',
    'priority': 'u=0, i',
    'sec-ch-prefers-color-scheme': 'dark',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-full-version-list': '"Chromium";v="142.0.7444.176", "Google Chrome";v="142.0.7444.176", "Not_A Brand";v="99.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"19.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'viewport-width': '1812',
}
def Getfollower_count(url:str)->int:
    try:
        """
        Get follower count from url
        """
        headers_instagram =headers_instagrams.copy()
        get_datya=requests.get('https://www.instagram.com/hasan__ekram', headers=headers_instagram).text
        profile_id = re.search(r'"profile_id":"(\d+)"', get_datya).group(1)
        data = {
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'PolarisProfilePageContentQuery',
            'server_timestamps': 'True',
            'variables': json.dumps({"enable_integrity_filters":True,"id":profile_id,"render_surface":"PROFILE","__relay_internal__pv__PolarisProjectCannesEnabledrelayprovider":True,"__relay_internal__pv__PolarisProjectCannesLoggedInEnabledrelayprovider":True,"__relay_internal__pv__PolarisCannesGuardianExperienceEnabledrelayprovider":True,"__relay_internal__pv__PolarisCASB976ProfileEnabledrelayprovider":False,"__relay_internal__pv__PolarisRepostsConsumptionEnabledrelayprovider":False}),
            'doc_id': '26056258483976274',
        }
        headers_instagram.update({ 
            'x-asbd-id': random_digits(6),
            'x-bloks-version-id': random_hex(64),
            'x-csrftoken': random_alphanumeric(32),
            'x-fb-friendly-name': 'PolarisProfilePageContentQuery',
            'x-fb-lsd': random_alphanumeric(16),
            'x-ig-app-id': random_digits(15)
        }

            )
        response = requests.post('https://www.instagram.com/graphql/query',  headers=headers_instagram, data=data).json()
        return int(response['data']['user']['follower_count'])

    except:
        return 0
def instara_follow(url,cookesr):
    
    try:
        headers_instagram=headers_instagrams.copy()
        session = Session()
        cookies = __formate_coki__(str(cookesr).replace(' ', ''))
        response = session.get(url, headers=headers_instagram,cookies=cookies)
        get_data=x.get_data(response.text)
        if get_data == False:
            return False,"Cookies Invalid"
        target_id = search('"target_id":"(.*?)"', str(response.text)).group(1)
        csrf_token = search('"csrf_token":"(.*?)"', str(response.text)).group(1)
        versioningID = search('"versioningID":"(.*?)"', str(response.text)).group(1)
        app_id = search('"app_id":"(.*?)"', str(response.text)).group(1)
        headers_instagram['x-bloks-version-id'] = versioningID
        headers_instagram['x-csrftoken'] = csrf_token
       
        # open("testc.txt","w" ,encoding="utf-8").write(response.text)
        
        get_data.update({
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'PolarisProfilePageContentQuery',
                'server_timestamps': 'true',
                'variables': dumps({"enable_integrity_filters":True,"id":target_id,"render_surface":"PROFILE","__relay_internal__pv__PolarisProjectCannesEnabledrelayprovider":True,"__relay_internal__pv__PolarisProjectCannesLoggedInEnabledrelayprovider":True,"__relay_internal__pv__PolarisCannesGuardianExperienceEnabledrelayprovider":True,"__relay_internal__pv__PolarisCASB976ProfileEnabledrelayprovider":False,"__relay_internal__pv__PolarisRepostsConsumptionEnabledrelayprovider":False}),
                'doc_id': '25585291164389315',
        })
        response = post('https://www.instagram.com/graphql/query',cookies=cookies, headers=headers_instagram, data=get_data).text
        if '"following":false' in response:
            headers_instagram['x-fb-friendly-name'] = 'usePolarisFollowMutation'
            headers_instagram['x-fb-lsd'] = get_data['lsd']
            headers_instagram['x-ig-app-id'] = app_id
            headers_instagram['x-root-field-name'] = 'xdt_create_friendship'
            get_data.update(({
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'usePolarisFollowMutation',
            'server_timestamps': 'true',
            'variables': dumps({"target_user_id":target_id,"container_module":"profile","nav_chain":"PolarisProfilePostsTabRoot:profilePage:1:via_cold_start"}),
            'doc_id': '9740159112729312',
            }))
            response = post('https://www.instagram.com/graphql/query', cookies=cookies, headers=headers_instagram, data=get_data)
            try:
                if '"following":true' in response.text:
                    return True,get_data['av']
                else:
                    return False,get_data['av']
            except Exception as e:
                return False,"failed to follow"
        elif '"following":true' in response:
            return False,'Already Following'
    except Exception as e:
        return False,"Cookies Invalid"
    


