import requests
import bs4
import configparser
import urllib.parse
import mechanize

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



if __name__ == "__main__":
    main()
