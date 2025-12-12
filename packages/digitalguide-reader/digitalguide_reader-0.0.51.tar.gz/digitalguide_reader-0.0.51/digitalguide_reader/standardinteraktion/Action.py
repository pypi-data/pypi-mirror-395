
import re
import os
import requests
import subprocess

def readActions(format_inhalt_list, messanger="Telegram", asset_url=""):
    actions = []
    for format, inhalt in format_inhalt_list:
        
        format_split = format.split(" - ")
        if len(format_split) == 2 and format_split[1] != messanger:
            continue
        elif len(format_split) == 2:
            format = format_split[0]

        action = {}

        if format == "Textnachricht":
            if messanger =="Telegram":
                inhalt = inhalt.replace(".", "\.")
                inhalt = inhalt.replace("(", "\(")
                inhalt = inhalt.replace(")", "\)")
                inhalt = inhalt.replace("!", "\!")
                inhalt = inhalt.replace("?", "\?")
                inhalt = inhalt.replace("-", "\-")
                inhalt = inhalt.replace("+", "\+")
                inhalt = inhalt.replace("#", "\#")

                action["parse_mode"] = "MarkdownV2"

            action["type"] = "message"
            action["text"] = inhalt

        elif format == "Interaktive Textnachricht":
            action["type"] = "message"

            text_match = re.search(r"Text: (?P<text>(.?\n?)*?)(^.*:|\Z)", inhalt, re.MULTILINE)
            if text_match:
                action["text"] = text_match.group('text').strip()
            else:
                print("In der intaraktiven Nachricht ist kein Text hinterlegt: {}".format(inhalt))

            text_match = re.search(r"Footer: (?P<footer>.*)", inhalt)
            if text_match:
                footer = text_match.group('footer')
                if len(footer) > 60:
                    print("Error: Footer can not be longer 60 characters: {}".format(footer)) 
                action["footer"] = footer
            else:
                print("Info: In der intaraktiven Nachricht ist kein Footer hinterlegt: {}".format(inhalt))

            buttons_matches = re.findall(r"Button_(?P<id>.*): (?P<button_text>.*)", inhalt)
            if buttons_matches:
                buttons = []
                for buttons_match in buttons_matches:
                    button = {}
                    button["id"] = buttons_match[0]
                    button["text"] = buttons_match[1]
                    if len(button["text"]) > 20:
                        print("Error: Button can not be longer 20 characters: {}".format(button["text"])) 
                    buttons.append(button)
                action["reply_buttons"] = buttons
            else:
                print("Error: In der intaraktiven Nachricht sind keine Buttons hinterlegt: {}".format(inhalt))


        elif format == "Listen Textnachricht":
            action["type"] = "message"

            text_match = re.search(r"Text: (?P<text>(.?\n?)*?)(^.*:|\Z)", inhalt, re.MULTILINE)
            if text_match:
                action["text"] = text_match.group('text').strip()
            else:
                print("In der intaraktiven Nachricht ist kein Text hinterlegt: {}".format(inhalt))

            footer_match = re.search(r"Footer: (?P<footer>.*)", inhalt)
            if footer_match:
                footer = footer_match.group('footer')
                if len(footer) > 60:
                    print("Error: Footer can not be longer 60 characters: {}".format(footer)) 
                action["footer"] = footer
            else:
                print("Info: In der intaraktiven Nachricht ist kein Footer hinterlegt: {}".format(inhalt))

            button_match = re.search(r"Button: (?P<button>.*)", inhalt)
            if button_match:
                action["button"] = button_match.group('button')
            else:
                print("In der intaraktiven Nachricht ist kein Text hinterlegt: {}".format(inhalt))

            section_title_match = re.search(r"Section Title: (?P<section_title>.*)", inhalt)
            if section_title_match:
                action["section_title"] = section_title_match.group('section_title')
            else:
                print("In der intaraktiven Nachricht ist kein Text hinterlegt: {}".format(inhalt))

            row_matches = re.findall(r"Row_(?P<id>.*): (?P<row_title>.*)", inhalt)
            if row_matches:
                rows = []
                for row_match in row_matches:
                    row = {}
                    row["id"] = row_match[0]
                    if len(row_match[1].split("| ")) == 1:
                        row["title"] = row_match[1]
                    if len(row_match[1].split("| ")) == 2:
                        row["title"] = row_match[1].split("| ")[0]
                        row["description"] = row_match[1].split("| ")[1]
                        if len(row["description"]) > 72:
                            print("Error: row description can not be longer 24 characters: {}".format(row["description"]))
                    if len(row["title"]) > 24:
                        print("Error: row title can not be longer 24 characters: {}".format(row["title"]))
                    rows.append(row)
                action["rows"] = rows
            else:
                print("Error: In der intaraktiven Nachricht sind keine Buttons hinterlegt: {}".format(inhalt))

            
        elif format == "Audionachricht":
            action["type"] = "audio"
            regex = r"Datei: (?P<file>.*)\nAnzeigename: (?P<name>.*)\nPerformer: (?P<performer>.*)"

            match = re.search(regex, inhalt)
            if match:
                action["url"] = os.path.join(asset_url, match.group('file'))
                if requests.get(action["url"]).status_code != 200:
                    print("Die angegebenen Datei ({}) konnte nicht unter der Asset URL ({}) gefunden werden.".format(
                    match.group('file'), asset_url))
                action["title"] = match.group('name')
                action["performer"] = match.group('performer')
            else:
                action["url"] = os.path.join(asset_url, "platzhalter.mp3")
                action["title"] = inhalt
                action["performer"] = "🤖"

        elif format == "Sprachnachricht":
            action["type"] = "voice"
            regex = r"Datei: (?P<file>.*)"

            match = re.search(regex, inhalt)
            if match:              
                if messanger=="Telegram":
                    mp3_filepath = os.path.join("assets/", match.group('file'))
                    ogg_filename = match.group('file').replace(".mp3", ".ogg")
                    ogg_filepath =  os.path.join("assets/", ogg_filename)
                    subprocess.run(["ffmpeg", "-loglevel", "error", '-i', mp3_filepath, "-b:a", " 64k", "-ac", "1", '-acodec', 'libopus', '-y', "-hide_banner", ogg_filepath])
                    action["file"] = ogg_filepath
                else:
                    action["url"] = os.path.join(asset_url, match.group('file'))
            else:
                print("Error: Für die Sprachnachricht wurde keine Datei angegeben ({}). Platzhalter wird benutzt".format(inhalt))
                action["url"] = os.path.join(asset_url, "platzhalter.mp3")
                action["caption"] = inhalt

        elif format == "Foto":
            action["type"] = "photo"            
            file_match = re.search(r"Datei: (?P<file>.*)", inhalt)

            if file_match:
                if messanger=="Telegram":
                    action["file"] = os.path.join("assets", file_match.group('file'))
                    action["url"] = os.path.join(asset_url, "platzhalter.png")
                else:
                    action["url"] = os.path.join(asset_url, file_match.group('file'))

            caption_match = re.search(r"Anzeigename: (?P<name>.*)", inhalt)
            if caption_match:
                action["caption"] = caption_match.group('name')

        elif format == "GIF":
            action["type"] = "document"
            regex = r"Datei: (?P<file>.*)\nAnzeigename: (?P<name>.*)"

            match = re.search(regex, inhalt)
            if match:
                action["url"] = os.path.join(asset_url, match.group('file'))
                if requests.get(action["url"]).status_code != 200:
                    print("Die angegebene Datei ({}) konnte nicht unter der Asset URL ({}) gefunden werden.".format(
                    match.group('file'), asset_url))
                action["caption"] = match.group('name')
            else:
                action["url"] = os.path.join(asset_url, "platzhalter.png")
                action["caption"] = inhalt

        elif format == "GPS":
            action["type"] = "venue"

            action["longitude"] = re.search(
                r"L: (?P<long>.*)", inhalt).group('long')
            action["latitude"] = re.search(r"B: (?P<lat>.*)", inhalt).group('lat')
            action["title"] = re.search(
                r"Anzeigename: (?P<name>.*)", inhalt).group('name')
            action["address"] = re.search(
                r"Adresse: (?P<address>.*)", inhalt).group('address')

        elif format == "Video":
            action["type"] = "video"
            regex = r"Datei: (?P<file>.*)"

            match = re.search(regex, inhalt)
            if match:
                action["url"] = os.path.join(asset_url, match.group('file'))
            caption_match = re.search(r"Anzeigename: (?P<name>.*)", inhalt)
            if caption_match:
                action["caption"] = caption_match.group('name')
                
        elif format == "Sticker":
            id_regex = r"ID: (?P<id>.*)$"
            id_match = re.search(id_regex, inhalt)

            file_match = re.search(r"Datei: (?P<file>.*)", inhalt)

            action["type"] = "sticker"
            if id_match:
                action["id"] = id_match.group('id')
            elif file_match:
                action["url"] = os.path.join(asset_url, file_match.group('file'))
            else:
                print("Die angegebenen Informationen im Feld ({}) stimmen nicht mit dem angegebenen Format ({}) überein.".format(
                    inhalt, format))
        elif format == "Kontextspeicherung":
            action["type"] = "function"
            action["func"] = "contextActions:save_text_to_context"
            action["key"] = inhalt
        elif format == "Return":
            action["type"] = "return"
            action["state"] = inhalt
        elif format == "Formel":
            action["type"] = "function"
            action["func"] = re.search(
                r"function: (?P<function>.*)", inhalt).group('function')
            for line in inhalt.split("\n")[1:]:
                if len(line.split(": "))==2:
                    argument, value = line.split(": ")
                    action[argument] = value

        else:
            print("Das angegebene Format ({}) ist nicht bekannt".format(format))

        if action:
            actions.append(action)

    return actions
