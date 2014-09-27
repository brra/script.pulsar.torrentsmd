#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import gzip
from StringIO import StringIO
import requests
import re, glob
from time import sleep

from bs4 import BeautifulSoup

path = os.getcwd()

# for l in glob.glob(path+'/*.html'):
    # os.remove(l)

try:
    import xbmc
    run_from_xbmc = True
except ImportError:
    run_from_xbmc = False
    pass

movie_id = [31,28,5,35,19,24,20,7,33]
logindata = {'username' : '',
              'password' : ''}
fnd = {
  'search' : '',
  'cat' : '0',
  'incldead' : '1',
  'in' : 'name'}

user_agent = {"Host" : "zelka.org",
  "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0"}

found_data_list = []
s = requests.Session()
def savetofile(d, name):
  if run_from_xbmc == False:
    n = os.path.join(path, name)
    f = open(n, 'wb')
    f.write(d)
    f.close

def movie_get(data):
  s = BeautifulSoup(data)
  for link in s.findAll('a', href=re.compile(r'magnet:\?xt=.*')):
    found_data_list.append({
      'id': link.find_parent('td').find_previous_sibling('td').find('a', href=re.compile(r'browse\.php\?cat=\d+'))['href'].split('=')[1],
      # 'name': link.find_previous_sibling('a', href=re.compile(r'details\.php\?id=.*')).string,
      'link': link['href'],
      })

def do_login():
  r = s.post('http://www.torrentsmd.com/login.php', data=logindata, headers = user_agent)
  if re.search(logindata['username'], r.text, re.IGNORECASE):
    #have a login
    return True

def do_logout():
  r = s.post('http://www.torrentsmd.com/logout.php', data=logindata, headers = user_agent)

def get_data():
  text = ''
  r = s.get('http://www.torrentsmd.com/browse.php', params=fnd, headers = user_agent)
  savetofile(r.text.encode('windows-1251'), 'tmp1.1.html')
  text = r.text.encode('windows-1251')
  #r = s.get('http://zelka.org/browse.php?cat=31', headers = user_agent)
  #savetofile(r.text.encode('windows-1251'), 'tmp1.2.html')
  r = s.get('http://www.torrentsmd.com/logout.php', headers = user_agent)
  return text

if __name__ == "__main__":
  if True == os.environ.has_key('MDTORRENT_LOGIN'):
    logindata['username'] = os.environ.get('MDTORRENT_LOGIN').split(':')[0]
    logindata['password'] = os.environ.get('MDTORRENT_LOGIN').split(':')[1]
  cnt = len(sys.argv)
  have_login = False
  if cnt == 2:
    fnd['search'] = sys.argv[1]
    have_login = do_login()
    dat = get_data()
  elif cnt == 1:
    print 'use file'
    f = open('tmp1.1.html', 'rb')
    dat = f.read()
    f.close()

  movie_get(dat)

  for l in found_data_list:
    if int(l['id']) in movie_id:
      print l['id']
      #print l['name']
      print l['link']

  if have_login == True:
    do_logout()

  sys.exit(0)
