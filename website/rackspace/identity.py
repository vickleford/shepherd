import requests
import json


url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'


def auth_with_key(username, apikey):
    """Return an auth response."""
    
    headers = {'Content-Type': 'application/json'}
    
    payload = {
                'auth': {
                    'RAX-KSKEY:apiKeyCredentials': {
                        'username': username,
                        'apiKey': apikey
                    }
                 }
               }
               
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    return r.json()


def get_token(authresponse):
    """Return a token from an auth response."""
    
    return authresponse['access']['token']['id']
    

def get_maas_endpoint(authresponse):
    """Return the MaaS endpoint from an auth response."""
    
    for endpoints in authresponse['access']['serviceCatalog']:
        if endpoints['name'] == 'cloudMonitoring':
            return endpoints['endpoints'][0]['publicURL']


