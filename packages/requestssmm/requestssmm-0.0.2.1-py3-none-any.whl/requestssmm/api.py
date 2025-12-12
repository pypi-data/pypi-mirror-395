# import logging
from requests import get
from requests import post
from requests import exceptions
# Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class InvalidURLException(Exception):
    """Custom Exception for Invalid URLs"""
    pass

class API:
    def __init__(self, url, api_key, api_type="adminapi"):
        """Initialize API instance with validation"""
        self.allowed_domains = {
            "teamluxusboostingservices.com": {"secure": True},
            "top1phsmm.com": {"secure": True}
        }
        self.api_typ = api_type

        # Validate URL
        if url not in self.allowed_domains:
            raise InvalidURLException("The provided URL is not authorized.")

        protocol = "https://" if self.allowed_domains[url]["secure"] else "http://"
        self.url = f"{protocol}{url}"
        self.api_key = api_key

    def _make_request(self, action, service_id=None, extra_data=None):
        """Private method to handle API requests with dynamic parameters"""
        payload = {
            "key": self.api_key,
            "action": action
        }

        if service_id:
            payload["type"] = service_id

        if extra_data:
            payload.update(extra_data)

        try:
            response = post(f"{self.url}/{self.api_typ}/v1", data=payload)
            response_data = response.json()

            if response_data.get("status") == "success":
                # logging.info(f"API Request Successful: {response_data}")
                return response_data
            else:
                # logging.warning(f"API Request Failed: {response_data}")
                return None

        except exceptions.RequestException as e:
            # logging.error(f"Request error: {e}")
            raise InvalidURLException(f"Request error: {e}")

    def get_order(self, service_id):
        """Retrieve a single order"""
        return self._make_request("getOrder", service_id)

    def get_orders(self, service_id):
        """Retrieve multiple orders"""
        return self._make_request("getOrders", service_id)

    def complete_order(self, order_id):
        """Mark an order as completed"""
        return self._make_request("setCompleted", extra_data={"id": order_id})


if __name__ == "__main__":
    pass