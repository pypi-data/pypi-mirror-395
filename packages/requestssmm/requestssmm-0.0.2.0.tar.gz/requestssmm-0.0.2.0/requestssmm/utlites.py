from os import name
from requests import get,post,Session
import requests,re
import base64,uuid,json,time
from json import dumps
from mahdix import *
from fb_atm import Page
from random import choice
__formate_coki__ = lambda x: {cookie.split('=', 1)[0].strip(): cookie.split('=', 1)[1].strip() for cookie in x.split(';') if '=' in cookie}
class Botgp:
    def __init__(self):
        pass
    
        
    def share_facebook_post_EAAGN(self,token, id_share,cookie,privacy='0'):
        try:
            """
            Share a post on Facebook using the Facebook Graph API.
            :param token: Facebook access token [EAAGNO...........]
            :param post_url: URL of the post to share
            :param privacy: Privacy setting for the post (default: SELF)
            Returns:
                Grapg api respone
            """
            he = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate',
                'connection': 'keep-alive',
                'content-length': '0',
                'cookie': cookie,
                'host': 'graph.facebook.com'
            }
            response = post(f'https://graph.facebook.com/me/feed?link=https://m.facebook.com/{id_share}&published={privacy}&access_token={token}', headers=he).json()
            if 'id' in response:
                return (True,response)
            else:
                return (False,"failed")
        except Exception as e:
            return (False,e)
    def comment_post_EAAGN(self,post_id='9000855519965854',message='ma4D1',token=None,cookes=None):
        try:
            """
            Comment on a post on Facebook using the Facebook Graph API.
            :param token: Facebook access token [EAAGNO...........]
            :param post_url: URL of the post to share
            :param privacy: Privacy setting for the post (default: SELF)
            Returns:
            Grapg api respone
            """
            if token and cookes :
                response=post(f"https://graph.facebook.com/{post_id}/comments/?message={message}&access_token={token}", headers = {"cookie":cookes}).json()
                if 'id' in response:
                    return (True,response)
            else:
                return (False,"failed")
        except Exception as e:
            return (False,e)


class EAAAAU(Botgp):
    def __init__(self):
        super().__init__()
        #--> Access Token (EAAU from b-graph login)
        pass
    def share_facebook_post_EAAAAU(self,token, post_url,privacy='SELF'):
        try:
            """
            Share a post on Facebook using the Facebook Graph API.
            :param token: Facebook access token [EAAAAUaZA8...........]
            :param post_url: URL of the post to share
            :param privacy: Privacy setting for the post (default: SELF)
            Returns:
                Grapg api respone
            """
            fb_url = 'https://graph.facebook.com/v13.0/me/feed'
            data = {'link': post_url, 'published': '0', 'privacy': '{"value":"%s"}'%(privacy), 'access_token': token}
            response = post(fb_url, data=data).json()
            if 'id' in response:
                return (True,response)
        except Exception as e:
            return (False,e)
        
    def follow_EAAAAU(self,terge_id=None,Token=None):
        """_summary_
        This a function to follow a user on Facebook using the Facebook Graph API.
         token after loging use graph api
        Args:
            terge_id (_type_, optional): _description_. Defaults to None.
            Token (_type_, optional): _description_. Defaults to None.
             #--> Access Token (EAAU from b-graph login)

        Returns:
            _type_: _description_
        """
        try:
            if terge_id and Token:
                response=post(f'https://graph.facebook.com/{terge_id}/subscribers?access_token={Token}').json()
                return True,response
        except Exception as e:
            return (False,e)
    def pgLike_EAAAAU(self,terge_id=None,Token=None):
        """_summary_
        This a function to page like a user on Facebook using the Facebook Graph API.
         token after loging use graph api
        Args:
            terge_id (_type_, optional): _description_. Defaults to None.
            Token (_type_, optional): _description_. Defaults to None.
             #--> Access Token (EAAU from b-graph login)
        Returns:
            _type_: _description_
        """
        try:
            if terge_id and Token:
                response=post(f'https://graph.facebook.com/{terge_id}/likes?access_token={Token}').json()
                return True,response
        except Exception as e:
            return (False,e)
    def post_reaction_EAAAAU(self,actor_id:str, post_id:str, react:str, token:str):
        r    = Session()
        var  = {"input":{"feedback_referrer":"native_newsfeed","tracking":[None],"feedback_id":str(base64.b64encode(('feedback:{}'.format(post_id)).encode('utf-8')).decode('utf-8')),"client_mutation_id":str(uuid.uuid4()),"nectar_module":"newsfeed_ufi","feedback_source":"native_newsfeed","attribution_id_v2":"NewsFeedFragment,native_newsfeed,cold_start,1710331848.276,264071715,4748854339,,","feedback_reaction_id":react,"actor_id":actor_id,"action_timestamp":str(time.time())[:10]}}
        data = {'access_token':token,'method':'post','pretty':False,'format':'json','server_timestamps':True,'locale':'id_ID','fb_api_req_friendly_name':'ViewerReactionsMutation','fb_api_caller_class':'graphservice','client_doc_id':'2857784093518205785115255697','variables':json.dumps(var),'fb_api_analytics_tags':["GraphServices"],'client_trace_id':str(uuid.uuid4())}
        pos  = r.post('https://graph.facebook.com/graphql', data=data).json()
        try:
            if react in str(pos):
                return(True,pos['data']['feedback_react']['feedback']['reactors']['count'])
               
            else: return(False,'React Failed!')
        except Exception: return(False,'React Failed!')
        
        

class Cookees(Page):
    def __init__(self):
        super().__init__()
        self.headers= {
        'authority': 'mbasic.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8,nl;q=0.7,pt;q=0.6',
        'cache-control': 'max-age=0',
        'dpr': '12',
        'referer': 'https://mbasic.facebook.com/photo/?fbid=778900340946473&set=a.598020855701090',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6262.5", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6262.5"',
        'sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent':W_ueragnt() ,'viewport-width': '673',
        "ysafb":"24"}
    def react_post(self,cok,url, react):
        try:
            react_type = ['Like','Love','Haha','Wow','Care','Sad','Angry'][react-1]
            react      = ['1635855486666999','1678524932434102','115940658764963','478547315650144','613557422527858','908563459236466','444813342392137'][react-1]
            data_responce=requests.get(url,headers=self.headers_web,cookies=self.fromate_cookes(cok)).text
            try: feedback_id = re.search('"feedback":{"associated_group":null,"id":"(.*?)"},"is_story_civic":null',str(data_responce)).group(1)
            except Exception as e: feedback_id = re.search('"feedback":{"id":"(.*?)"',str(data_responce)).group(1)
            session_id = re.search(r'"sessionID":"(.*?)"',str(data_responce)).group(1)
            uidx = re.search(r'__user=(.*?)&', str(data_responce)).group(1)
            fb_dtsg = re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"', str(data_responce)).group(1)
            jazoest = re.search(r'&jazoest=(.*?)",', str(data_responce)).group(1)
            lsd = re.search(r'"LSD",\[\],{"token":"(.*?)"', str(data_responce)).group(1)
            data = {
            'av': uidx,
            'fb_dtsg': fb_dtsg,
            'jazoest': jazoest,
            'lsd': lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
            'variables': '{"input":{"attribution_id_v2":"CometPhotoRoot.react,comet.mediaviewer.photo,unexpected,1727623102922,48437,,,;CometHomeRoot.react,comet.home,via_cold_start,1727623004088,438841,4748854339,12#15#301,8760540677331341","feedback_id":"%s","feedback_reaction_id":"%s","feedback_source":"MEDIA_VIEWER","is_tracking_encrypted":true,"tracking":[""],"session_id":"%s","actor_id":"%s","client_mutation_id":"4"},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}'%(feedback_id,react,session_id,uidx),
            'server_timestamps': 'true',
            'doc_id': '8030707243693006',
        }
            response = requests.post('https://www.facebook.com/api/graphql/', cookies=self.fromate_cookes(cok), headers=self.headers, data=data).text
            if '"data":{"feedback_react":{"feedback":{"id":"' in str(response):
                return True,re.search('"reactors":{"count":(.*?),',str(response)).group(1)
                
            else:
                return False,"account error"

        except  Exception as e:
            return False,str(e)
    def get_data(self,req):
        try:
            av= re.search('"actorID":"(.*?)"', str(req)).group(1)
            __hs= re.search('"haste_session":"(.*?)",', str(req)).group(1)
            __rev= re.search('{"rev":(.*?)}', str(req)).group(1)
            __hsi= re.search('"hsi":"(.*?)",', str(req)).group(1)
            fb_dtsg= re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"', str(req)).group(1)
            jazoest= re.search('&jazoest=(.*?)",', str(req)).group(1)
            lsd= re.search(r'"LSD",\[\],{"token":"(.*?)"', str(req)).group(1)
            __spin_r= re.search('"__spin_r":(.*?),', str(req)).group(1)
            __spin_t= re.search('"__spin_t":(.*?),', str(req)).group(1)
            __comet_req = re.search('__comet_req=(.*?)&', str(req)).group(1)
            _req =  re.search('_req=(.*?)&', str(req)).group(1)
            data = {
                '__s': 'mr42k3:0gsl5n:9smutq',
                'av': av,
                '__aaid': '0',
                '__user': av,
                '__a': '1',
                '__req': _req,
                '__hs':__hs,
                'dpr': '1',
                '__ccg': 'EXCELLENT',
                '__rev': __rev,
                '__hsi': __hsi,
                '__comet_req': __comet_req,
                'fb_dtsg': fb_dtsg,
                'jazoest':jazoest,
                'lsd': lsd,
                '__spin_r': __spin_r,
                '__spin_b': 'trunk',
                '__spin_t':__spin_t,}
            return data
        except Exception as e:
            return False
            

    def story_viwes(self,cookes:str,url:str):
        try:
            cookies =self.fromate_cookes(cookes)
            bucket_id=re.search('.com/stories/(.*?)/',str(url)).group(1)
            story_id =re.search(f'{bucket_id}/(.*?)/',str(url)).group(1)
            req=requests.get(url,cookies=cookies, headers= self.headers).text
            gets_data=self.get_data(req)
            if gets_data:
                data = {
                    '__crn': 'comet.fbweb.CometStoriesSuspenseSingleBucketViewerWithEntryPointRoute',
                    'fb_api_caller_class': 'RelayModern',
                    'fb_api_req_friendly_name': 'storiesUpdateSeenStateMutation',
                    'variables': '{"input":{"bucket_id":"%s","story_id":"%s","actor_id":"%s","client_mutation_id":"1"},"scale":1}'%(bucket_id,story_id,gets_data['av']),
                    'server_timestamps': 'true',
                    'doc_id': '5127393270671537',
                }
                data.update(gets_data)
                response = requests.post('https://www.facebook.com/api/graphql/', cookies=cookies, headers= self.headers, data=data).text
                if '"is_seen_by_viewer":true' in response:
                        return True,gets_data['av']
                else :
                    return False,gets_data['av']
            if not gets_data :
                return False,' Invalid CookiesError'
        except Exception as e:
            return False,str(e)
    def poll_vote(self,text:str,poll_url:str,cookes:str):
        try:
            return_valu=None
            cookies=self.fromate_cookes(cookes)
            response = requests.get(
                poll_url,
                cookies=cookies,
                headers=self.headers,
            ).text
            all_=re.findall(r'{"id":"(\d+)","text":"(.*?)","viewer_has_voted":',str(response))
            gets_data=self.get_data(response)
            if gets_data:
                if all_:
                    POLL_ID = re.search(r'"Question","id":"(\d+)"',str(response)).group(1)
                    for OPTION_ID, name in all_:
                        if text.lower() in str(name).lower():
                            data = {
                            'fb_api_caller_class': 'RelayModern',
                            'fb_api_req_friendly_name': 'useCometPollAddVoteMutation',
                            'variables': '{"input":{"is_tracking_encrypted":true,"option_id":"%s","question_id":"%s","tracking":[""],"actor_id":"%s","client_mutation_id":"2"},"scale":1.5,"__relay_internal__pv__IsWorkUserrelayprovider":false}'%(OPTION_ID,POLL_ID,gets_data['av']),
                            'server_timestamps': 'true',
                        'doc_id': '6681967255191860',}
                            data.update(gets_data)
                            response = requests.post('https://www.facebook.com/api/graphql/', cookies=cookies , headers=self.headers,data=data,allow_redirects=False)
                            if OPTION_ID and gets_data['av'] in response.text:
                                voter_count = re.search(f'"profile_voters":{{"count":(\\d+)}},"id":"{OPTION_ID}"', response.text).group(1)
                                
                                return_valu =True,voter_count
                                                
                        else :
                            return_valu =False,"invalid Text"
                else:
                    return_valu = False, "invalid Poll"
            else:
                    return_valu = False, "Invalid Cookies"

        except Exception as e:
            return_valu = False, str(e)
        return return_valu
    def subtime_comment(self,url,cookie,text):
        try:
            cookies=self.fromate_cookes(cookie)
            req=requests.get(url,headers=self.headers,cookies=cookies).text
            ge_d=self.get_data(req)
            if ge_d:
                    session_id = re.search('"sessionID":"(.*?)"',str(req)).group(1)
                    client_id = re.search('"clientID":"(.*?)"',str(req)).group(1)
                    try: feedback_id = re.search('"feedback":{"associated_group":null,"id":"(.*?)"},"is_story_civic":null',str(req)).group(1)
                    except Exception as e: feedback_id = re.findall('"feedback_id":"(.*?)"',str(req))[-1]
                    try: tracking = re.findall('{"action_link":null,"badge":null,"follow_button":null},"encrypted_tracking":"(.*?)"},"__module_operation_CometFeedStoryTitleSection_story"',str(req))[-1]
                    except Exception as e: tracking = re.findall('"encrypted_tracking":"(.*?)"',str(req))[0]
                    Vir = {"assistant_caller":"comet_above_composer","conversation_guide_session_id":None,"conversation_guide_shown":None}
                    Var = {"feedLocation":"PERMALINK","feedbackSource":2,"groupID":None,"input":{"client_mutation_id":"1","actor_id":ge_d['av'],"attachments":None,"feedback_id":feedback_id,"formatting_style":None,"message":{"ranges":[],"text":text},"attribution_id_v2":"CometSinglePostRoot.react,comet.post.single,via_cold_start,1703691784875,275571,,,","vod_video_timestamp":None,"is_tracking_encrypted":True,"tracking":[tracking,json.dumps(Vir)],"feedback_source":"OBJECT","idempotence_token":"client:%s"%(client_id),"session_id":session_id},"inviteShortLinkKey":None,"renderLocation":None,"scale":1.5,"useDefaultActor":False,"focusCommentID":None}
                    data = {
                    'fb_api_caller_class': 'RelayModern',
                    'fb_api_req_friendly_name': 'useCometUFICreateCommentMutation',
                    'variables': json.dumps(Var),
                    'server_timestamps': 'True',
                    'doc_id': '9389802714420896',
                    }
                    data.update(ge_d)
                    response = requests.post('https://www.facebook.com/api/graphql/', cookies=cookies, headers=self.headers, data=data).text
                    if text in response:
                        return True,data['av']
                    else:
                        return False,data['av']
            else:
                return False,'invalid cookies'
        except Exception as e:
            return False,f'invalid cookies {e}'
                    
    def sub_Member(self,url,cookes):
        try:
            cookes=__formate_coki__(cookes)
            req = requests.get(url, headers=self.headers, cookies=cookes,allow_redirects=True).text
            if '"viewer_forum_join_state":"MEMBER"' in req:
                return False,"Allready MEMBER"
            ge_d=self.get_data(req)
            if ge_d:
                groupID = re.search('"groupID":"(.*?)"',req).group(1)
                self.headers.update({'x-fb-friendly-name': 'GroupCometJoinForumMutation',
                'x-fb-lsd': ge_d['lsd']})
                data = {
                '__crn': 'comet.fbweb.CometGroupDiscussionRoute',
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'GroupCometJoinForumMutation',
                'variables': json.dumps(  {"feedType":"DISCUSSION","groupID":groupID,"input":{"action_source":"GROUP_MALL","attribution_id_v2":"CometGroupDiscussionRoot.react,comet.group,unexpected,1747809244052,700445,2361831622,,","group_id":groupID,"group_share_tracking_params":{"app_id":"2220391788200892","exp_id":"null","is_from_share":False},"actor_id":ge_d['av'],"client_mutation_id":"6"},"inviteShortLinkKey":None,"isChainingRecommendationUnit":False,"scale":1,"source":"GROUP_MALL","renderLocation":"group_mall","__relay_internal__pv__GroupsCometGroupChatLazyLoadLastMessageSnippetrelayprovider":False}),
                'server_timestamps': 'true',
                'doc_id': '29626761770304614',
                }
                data.update(ge_d)
                response = requests.post('https://www.facebook.com/api/graphql/', cookies=cookes, headers=self.headers, data=data).text
                if '"viewer_forum_join_state":"MEMBER"' in response:
                        return True,data['av']
                else: return False,data['av']
            else: return False,'invalid cookies'
        except Exception as e:
            return False,'invalid cookies'
    def page_like(self,url,cookes): 
        try:
            cookes=__formate_coki__(cookes)
            req = requests.get(url, headers=self.headers, cookies=cookes,allow_redirects=True).text
            if '{"text":"Liked"}' in req: 
                #  print( f'{LI_YELLOW} {LI_WHITE}Allready Liked : {LI_GREEN}{cookes["c_user"]}{LI_WHITE}')
                return False,"Allready Liked"
            ge_d=self.get_data(req)
            if ge_d:
                page_id =re.search('"delegate_page_id":"(.*?)"',req).group(1)
                self.headers.update({'x-fb-friendly-name': 'CometProfilePlusLikeMutation',
                'x-fb-lsd': ge_d['lsd']})
                data = {
                '__crn': 'comet.fbweb.CometProfileTimelineListViewRoute',
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'CometProfilePlusLikeMutation',
                'variables': dumps({"input":{"is_tracking_encrypted":False,"page_id":page_id,"source":None,"tracking":None,"actor_id":ge_d['av'],"client_mutation_id":"1"},"scale":1}),
                'server_timestamps': 'true',
                'doc_id': '24452064861060493',
                }
                data.update(ge_d)
                response = requests.post('https://www.facebook.com/api/graphql/', cookies=cookes, headers=self.headers, data=data).text
                if '{"text":"Liked"}' in response:
                    return True,data['av']
                else: return False,data['av']
            else: return False,'invalid cookies'
        except Exception as e:
                return False,'invalid cookies'
    def submite_follow(self,url,cookes):
        try:
        
            cookes=__formate_coki__(cookes)
            req = requests.get(url, headers=self.headers, cookies=cookes).text
            if '{"text":"Following"}' in req: 
                return False,"Allready Following"
            ge_d=self.get_data(req)
            if ge_d:
        
                subscribee_id= re.search('"userID":"(.*?)"',req).group(1)
                self.headers.update({'x-fb-friendly-name': 'CometUserFollowMutation',
                'x-fb-lsd': ge_d['lsd']})
                data = {
                    '__crn': 'comet.fbweb.CometProfileTimelineListViewRoute',
                    'fb_api_caller_class': 'RelayModern',
                    'fb_api_req_friendly_name': 'CometUserFollowMutation',
                    'variables': dumps({"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1747723243188,835444,250100865708545,,","is_tracking_encrypted":False,"subscribe_location":"PROFILE","subscribee_id":subscribee_id,"tracking":None,"actor_id":ge_d['av'],"client_mutation_id":"1"},"scale":1}),
                    'server_timestamps': 'true',
                    'doc_id': '24034012419524524',
                }
                data.update(ge_d)
                response = requests.post('https://www.facebook.com/api/graphql/', cookies=cookes, headers=self.headers, data=data).text
                if '"title":{"text":"Following"}' in response:
                        return True , data['av']
                else:
                    return False, data['av']
            else: return False,'invalid cookies'
        except Exception as e:
                return False , 'invalid cookies'
    def subtime_PG_reviews(self,url,cookie,text):
        try:
                cookies=__formate_coki__(cookie)
                req=requests.get(url,headers=self.headers,cookies=cookies).text
                ge_d=self.get_data(req)
                if ge_d:
                    clientID = re.search('"clientID":"(.*?)"', req).group(1)
                    self.headers.update({'x-fb-friendly-name': 'ComposerStoryCreateMutation',
                'x-fb-lsd': ge_d['lsd']})
                    data = {

                        '__crn': 'comet.fbweb.CometProfileReviewsTabRoute',
                        'fb_api_caller_class': 'RelayModern',
                        'fb_api_req_friendly_name': 'ComposerStoryCreateMutation',
                        'variables': json.dumps({"input":{"composer_entry_point":"inline_composer","composer_source_surface":"page_recommendation_tab","idempotence_token":f"{clientID}_FEED","source":"WWW","audience":{"privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}},"message":{"ranges":[],"text":text},"with_tags_ids":None,"text_format_preset_id":"0","page_recommendation":{"page_id":"104121542118658","rec_type":"POSITIVE"},"logging":{"composer_session_id":clientID},"navigation_data":{"attribution_id_v2":"ProfileCometReviewsTabRoot.react,comet.profile.reviews,via_cold_start,1748001898861,567838,250100865708545,,"},"tracking":[None],"event_share_metadata":{"surface":"newsfeed"},"actor_id":ge_d['av'],"client_mutation_id":"1"},"feedLocation":"PAGE_SURFACE_RECOMMENDATIONS","feedbackSource":0,"focusCommentID":None,"gridMediaWidth":None,"groupID":None,"scale":1,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":False,"renderLocation":"timeline","useDefaultActor":False,"inviteShortLinkKey":None,"isFeed":False,"isFundraiser":False,"isFunFactPost":False,"isGroup":False,"isEvent":False,"isTimeline":True,"isSocialLearning":False,"isPageNewsFeed":False,"isProfileReviews":True,"isWorkSharedDraft":False,"hashtag":None,"canUserManageOffers":False,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":True,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":True,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":True,"__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider":False,"__relay_internal__pv__IsWorkUserrelayprovider":False,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":False,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":True,"__relay_internal__pv__CometFeedStoryDynamicResolutionPhotoAttachmentRenderer_experimentWidthrelayprovider":500,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":False,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":False,"__relay_internal__pv__IsMergQAPollsrelayprovider":False,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":True,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":True,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":False,"__relay_internal__pv__GHLShouldChangeSponsoredAuctionDistanceFieldNamerelayprovider":False}),
                        'server_timestamps': 'True',
                        'doc_id': '9727242900657510',
                    }
                    data.update(ge_d)
                    response = requests.post('https://www.facebook.com/api/graphql/', cookies=cookies, headers=self.headers, data=data).text
                    if '"story":{"message":{"text":"%s'%(text) in response:
                        return True,data['av']
                    else:
                        return False,data['av']

                else:
                        return False,'invalid cookies'
        except Exception as e:
                return False,f'invalid cookies {e}'


    def page_create(self,coklis,boi=None,name_p=None):

        try:
            if name_p == None:
                names_fast = [
                'রাহমান','খান','আলম','মিঞা','আহমেদ','হোসেন','ইসলাম','চৌধুরী','মির্জা','বেগম','ভূঁইয়া','মুসা','আক্তার','মিয়া','বেগুম','নূর','আবু তালহা','মনিরুল','শাহ','মোঃ নাজমুস','সাকিব','ইমরান','জাফরুল্লাহ','মোঃ মুজিব','রফিকুল','আলমগীর','নূর আলম','হাসান','আব্দুল্লাহ','আহমেদ','মোঃ সালিম']
                last_names = ['রাহমান', 'খান', 'আলম', 'মিঞা', 'আহমেদ', 'হোসেন', 'ইসলাম', 'চৌধুরী', 'মির্জা', 'বেগম', 'ভূঁইয়া', 'মুসা', 'আক্তার', 'মিয়া', 'বেগুম', 'নূর', 'বিন্দ্যোপাধ্যায়', 'চক্রবর্তী', 'সরকার', 'দত্ত', 'ব্যানার্জি', 'ব্যানার্জী', 'মুখার্জি', 'ব্যানার্জি', 'চৌধুরী', 'সেন', 'মজুমদার', 'রায়', 'রায়', 'পাল', 'গুপ্ত', 'বসু', 'সিংহ', 'সেন', 'চাকমা', 'বর্মা', 'তালুকদার', 'মন্ডল', 'সুলতান', 'রয়', 'শর্মা', 'রহমান', 'সাহা', 'শুভ্র', 'শিকদার', 'কাবিরা', 'তালুকদার', 'রহমান', 'বেগম', 'মুক্তাদির', 'সিংহ', 'বৈদ্য', 'বড়', 'বৈদ্য', 'বড়', 'বড়', 'হাসান']
                name_p = random.choice(names_fast) + ' ' + random.choice(last_names)
            if boi == None:
                bio_p="Page Create : Mahdi Hasan\\nMY pg: https://www.facebook.com/ma4D1\\nIf you need any project contact me"
            cookis = __formate_coki__(coklis)
            req = requests.get('https://www.facebook.com/pages/creation/?ref_type=launch_point', headers=self.headers,cookies=cookis).text
            g_data =self.get_data(req)

            if g_data:
                self.headers.update({'x-fb-friendly-name': 'AdditionalProfilePlusCreationMutation',
                'x-fb-lsd': g_data['lsd']})
                data={  '__crn': 'comet.fbweb.CometAdditionalProfilePlusCreationRoute',
                    'fb_api_caller_class': 'RelayModern',
                    'fb_api_req_friendly_name': 'AdditionalProfilePlusCreationMutation',
                    'variables': json.dumps({"input":{"bio":bio_p,"categories":["2347428775505624"],"creation_source":"comet","name":name_p,"off_platform_creator_reachout_id":None,"page_referrer":"launch_point","actor_id":g_data['av'],"client_mutation_id":"3"}}),
                    'server_timestamps': 'true',
                    'doc_id': '10085210741491515',
                }
                response = requests.post('https://www.facebook.com/api/graphql/',headers=self.headers,cookies=cookis, data=data)
                parsed_data = json.loads(response.text)
                try:
                    additional_profile_id = parsed_data['data']['additional_profile_plus_create']['additional_profile']['id']
                    page_id = parsed_data['data']['additional_profile_plus_create']['page']['id']
                    return True,additional_profile_id
                except:
                    return False,'You have created too many Pages recently. Please try again later'
            else :
                return False,'invalid cookies'
        except Exception as e:
            return False ,f"invalid cookes : {e}"