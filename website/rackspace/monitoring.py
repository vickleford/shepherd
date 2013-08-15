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
        
    def discover_alarm_history(self, entityid, alarmid):
        """Return json for the checks on an alarm history discovery."""
        
        url = "{0}/entities/{1}/alarms/{2}/notification_history".format(self.endpoint, entityid, alarmid)
        
        r = requests.get(url, headers=self.headers)
        
        return r.json()
        
    def list_alarm_history(self, entityid, alarmid, checkid):
        """Return the list of alarm notification histories."""
        
        url = "{0}/entities/{1}/alarms/{2}/notification_history/{3}".format(self.endpoint, entityid, alarmid, checkid)
        
        r = requests.get(url, headers=self.headers)
        
        return r.json()
                
    def get_alarm_history(self, entityid, alarmid, checkid, uuid):
        """Return an alarm's notification history."""

        url = "{0}/entities/{1}/alarms/{2}/notification_history/{3}/{4}".format(self.endpoint, entityid, alarmid, checkid, uuid)

        r = requests.get(url, headers=self.headers)

        return r.json()