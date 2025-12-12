#!/bin/python3

"""This script generates the compose-urls-YYYYMMDD.json list of compose
URLs that is used for the test_compose_urls test.
"""

import datetime
import logging
import json

from urllib.parse import urlencode
from urllib.request import Request

import fedfind.helpers

logging.basicConfig(level=logging.DEBUG)


def datagrepper_query(topics, days):
    """Get messages on specified topics in the last X days."""
    messages = []
    secs = days * 24 * 60 * 60
    page = 1
    params = [("topic", topic) for topic in topics]
    params.extend([("delta", secs), ("page", page)])
    baseurl = "https://apps.fedoraproject.org/datagrepper/raw"
    nxt = True
    while nxt:
        url = "?".join((baseurl, urlencode(params)))
        headers = {"Content-type": "application/json"}
        req = Request(url, headers=headers)
        resp = fedfind.helpers.download_json(req)
        messages.extend(message["msg"] for message in resp["raw_messages"])
        page += 1
        params[-1] = ("page", page)
        if resp["pages"] < page:
            nxt = False
    return messages


msgs = datagrepper_query(["org.fedoraproject.prod.pungi.compose.status.change"], 180)
urls = [msg.get("location") for msg in msgs]
urls = set([url for url in urls if url])

fn = "compose-urls-{0}.json".format(datetime.date.today().strftime("%Y%m%d"))
fh = open(fn, "w")
json.dump(list(urls), fh, indent=4, separators=(",", ": "))
fh.close()
