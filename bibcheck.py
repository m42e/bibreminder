import bs4
import requests
import configparser
import urllib.parse
import mechanize
import pushover
import datetime

pushover.init('a5uja274ec5h46paanzjqy5zo1ym6y')

def main():
    requests.get("https://health.d1v3.de/ping/5185e698-ea0b-44e0-857e-8f52487dca5d/start")
    allinfo = []
    allinfo += check('400008532980', '4F3sf7KfQC')
    allinfo += check('400006306065', '54zjxTHvIY')
    allinfo += check('800000974318', '142042')
    requests.post("https://health.d1v3.de/ping/5185e698-ea0b-44e0-857e-8f52487dca5d", data='\n'.join(allinfo).encode('utf8'))

def check(username, password):
    br = mechanize.Browser()
    starturl = 'https://ssl.muenchen.de/aDISWeb/app?service=direct/0/Home/$DirectLink&sp=SOPAC'
    response = br.open(starturl)
    br.follow_link(text_regex=r"Anmelden")
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
                pushover.Client('u5w9h8gc7hpzvr5a2kh2xh4m9zpidq').send_message('Bitte an {} denken, Abgabe {}'.format(info[3], info[1]), title="Erinnerung")
    except (StopIteration, mechanize._mechanize.LinkNotFoundError) as e:
        pushover.Client('u5w9h8gc7hpzvr5a2kh2xh4m9zpidq').send_message(f'nichts ausgeliehen {username}({e})')
    return allinfo

if __name__ == "__main__":
    main()
