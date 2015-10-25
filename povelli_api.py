import base64, hashlib, hmac, json, requests
from urlparse import urlparse
from datetime import datetime
from time import mktime

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


def post_data(api_server_domain, url_path, public_key, private_key, data=[]):
    url = 'https://%s%s'%(api_server_domain, url_path)
    auth = HTTPSignatureAuth(public_key, private_key, 'POST', url_path)
    json_data = json.dumps(data)

    response = requests.post(url, auth=auth, data=json_data, headers=JSON_HEADERS, verify=SSL_VERIFY)
    status_code = response.status_code

    if status_code == 200:
        response_content = response.json()
        success = response_content.get('success', False)

    else:
        success = False
        response_content = {}

    return success, response_content

