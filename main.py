import os
import sys
import json
import base64
import re
import urllib
import urllib2
import login
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
  torrentmd.logindata['username'] = os.environ.get('MDTORRENT_LOGIN').split(':')[0]
  torrentmd.logindata['password'] = os.environ.get('MDTORRENT_LOGIN').split(':')[1]

def search(query):
    b = time.time()
    ret = []
    if have_login == True:
      torrentmd.fnd['search'] = query
      torrentmd.movie_get(torrentmd.get_data())
      # return [{"uri": magnet} for magnet in re.findall(r'magnet:\?[^\'"\s<>\[\]]+', data)]
      for l in torrentmd.found_data_list:
        if int(l['id']) in torrentmd.movie_id:
          ret.append({"uri": l['link']})
    print 'Torrentmd time: ' + str((time.time() - b))
    return ret

def search_episode(imdb_id, tvdb_id, name, season, episode):
    return search("%s S%02dE%02d" % (name, season, episode))

def search_movie(imdb_id, name, year):
    return search("%s %s" % (name, year))

have_login = torrentmd.do_login()

PAYLOAD = json.loads(base64.b64decode(sys.argv[1]))

urllib2.urlopen(
    PAYLOAD["callback_url"],
    data=json.dumps(globals()[PAYLOAD["method"]](*PAYLOAD["args"]))
)

if have_login == True:
  torrentmd.do_logout()

torrentmd.s.close()
print torrentmd.found_data_list
