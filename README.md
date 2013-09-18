Shepherd is a MaaS dashboard to show you what's going on with your monitors and alerts at a glance. 
It's supposed to be read-only so you can distribute the link to it for other people to view.

### Installing dependencies

Once you've cloned the repository, run the following command to install dependencies:

    sudo pip install -r requirements.txt
    
### Configuring

Put string values for APIKEY and APIUSER in any python file

    # anywhere.py
    APIUSER='raxcloudusername'
    APIKEY='39484389jg39gljg9sn398egou'
    
### Running

Set the SHEPHERD_CONFIG environment variable then run python on the application

    (shepherd)aluminum13:shepherd$ SHEPHERD_CONFIG=~/.config/shepherd.py python website/web.py
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader
