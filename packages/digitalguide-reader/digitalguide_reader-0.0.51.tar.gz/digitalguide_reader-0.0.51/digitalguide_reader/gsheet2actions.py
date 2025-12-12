import yaml
import json
from digitalguide_reader import gsheet_utils
from digitalguide_reader.standardinteraktion.Route import Route
from openpyxl import load_workbook

from configparser import ConfigParser

def gsheet2actions():
    config = ConfigParser()
    config.read("config.ini")

    interaktion_spalte = int(config.get("gsheet", "spalte_interaktion", fallback=1))
    poi_spalte = int(config.get("gsheet", "spalte_poi", fallback=0))
    aktion_spalte = int(config.get("gsheet", "spalte_aktion", fallback=2))
    format_spalte = int(config.get("gsheet", "spalte_format", fallback=3))
    inhalt_spalte = int(config.get("gsheet", "spalte_inhalt", fallback=4))

    messanger = config.get("build", "messenger", fallback="WhatsApp")

    sheet_id = config.get("gsheet", "sheet_id")


    CLIENT_SECRET_FILE = "client_secret.json"
    API_NAME = "drive"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    excel_file = "tmp.xlsx"

    service = gsheet_utils.Create_Service(
        CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    gsheet_utils.sheed_id2excel(service, sheet_id, excel_file)

    workbook = load_workbook(filename=excel_file)
    page_names = config.get("gsheet", "page_names", fallback=[workbook.active])

    combined_excel_dict = {}
    for sheet_name in json.loads(page_names):
        sheet = workbook[sheet_name]
        excel_dict = gsheet_utils.excel2dict(
            sheet, interaktion_spalte, poi_spalte, aktion_spalte, format_spalte, inhalt_spalte, None)

        #check for overlapping keys in the dict
        if set(combined_excel_dict.keys()).intersection(set(excel_dict.keys())):
            print("Warning: Overlapping keys found in the different sheets: {}".format(
                set(combined_excel_dict.keys()).intersection(set(excel_dict.keys()))))
        combined_excel_dict.update(excel_dict)


    route = Route()

    route.from_excel_dict(combined_excel_dict, messanger=messanger, asset_url=config["assets"]["url"])
    states = route.states
    actions = route.actions

    ## WRITE TO YAML
    print("yaml" in config)
    if "yaml" in config:
        with open(config["yaml"]["datei_states"], 'w') as outfile:
            yaml.dump(dict(states), outfile, allow_unicode=True)

        with open(config["yaml"]["datei_actions"], 'w') as outfile:
            yaml.dump(dict(actions), outfile, allow_unicode=True)