from lxml import etree, html
from StringIO import StringIO
import requests
import logging
import uuid, time

log = logging.getLogger(__name__)

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'

def fetch(url):
    url = url.replace('http://', 'https://')
    for x in range(10):
        try:
            body = requests.get(url, 
                headers={'user-agent': UA},
                timeout=2.0,
                config={'max_retries': 10},
                verify=False)
            return body.content
        except requests.exceptions.Timeout:
            time.sleep(1)
        except Exception, e:
            logging.exception(e)
            time.sleep(1)

def fetch_stream(url):
    data = fetch(url)
    if data is None:
        return None
    return StringIO(data)

def _xml(url):
    d = fetch_stream(url)
    return etree.parse(d) if d is not None else d

def _html(url):
    d = fetch_stream(url)
    return html.parse(d) if d is not None else d

