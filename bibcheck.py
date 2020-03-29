import bs4
import itertools
import time
import requests
import configparser
import urllib.parse
import mechanize
import pushover
import datetime
import os

def split_notify(string):
    values = string.split(':')
    return (values[0], values[1:])


def main():
    while True:
        pushover.init(os.environ['PUSHOVER_KEY'])
        if 'HEALTHCHECK_URL' in os.environ:
            requests.get(f"{os.environ['HEALTHCHECK_URL']}/start")
        allinfo = []
        users = list(map(lambda x: x.split(':', 1), os.environ['BIB_USERS'].split(',')))
        notify = dict(map(split_notify, os.environ['NOTIFY_USERS'].split(',')))
        for user, pwd in users:
            allinfo += check(user, pwd, notify.get(user, []))
        if 'HEALTHCHECK_URL' in os.environ:
            requests.post(f"{os.environ['HEALTHCHECK_URL']}", data='\n'.join(allinfo).encode('utf8'))
        if 'RUN_FOREVER' in os.environ and os.environ['RUN_FOREVER'] == 'False':
            break

        now = datetime.datetime.utcnow
        to = (now() + datetime.timedelta(days = 1)).replace(hour=os.environ.get('RUN_AT_HOUR', 6), minute=os.environ.get('RUN_AT_MINUTE', 0), second=0)
        time.sleep((to-now()).seconds)

def check(username, password, notify_ids):
    br = mechanize.Browser()
    starturl = os.environ.get('LIBRARY_URL', 'https://ssl.muenchen.de/aDISWeb/app?service=direct/0/Home/$DirectLink&sp=SOPAC')
    response = br.open(starturl)
    br.follow_link(text_regex=r"Anmeld(en|ung abschicken)")
    br.select_form('Form0')
    br['$Textfield'] = username
    br['$Textfield$0'] = password
    response = br.submit()
    br.follow_link(text_regex=r"Konto")
    try:
        response = br.follow_link(text_regex=r"Ausleihen? zeigen")
        br.select_form('Form0')
        response = br.submit(name='textButton$0', label='Alle verlängern')
        lentlist = bs4.BeautifulSoup(response.read(), 'html.parser')
        table = lentlist.select('table[class="rTable_table"]')[0]
        allinfo = []
        for entry in table.tbody.select('tr'):
            info = list(map(lambda x: str(x.text).strip(), entry.select('td')))
            date = datetime.datetime.strptime(info[1], '%d.%m.%Y')
            delta = date - datetime.datetime.now()
            allinfo.append(str(info))
            if delta.days <= 10 or delta.days == 20 or delta.days == 15:
                message = f'Bitte an {info[3]} denken\n' 
                if delta.days <= 7:
                    message += '<font color="#ff0000">'
                message += f'Abgabe <b>{info[1]}</b>'
                if delta.days <= 7:
                    message += '</font>'
                message += f' - {username}'
                for client in itertools.chain(notify_ids, os.environ.get('PUSHOVER_CLIENTS', '').split(',')):
                    try:
                        pushover.Client(client).send_message(message, title="Erinnerung", html=1)
                    except:
                        print("No client")
    except (StopIteration, mechanize._mechanize.LinkNotFoundError) as e:
        return []
    return allinfo

if __name__ == "__main__":
    main()
