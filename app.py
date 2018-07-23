import requests
import json
import threading

from multiprocessing.dummy import Pool as ThreadPool
from socket import gethostbyname, gaierror
from urllib.parse import urlparse
from flask import Flask, render_template, jsonify
from time import gmtime, strftime

def has_dns(url):
    """ This function checks to see if a host name has a DNS entry
    by checking for socket info. """
    try:
        gethostbyname(url)
    except gaierror:
        return False
    else:
        return True

def get_status_code(url):
	""" This function returns the status code of the url. """
	status_code = requests.get(url).status_code
	return status_code

def check_single_url(url):
    """This function checks a single url and if connectable returns
    the status code, else returns UNREACHABLE"""
    if has_dns(urlparse(url).hostname) == True:
        return str(get_status_code(url))
    else:
        return 'UNREACHABLE'

def check_multiple_urls():
    """ This function checks through urls specified in the checkurls.json file
    and returns their statuses as a dictionary every 60s."""
    statuses = {}
    list_urls = []
    list_statuses = []
    global returned_statuses
    global last_update_time
    t = threading.Timer
    t(60.0, check_multiple_urls).start()
    for group, urls in checkurls.items():
        for url in urls:
            list_urls.append(url)
    pool = ThreadPool(8)
    list_statuses = pool.map(check_single_url, list_urls)
    for i in range(len(list_urls)):
        statuses[list_urls[i]] = list_statuses[i]
    last_update_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    returned_statuses = statuses

app = Flask(__name__)

@app.route("/", methods=["GET"])
def display_returned_statuses():
    return render_template(
        'returned_statuses.html',
        returned_statuses = returned_statuses,
        checkurls = checkurls,
        last_update_time = last_update_time
        )
        
@app.route("/api", methods=["GET"])
def display_returned_api():
    return jsonify(
        returned_statuses
        ),200

filename = 'checkurls.json'
with open(filename) as f:
    checkurls = json.load(f)

returned_statuses = {}
last_update_time = 'time string'

if __name__ == '__main__':
    check_multiple_urls()
    app.run()
    