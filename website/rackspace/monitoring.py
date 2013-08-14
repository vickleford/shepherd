import requests
import json


class MonitoringClient(object):
    
    def __init__(self, endpoint, token):
        self.headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
        self.token = token
        self.endpoint = endpoint

    def get_overview(self, entities=None):
        """Return the overview for this account."""
        
        url = "{0}/views/overview".format(self.endpoint)
        
        if entities is not None:
            qs = {}
            for e in entities:
                qs.update({'entityId': e})
                
            r = requests.get(url, headers=self.headers, params=qs)
        else:
            r = requests.get(url, headers=self.headers)
            
        return r.json()
        
    def get_alarm(self, entityid, alarmid):
        """Return the details for an alarm."""
        
        url = "{0}/entities/{1}/alarms/{2}".format(self.endpoint, entityid, alarmid)
        
        r = requests.get(url, headers=self.headers)
        
        return r.json()