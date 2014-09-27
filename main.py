import os
import sys
import json
import base64
import re
import urllib
import urllib2
import zelka
import time

try:
  import xbmcaddon
  run_from_xbmc = True
except ImportError:
  os.environ['no_proxy'] = '127.0.0.1,localhost'
  run_from_xbmc = False
  pass

if True == run_from_xbmc:
  __addon_id__= 'script.pulsar.torrentmd'
  __Addon = xbmcaddon.Addon(__addon_id__)
  torrentmd.logindata['username'] = __Addon.getSetting('usr')
  torrentmd.logindata['password'] = __Addon.getSetting('pass')
else:
  torrentmd.logindata['username'] = os.environ.get('_LOGIN').split(':')[0]
  torrentmd.logindata['password'] = os.environ.get('ZELKA_LOGIN').split(':')[1]

PAYLOAD = json.loads(base64.b64decode(sys.argv[1]))

def search(query):
    response = urllib2.urlopen("http://www.torrentsmd.com/search.php?search_str=%s" % urllib.quote_plus(query))
    data = response.read()
    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)]


def search_episode(imdb_id, tvdb_id, name, season, episode):
    return search("%s S%02dE%02d" % (name, season, episode))


def search_movie(imdb_id, name, year):
    return search(imdb_id)

urllib2.urlopen(
    PAYLOAD["callback_url"],
    data=json.dumps(globals()[PAYLOAD["method"]](*PAYLOAD["args"]))
)
