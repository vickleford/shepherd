from os.path import expanduser
from flask import Flask, session, g, render_template, jsonify, redirect, url_for, request
from filters import ms2utc

from rackspace.monitoring import MonitoringClient


app = Flask(__name__)
app.config.from_envvar(expanduser('SHEPHERD_CONFIG'))
app.jinja_env.filters['ms2utc'] = ms2utc

rax_mon = MonitoringClient(app.config.get('APIUSER'), app.config.get('APIKEY'))


def _tag_alarm_labels(overview):
    # latest alarm states don't come with alarm labels ;(
    labels = {}
    for ent in overview['values']:
        for las in ent['latest_alarm_states']:
            # search for alarm labels matching this latest alarm status
            for alarm in ent['alarms']:
                if alarm['id'] == las['alarm_id']:
                    labels.update({las['alarm_id']: alarm['label']})

    return labels


@app.route('/')
def index():
    return redirect(url_for('overview'))
    
    
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
        
    return render_template('overview.html', values=sorted_vals, meta=details['metadata'], labels=_tag_alarm_labels(details))

@app.route('/entity/<entityid>')
def entity_overview(entityid):
    entity = rax_mon.get_entity(entityid)
    checks = rax_mon.get_checks(entityid)
    alarms = rax_mon.get_alarms(entityid)
    overview = rax_mon.get_overview(entities=[entity['id']])
    
    rendered_template = render_template('entity.html', 
                                        entity=entity, 
                                        checks=checks, 
                                        alarms=alarms, 
                                        overview=overview['values'],
                                        labels=_tag_alarm_labels(overview))
    
    return rendered_template


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
    marker = request.args.get('marker')
    details = rax_mon.list_alarm_history(entityid, alarmid, checkid, marker=marker)
    details.update({'entity_id': entityid, 'alarm_id': alarmid})
    
    return jsonify(details)
  
  
@app.route('/history/<entityid>/<alarmid>/<checkid>/<uuid>')
def get_alarm_history(entityid, alarmid, checkid, uuid):
    details = rax_mon.get_alarm_history(entityid, alarmid, checkid, uuid)
    details.update({'entity_id': entityid, 'alarm_id': alarmid})
    
    return jsonify(details)


@app.route('/metrics/<entityid>/<checkid>')
def metrics(entityid, checkid):
    check = rax_mon.get_check(entityid, checkid)
    metrics = rax_mon.list_metrics(entityid, checkid)

    return render_template('metrics.html', entityid=entityid, check=check, metrics=metrics)
        

@app.route('/metrics/<entityid>/<checkid>/<metricname>')
def get_metrics(entityid, checkid, metricname):
    params = { 'from': request.args.get('starttime'),
               'to': request.args.get('endtime'),
               'points': request.args.get('density'),
               'metric': metricname
             }
             
    plot = rax_mon.fetch_data_points(entityid, checkid, metricname, **params)
    
    return jsonify(plot)
    
    
@app.route('/d3-line-chart')
def tutorial():
    return render_template('tutorial.html')
    
    
if __name__ == '__main__':
    app.run(debug=True)

