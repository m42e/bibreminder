import bs4
import configparser
import urllib.parse
import mechanize
import pushover
import datetime

pushover.init('a5uja274ec5h46paanzjqy5zo1ym6y')

def main():
    br = mechanize.Browser()
    starturl = 'https://ssl.muenchen.de/aDISWeb/app?service=direct/0/Home/$DirectLink&sp=SOPAC'
    response = br.open(starturl)
    br.follow_link(text_regex=r"Anmelden")
    br.select_form('Form0')
    br['$Textfield'] = '400006306065'
    br['$Textfield$0'] = '54zjxTHvIY'
    response = br.submit()
    br.follow_link(text_regex=r"Konto")
    response = br.follow_link(text_regex=r"Ausleihe zeigen")
    lentlist = bs4.BeautifulSoup(response.read(), 'html.parser')
    table = lentlist.select('table[class="rTable_table"]')[0]
    for entry in table.tbody.select('tr'):
        info = list(map(lambda x: str(x.text).strip(), entry.select('td')))
        date = datetime.datetime.strptime(info[1], '%d.%m.%Y')
        delta = date - datetime.datetime.now()

        if delta.days <= 10 or delta.days == 20 or delta.days == 15:
            pushover.Client('u5w9h8gc7hpzvr5a2kh2xh4m9zpidq').send_message('Bitte an {} denken, Abgabe {}'.format(info[3], info[1]), title="Erinnerung")

if __name__ == "__main__":
    main()
