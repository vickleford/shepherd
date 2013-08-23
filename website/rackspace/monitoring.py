import requests
import json

import identity


class MonitoringClient(object):
    
    def __init__(self, user, key):
        self.user = user
        self.key = key
        
        self.token = None
        self.endpoint = None
        self.headers = { 'Content-Type': 'application/json',
                         'X-Auth-Token': self.token }
        
        self._authenticate()
        
    def _authenticate(self):
        """Get a new authentication token."""
        identity_response = identity.auth_with_key(self.user, self.key)
        self.token = identity.get_token(identity_response)
        self.endpoint = identity.get_maas_endpoint(identity_response)
        self.headers.update({'X-Auth-Token': self.token})

    def _send_request(self, 
                      url, 
                      method=requests.get,
                      params=None, 
                      payload=None):
        """Send request to url and ensure we can keep a valid token.
        
        url where to send the request to:
        params: a dict of what you would put in the query string
        method: requests,get, requests.post, what you want to do...
        headers: a dict of headers
        payload: a json dict of the request body
        """
                
        response = method(url, params=params, data=payload, headers=self.headers)
        if response.status_code == 401:
            self._authenticate()
            response = method(url, params=params, data=payload, headers=headers)
        
        return response
        
    def get_entity(self, entityid):
        """Return an entity represented in JSON."""
        
        url = "{0}/entities/{1}".format(self.endpoint, entityid)
        
        r = self._send_request(url)
        
        return r.json()
        
    def get_checks(self, entityid):
        """Return checks for an entity represented in JSON."""

        url = "{0}/entities/{1}/checks".format(self.endpoint, entityid)

        r = self._send_request(url)

        return r.json()
    
    def get_alarms(self, entityid):
        """Return alarms for an entity represented in JSON."""

        url = "{0}/entities/{1}/alarms".format(self.endpoint, entityid)

        r = self._send_request(url)

        return r.json()
        
    def get_overview(self, entities=None):
        """Return the overview for this account."""

        url = "{0}/views/overview".format(self.endpoint)

        try:
            qs = {}
            for e in entities:
                qs.update({'entityId': e})
            r = self._send_request(url, params=qs)
        except TypeError:
            # that's ok, we just weren't given any entities
            r = self._send_request(url)            
            
        return r.json()
                
    def get_alarm(self, entityid, alarmid):
        """Return the details for an alarm."""
        
        url = "{0}/entities/{1}/alarms/{2}".format(self.endpoint, entityid, alarmid)
        
        r = self._send_request(url)
        
        return r.json()
        
    def discover_alarm_history(self, entityid, alarmid):
        """Return json for the checks on an alarm history discovery."""
        
        url = "{0}/entities/{1}/alarms/{2}/notification_history".format(self.endpoint, entityid, alarmid)
        
        r = self._send_request(url)
        
        return r.json()
        
    def list_alarm_history(self, entityid, alarmid, checkid, limit=None, marker=None):
        """Return the list of alarm notification histories."""
        
        url = "{0}/entities/{1}/alarms/{2}/notification_history/{3}".format(self.endpoint, entityid, alarmid, checkid)
        
        r = self._send_request(url, params={'marker': marker, 'limit': limit})
        
        return r.json()
                
    def get_alarm_history(self, entityid, alarmid, checkid, uuid):
        """Return an alarm's notification history."""

        url = "{0}/entities/{1}/alarms/{2}/notification_history/{3}/{4}".format(self.endpoint, entityid, alarmid, checkid, uuid)

        r = self._send_request(url)

        return r.json()
        
    def list_metrics(self, entityid, checkid):
        """Return a list of metrics associated with your check."""
        
        url = "{0}/entities/{1}/checks/{2}/metrics".format(self.endpoint, entityid, checkid)
        
        r = self._send_request(url)
        
        return r.json()
        
    def fetch_data_points(self, entityid, checkid, metricname, **qs):
        """Return data points between two points in time for metricname on checkid.
        
        qs is the querystring and controls the data points returned.
            Required: from=msSinceEpoch 
            Required: to=msSinceEpoch
        
            Required:
                points=numberPoints
                or resolution=granulatiry
        
            Optional: select=average|variance|min|max
                Since we can add multiple select parameters, 
                should we expect this to come in as a list?
        
        http://docs.rackspace.com/cm/api/v1.0/cm-devguide/content/metrics-api.html#fetch-data-points
        http://docs.rackspace.com/cm/api/v1.0/cm-devguide/content/metrics-api.html#metrics-data-granularity
        """
        
        pass