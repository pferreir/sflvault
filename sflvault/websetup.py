"""Setup the SFLvault application"""
import logging

from paste.deploy import appconfig
from pylons import config
from datetime import datetime, timedelta

from sflvault.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup sflvault here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)

    from sflvault import model
    log.info("Creating tables")
    model.metadata.create_all(bind=config['pylons.g'].sa_engine)
    log.info("Adding 'admin' user, you have 5 minutes to setup from your client")

    ## Add default user 'admin' with 5 minutes for the client to call "sflvault setup"
    u = model.User()
    u.waiting_setup = datetime.now() + timedelta(0, 300)
    u.username = u'admin'
    u.create_time = datetime.now()
    model.Session.commit()
    
    log.info("Successfully setup")
