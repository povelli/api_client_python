import base64, hashlib, hmac, json, requests
from urlparse import urlparse
from datetime import datetime
from time import mktime

API_DOMAIN = "dev.povelli.com"
API_URL_PRODUCTS_UPDATE = "/e/backoffice/products/update"
API_URL_PRODUCTS_DELETE = "/e/backoffice/products/delete"
API_URL_PRODUCTS_GET    = "/e/backoffice/products/status"
API_URL_LABELS_GET      = "/e/backoffice/labels/status"
API_URL_LABELS_ASSIGN   = "/e/backoffice/labels/assign"
API_URL_LABELS_UNASSIGN = "/e/backoffice/labels/unassign"

JSON_HEADERS = {'Accept': 'application/json', 'Content-type': 'application/json'}
SSL_VERIFY = True

def _sign_string(string, private_key=''):
    """
    given a string and a private_key, the method returns the signature resulting to apply hmac-sha256
    """
    return base64.b64encode(hmac.new(str(private_key), string, hashlib.sha256).digest())


def generate_request_signature(public_key, private_key, method, path, timestamp=None, data=None, files=None):
    # if no timestamp provided, generate one using the current time
    if timestamp is None:
        timestamp = str(mktime(datetime.now().timetuple()))

    signable_list = [public_key, str(timestamp), method, path]
    signable = '\n'.join(signable_list)
    signature = _sign_string(signable, private_key)

    return signature


class HTTPSignatureAuth(requests.auth.AuthBase):
    '''
    Sign a request using the http-signature scheme.
    https://github.com/joyent/node-http-signature/blob/master/http_signing.md
    
    public_key is the mandatory label indicating to the server which private_key to use
    private_key is a secret string shared by the client and the server
    method is the HTTP method used: GET, POST, PUT, PATCH, DELETE in uppercase
    path is the complete url, including any get param, excluding the domain and starting with a /
    timestamp is a date in unix time format (number of seconds from 1970/01/01 00:00
    data is a string with the payload of a POST/PUT/PATCH method
    files is a list of attached files
    '''
    def __init__(self, public_key, private_key, method, path, timestamp=None, data=None, files=None):
        if timestamp is None:
            timestamp = str(mktime(datetime.now().timetuple()))

        self.public_key = public_key
        self.private_key = private_key
        self.method = method.upper()
        self.path = path
        self.timestamp = timestamp
        self.data = data
        self.files = files

    def __call__(self, request):
        signature = generate_request_signature(self.public_key, self.private_key, self.method, self.path, 
                                               timestamp=self.timestamp, data=self.data, files=self.files)
        request.headers['PV-Signature'] = signature
        request.headers['PV-Timestamp'] = self.timestamp
        request.headers['PV-Public-Key'] = self.public_key

        return request

def _post_data(api_server_domain, url_path, public_key, private_key, data=[], method="POST"):
    url = 'https://%s%s'%(api_server_domain, url_path)
    auth = HTTPSignatureAuth(public_key, private_key, method, url_path)
    json_data = json.dumps(data)

    if method.upper() == "POST":
        method_func = requests.post
    elif method.upper() == "DELETE":
        method_func = requests.delete
    elif method.upper() == "GET":
        method_func = requests.get
    else:
        raise Exception ("Invalid method!")
        
    response = method_func(url, auth=auth, data=json_data, headers=JSON_HEADERS, verify=SSL_VERIFY)
    status_code = response.status_code

    if status_code == 200:
        response_content = response.json()
        success = response_content.get('success', False)

    else:
        raise Exception ("Unauthorized! [%s]" % status_code)

    return success, response_content

def send_product_updates(public_key, private_key, products):
    return _post_data(API_DOMAIN, API_URL_PRODUCTS_UPDATE, public_key, private_key, products, "POST")
    
def delete_products(public_key, private_key, products):
    return _post_data(API_DOMAIN, API_URL_PRODUCTS_DELETE, public_key, private_key, products, "DELETE")
    
def get_products(public_key, private_key, products):
    return _post_data(API_DOMAIN, API_URL_PRODUCTS_GET, public_key, private_key, products, "POST")

def get_labels(public_key, private_key, labels):
    return _post_data(API_DOMAIN, API_URL_LABELS_GET, public_key, private_key, labels, "POST")

def assign_labels(public_key, private_key, label_assignments):
    return _post_data(API_DOMAIN, API_URL_LABELS_ASSIGN, public_key, private_key, label_assignments, "POST")

def unassign_labels(public_key, private_key, labels):
    return _post_data(API_DOMAIN, API_URL_LABELS_UNASSIGN, public_key, private_key, labels, "POST")
    