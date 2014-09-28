import sys
import json
import base64
import re
import urllib
import urllib2
import xbmcaddon
import xbmcplugin
import xbmc
__addon__ = xbmcaddon.Addon(str(sys.argv[0]))
__proxy__ = __addon__.getSetting("url_proxy")
__user__ = __addon__.getSetting("user")
__password__ = __addon__.getSetting("password")

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
opener.open('__proxy__')

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
