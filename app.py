import requests
import json
import threading
from socket import gaierror, gethostbyname
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urlparse
from flask import Flask, render_template, jsonify
from time import gmtime, strftime

from settings import refresh_interval, filename, site_down


def is_reachable(url):
    """ This function checks to see if a host name has a DNS entry
    by checking for socket info."""
    try:
        gethostbyname(url)
    except (gaierror):
        return False
    else:
        return True


def get_status_code(url):
	""" This function returns the status code of the url."""
	try:
	    status_code = requests.get(url, timeout=30).status_code
	    return status_code
	except requests.ConnectionError:
	    return site_down


def check_single_url(url):
    """This function checks a single url and if connectable returns
    the status code, else returns UNREACHABLE."""
    if is_reachable(urlparse(url).hostname) == True:
        return str(get_status_code(url))
    else:
        return site_down


def check_multiple_urls():
    """ This function checks through urls specified in the checkurls.json file
    and returns their statuses as a dictionary every 60s."""
    statuses = {}
    temp_list_urls = []
    temp_list_statuses = []
    global returned_statuses
    global last_update_time
    t = threading.Timer
    t(refresh_interval, check_multiple_urls).start()
    for group, urls in checkurls.items():
        for url in urls:
            temp_list_urls.append(url)
    pool = ThreadPool(8)
    temp_list_statuses = pool.map(check_single_url, temp_list_urls)
    for i in range(len(temp_list_urls)):
        statuses[temp_list_urls[i]] = temp_list_statuses[i]
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


with open(filename) as f:
    checkurls = json.load(f)
returned_statuses = {}
last_update_time = 'time string'


if __name__ == '__main__':
    check_multiple_urls()
    app.run()
