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
import logging

logging.basicConfig(level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO")))
_logger = logging.getLogger(__name__)


def split_notify(string):
    values = string.split(":")
    return (values[0], values[1:])


def main():
    try:
        pushover.init(os.environ["PUSHOVER_KEY"])
    except:
        _logger.exception("Pushover KEY is required")
        return
    while True:
        try:
            _logger.info("Starting Bibcheck")
            if "HEALTHCHECK_URL" in os.environ:
                _logger.info("Pinging Healthcheck [start]")
                _logger.debug(
                    f"Pinging Healthcheck Url {os.environ['HEALTHCHECK_URL']}/start"
                )
                requests.get(f"{os.environ['HEALTHCHECK_URL']}/start")
            allinfo = []
            users = list(
                map(lambda x: x.split(":", 1), os.environ["BIB_USERS"].split(","))
            )
            notify = dict(map(split_notify, os.environ["NOTIFY_USERS"].split(",")))
            _logger.info(f"Found {len(users)} user(s) to check for")
            for user, pwd in users:
                _logger.info(f"Check for {user}")
                allinfo += check(user, pwd, notify.get(user, []))
            if "HEALTHCHECK_URL" in os.environ:
                _logger.info("Pinging Healthcheck [stop]")
                requests.post(
                    f"{os.environ['HEALTHCHECK_URL']}",
                    data="\n".join(allinfo).encode("utf8"),
                )
            if "RUN_FOREVER" in os.environ and os.environ["RUN_FOREVER"] == "False":
                _logger.info("Finished")
                break
        except Exception as e:
            _logger.exception("Check Failed ")
            if "HEALTHCHECK_URL" in os.environ:
                _logger.info("Pinging Healthcheck [failed]")
                _logger.debug(
                    f"Pinging Healthcheck Url {os.environ['HEALTHCHECK_URL']}/fail"
                )
                requests.post(
                    f"{os.environ['HEALTHCHECK_URL']}/fail",
                    data="\n".join(allinfo).encode("utf8"),
                )

        now = datetime.datetime.utcnow
        to = (now() + datetime.timedelta(days=1)).replace(
            hour=os.environ.get("RUN_AT_HOUR", 6),
            minute=os.environ.get("RUN_AT_MINUTE", 0),
            second=0,
        )
        _logger.info(f"Sleeping till {to.isoformat()}")
        time.sleep((to - now()).seconds)


def check(username, password, notify_ids):
    br = mechanize.Browser()
    starturl = os.environ.get(
        "LIBRARY_URL",
        "https://ssl.muenchen.de/aDISWeb/app?service=direct/0/Home/$DirectLink&sp=SOPAC",
    )
    _logger.info(f"Library URL used: {starturl}")
    response = br.open(starturl)
    _logger.info(f"Goto loginpage")
    br.follow_link(text_regex=r"Anmeld(en|ung abschicken)")
    _logger.info(f"Fill form")
    br.select_form("Form0")
    br["$Textfield"] = username
    br["$Textfield$0"] = password
    _logger.info(f"Sumbit form")
    response = br.submit()
    _logger.info(f"Open account page")
    br.follow_link(text_regex=r"Konto")
    try:
        _logger.info(f"Open lent list")
        response = br.follow_link(text_regex=r"Ausleihen? zeigen")
        br.select_form("Form0")
        response = br.submit(name="textButton$0", label="Alle verlängern")
        lentlist = bs4.BeautifulSoup(response.read(), "html.parser")
        table = lentlist.select('table[class="rTable_table"]')[0]
        allinfo = []
        _logger.info(f"Parsing table")
        for entry in table.tbody.select("tr"):
            info = list(map(lambda x: str(x.text).strip(), entry.select("td")))
            date = datetime.datetime.strptime(info[1], "%d.%m.%Y")
            delta = date - datetime.datetime.now()
            allinfo.append(str(info))
            if delta.days <= 10 or delta.days == 20 or delta.days == 15:
                message = f"Bitte an {info[3]} denken\n"
                if delta.days <= 7:
                    message += '<font color="#ff0000">'
                message += f"Abgabe <b>{info[1]}</b>"
                if delta.days <= 7:
                    message += "</font>"
                message += f" - {username}"
                for client in itertools.chain(
                    notify_ids, os.environ.get("PUSHOVER_CLIENTS", "").split(",")
                ):
                    try:
                        pushover.Client(client).send_message(
                            message, title="Erinnerung", html=1
                        )
                    except:
                        print("No client")
    except (StopIteration, mechanize._mechanize.LinkNotFoundError) as e:
        _logger.exception("Failed to read information")
        return []
    return allinfo


if __name__ == "__main__":
    main()
