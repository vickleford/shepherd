_Humpty Dumpty sat on the wall_,

_Humpty Dumpty had a great fall_

Oh wait, no, those were our monitors... 

Humpty is a MaaS dashboard to show you what's going on with your monitors and alerts at a glance. 
It's supposed to be read-only so you can distribute the link to it for other people to view.

### Configuring

Put string values for APIKEY and APIUSER in any python file

    # anywhere.py
    APIUSER=raxcloudusername
    APIKEY=39484389jg39gljg9sn398egou
    
### Running

Set the HUMPTY_CONFIG environment variable then run python on the application

    $ HUMPTY_CONFIG=anywhere.py python website/web.py