from requests import get, post, exceptions
from json import dumps, loads
class API:
    def __init__(self, url, api_key, api_type="adminapi/v2"):
        self.allowed_domains = {
            "teamluxusboostingservices.com": {"secure": True},
            "top1phsmm.com": {"secure": True},
            "1semail.com": {"secure": True}
        }
        self.api_typ = api_type

        # Validate URL
        if url not in self.allowed_domains:
             return("The provided URL is not authorized.")

        protocol = "https://" if self.allowed_domains[url]["secure"] else "http://"
        self.url = f"{protocol}{url}/{self.api_typ}"
        self.api_key = api_key
        self.HEADERS = {
                "X-Api-Key": self.api_key,
                "Content-Type": "application/json"
            }
        # print(self.url)
    
    def api_get(self,endpoint, params=None):
        url = f"{self.url}{endpoint}"
        response = get(url, headers=self.HEADERS, params=params)
        return response.json()
    def api_post(self,endpoint, data=None):
        url = f"{self.url}{endpoint}"
        response = post(url, headers=self.HEADERS, data=dumps(data))
        return response.json()

    def getorders(self,limit=10, status=None):
        params = {
            "limit": limit,
            "sort": "date-desc"
        }
        if status:
            params["order_status"] = status
        return self.api_get("/orders", params=params)
    def gets_order(self, service_id):
        try:
            get_oder = self.getorders(limit=100, status=None)
            return[ i for i in get_oder['data']['list'] if i['service_id'] == service_id]
        except Exception as e:
            print(e)

    def change_order_status(self,order_ids, status):
        data = {
            "ids": ",".join(str(i) for i in order_ids),
            "status": status
        }
        return self.api_post("/orders/change-status", data=data)
    def smm_info(self,order_id):
        try:
            x=[]
            gets_order = self.gets_order(order_id)
            for i in gets_order:
                x.append({
                    "id" : i['id'],
                    "user" : i['user'],
                    'quantity' : i['quantity'],
                    "start_count" : i['start_count'],
                    "service_name" : i['service_name'],
                    "service_id" : i['service_id'],
                    "status" : i['status'],
                    "link" : i['link'],
                    "created" : i['created'],
    
                })
            return x
        except Exception as e:
            print(e)

    def update_order(self,order_ids:int, status=None, remains=None, start_count=None, cancel_reason=None):
        json_data = {
    'orders': [
        {
            'id': order_ids,
            'status': status,
            'remains': remains,
            'start_count': start_count,
            'cancel_reason': cancel_reason
        },
    ],
}
        return self.api_post("/orders/update", data=json_data)

