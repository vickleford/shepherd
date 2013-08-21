from os.path import expanduser
from flask import Flask, session, g, render_template, jsonify, redirect, url_for
from filters import ms2utc

from rackspace.monitoring import MonitoringClient


app = Flask(__name__)
app.config.from_envvar(expanduser('SHEPHERD_CONFIG'))
app.jinja_env.filters['ms2utc'] = ms2utc

rax_mon = MonitoringClient(app.config.get('APIUSER'), app.config.get('APIKEY'))

    
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
    
    # don't blow up on an entity without a label        
    try:
        sorted_vals = sorted(details['values'], key=lambda x: x['entity']['label'])
    except KeyError:
        sorted_vals = details['values']
        
    return render_template('overview.html', values=sorted_vals, meta=details['metadata'], labels=labels)


@app.route('/')
def index():
    return redirect(url_for('overview'))


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

