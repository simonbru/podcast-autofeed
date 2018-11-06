#!/usr/bin/env python

import os
import urllib.parse
from email.utils import formatdate
from hashlib import md5
from pathlib import Path

import bottle


BASE_URL = os.environ['BASE_URL']
PODCAST_DIR = os.environ['PODCAST_DIR']

app = bottle.Bottle()

FEED_TPL = """\
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="stylesheet.xsl" ?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>Symen autofeed</title>
    <description>Automatically generated feed</description>
    <link>{{link}}</link>
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


@app.get('/feed', name="feed")
def view_feed():
    items = []
    files = (
        file for file in 
        Path(PODCAST_DIR).glob('*.*')
        if file.is_file() and not file.name.startswith('.')
    )
    sorted_files = sorted(
        files, reverse=True, key=lambda it: it.stat().st_mtime
    )
    for file in sorted_files:
        item = {}
        stat = file.stat()
        hash = md5(
            (file.name + str(stat.st_size)).encode()
        )
        item['guid'] = hash.hexdigest()
        item['title'] = file.name
        item['desc'] = ''
        item['pub_date'] = formatdate(stat.st_mtime)
        quoted_name = urllib.parse.quote(file.name)
        static_path = app.get_url("static", path=quoted_name)
        item['file_url'] = BASE_URL + static_path
        item['file_size'] = stat.st_size
        items.append(item)
    bottle.response.set_header(
        "Content-Type", "text/xml; charset=utf-8"
    )
    static_url = BASE_URL + app.get_url("static", path="")
    return bottle.template(
        FEED_TPL, link=static_url, items=items
    )


@app.get('/stylesheet.xsl', name="stylesheet")
def view_stylesheet():
    return bottle.static_file('stylesheet.xsl', str(Path(__file__).parent))


@app.get('/<path:path>', name="static")
def view_static(path):
    return bottle.static_file(path, root=PODCAST_DIR)


application = app.wsgi
if __name__ == '__main__':
    app.run(host='::', port=8006, debug=True, reloader=True)
