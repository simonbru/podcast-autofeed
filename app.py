#!/usr/bin/env python

import os
import urllib.parse
from email.utils import formatdate
from hashlib import md5
from pathlib import Path

import bottle


STATIC_URL = os.environ['STATIC_URL']
PODCAST_DIR = os.environ['PODCAST_DIR']

app = bottle.Bottle()

FEED_TPL = """\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>Symen autofeed</title>
    <description>Automatically fenerated feed</description>
    <link>{{base_url}}</link>
    % for item in items:
    <item>
        <title>{{item['title']}}</title>
        <description>{{item['desc']}}</description>
        <pubDate>{{item['pub_date']}}</pubDate>
        <enclosure url="{{item['file_url']}}"
                    % # type="audio/mpeg"
                    length="{{item['file_size']}}"
        />
        % # <itunes:duration></itunes:duration>
        <guid isPermaLink="false">{{item['guid']}}</guid>
    </item>
    % end
  </channel>
</rss>
"""


@app.get('/feed')
def view_feed():
    items = []
    files = (
        file for file in 
        Path(PODCAST_DIR).glob('*.*')
        if file.is_file() and not file.name.startswith('.')
    )
    for file in files:
        item = {}
        stat = file.stat()
        hash = md5(
            (file.name + str(stat.st_size)).encode()
        )
        item['guid'] = hash.hexdigest()
        item['title'] = file.name
        desc = ''
        item['pub_date'] = formatdate(stat.st_mtime)
        escaped_name = urllib.parse.quote(file.name)
        item['file_url'] = f"{STATIC_URL}/{escaped_name}"
        item['file_size'] = stat.st_size
        items.append(item)
    bottle.response.set_header(
        "Content-Type", "text/xml; charset=utf-8"
    )
    return bottle.template(
        FEED_TPL, base_url=STATIC_URL, items=items
    )


@app.get('/<path:path>')
def view_static(path):
    return bottle.static_file(path, root=PODCAST_DIR)


app.run(host='::', port=8006, debug=True, reloader=True)
