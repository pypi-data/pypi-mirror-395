from digitalguide.db_objects import WhatsAppAction, WhatsAppHandler
import mongoengine
import os
import re

import yaml

from configparser import ConfigParser

def upload_route():
    config = ConfigParser()
    config.read("config.ini")

    dbname = config["bot"]["bot_name"]
    db_url=os.environ.get("DATABASE_URL")
    db_url = re.sub("admin", dbname, db_url, 1)
    mongoengine.connect(alias=dbname, host=db_url)

    # Read YAML file
    with open(config["yaml"]["datei_states"], 'r') as states_file:
        states = yaml.safe_load(states_file)

    with open(config["yaml"]["datei_actions"], 'r') as actions_file:
        actions = yaml.safe_load(actions_file)

    # Bulk insert handlers and actions instead of saving one-by-one
    WhatsAppHandler.objects.delete()
    handler_docs = [WhatsAppHandler(SateName=key, Handlers=value) for key, value in states.items()]
    WhatsAppHandler.objects.insert(handler_docs, load_bulk=False)

    WhatsAppAction.objects.delete()
    action_docs = [WhatsAppAction(ActionName=key, Action=value) for key, value in actions.items()]
    WhatsAppAction.objects.insert(action_docs, load_bulk=False)

    mongoengine.disconnect(alias=dbname)