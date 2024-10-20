import requests
base_url = "http://127.0.0.1:8000/"
def make_request(endpoint=None, method="GET", params=None, data=None):
    url = base_url
    if endpoint:
        url += f"/{endpoint}"
    if method == "GET":
        response = requests.get(url)
    if response:
        return response.json()
    return None
                
    