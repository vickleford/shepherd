from flask import Flask, session, g, render_template, jsonify

from rackspace import identity
from rackspace.monitoring import MonitoringClient

app = Flask(__name__)
app.config.from_envvar('HUMPTY_CONFIG')


identity_response = identity.auth_with_key(app.config.get('APIUSER'), 
                                               app.config.get('APIKEY'))
                                               
rax_token = identity.get_token(identity_response)
rax_maas = identity.get_maas_endpoint(identity_response)
rax_mon = MonitoringClient(rax_maas, rax_token)


@app.route('/overview')
def overview():
    details = rax_mon.get_overview()
    
    # latest alarm states don't come with alarm labels ;(
    labels = {}
    for ent in details['values']:
        for las in ent['latest_alarm_states']:
            # search for alarm labels matching this latest alarm status
            for alarm in ent['alarms']:
                if alarm['id'] == las['alarm_id']:
                    labels.update({las['alarm_id']: alarm['label']})
            
    return render_template('overview.html', values=details['values'], meta=details['metadata'], labels=labels)


@app.route('/entity/<entityid>/alarm/<alarmid>')
def alarm(entityid, alarmid):
    details = rax_mon.get_alarm(entityid, alarmid)
    
    return render_template('alarm.html', entity=entityid, alarm=details)
    

@app.route('/history/<entityid>/<alarmid>')
def alarm_history(entityid, alarmid):
    details = rax_mon.discover_alarm_history(entityid, alarmid)
    details.update({'entity_id': entityid, 'alarm_id': alarmid})
    
    return jsonify(details)


@app.route('/history/<entityid>/<alarmid>/<checkid>')
def list_alarm_history(entityid, alarmid, checkid):
    details = rax_mon.list_alarm_history(entityid, alarmid, checkid)
    details.update({'entity_id': entityid, 'alarm_id': alarmid})
    
    return jsonify(details)
  
  
@app.route('/history/<entityid>/<alarmid>/<checkid>/<uuid>')
def get_alarm_history(entityid, alarmid, checkid, uuid):
    details = rax_mon.get_alarm_history(entityid, alarmid, checkid, uuid)
    details.update({'entity_id': entityid, 'alarm_id': alarmid})
    
    return jsonify(details)

    
if __name__ == '__main__':
    app.run(debug=True)

