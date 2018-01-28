import requests, hmac, hashlib, json, os
from datetime import timedelta, datetime

def _sign_data(message, secret):
    return hmac.new(secret.encode(), message.encode('utf-8'), hashlib.sha1).hexdigest()

def get_params(payload={}):
    key = os.environ.get('TRANSLOADIT_KEY')
    secret = os.environ.get('TRANSLOADIT_SECRET')
    expiry = (timedelta(seconds=300) + datetime.utcnow()).strftime("%Y/%m/%d %H:%M:%S+00:00")
    data = { "auth": { "key": key, "expires": expiry } }
    data.update(payload)
    json_data = json.dumps(data)
    sig = _sign_data(json_data, secret)
    return { 'params': json_data, 'signature': sig }




# >>> url = 'http://httpbin.org/post'
# >>> files = {'file': open('report.xls', 'rb')}

# >>> r = requests.post(url, files=files)
# >>> r.text
