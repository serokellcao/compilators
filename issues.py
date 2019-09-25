from datetime import datetime
from bs4 import BeautifulSoup
import os
import sys
import requests as r
import time
import random
import pprint

pp = pprint.PrettyPrinter(indent=2)

repos = [ 'https://github.com/elm/compiler',              # 2013-10-22 ~> 11219
          'https://github.com/ocaml/ocaml',               # 1995-09-12 ~> 48946
          'https://github.com/evincarofautumn/kitten',    # 2017-02-28 ~> 22230
          'https://github.com/MLton/mlton',               # 2001-10-07 ~> 72219
          'https://github.com/purescript/purescript',     # 2014-07-27 ~> 8154
          'https://github.com/elixir-lang/elixir',        # 2015-09-01 ~> 81305
          'https://github.com/jagajaga/syava-lang' ]      # 2016-04-20 ~> 4637

mvps0 = [ '2013-10-22',
          '1995-09-12',
          '2017-02-28',
          '2001-10-07',
          '2014-07-27',
          '2015-09-01',
          '2016-04-20' ]

def mkMvps(xs, ys):
  ret = {}
  for j,x in enumerate(xs):
    ret[os.path.basename(x)] = ys[j]
  return ret

mvps = mkMvps(repos, mvps0)

data = 'data'

def fetch(url):
  print >> sys.stderr, "Fetching " + url + "..."
  time.sleep(0.05 + random.random() / 4)
  resp = r.get(url)
  if resp.status_code == 200:
    return BeautifulSoup(resp.content, 'html.parser')
  else:
    # TODO: retry if status isn't 200
    print('GitHub is onto us!')
    raise

def provision():
  for x in repos:
    xp = os.path.join(data, os.path.basename(x))
    if not (os.path.isdir(xp)):
      os.makedirs(os.path.join(xp, 'meta'))
      os.system('git clone ' + x + ' ' + os.path.join(xp, 'compiler'))

def allIssuelike(fnPageToURLSuffix):
  ret = {}
  #for x in repos[3:4]:
  for x in repos:
    ret1 = []
    issuelike = fetch(x + fnPageToURLSuffix(1))
    #for j in range(1, 2):
    for j in range(1, pages(issuelike)):
      ret1 = ret1 + issuesInfo(fetch(x + fnPageToURLSuffix(j)))
    ret1.reverse()
    ret[(os.path.basename(x))] = ret1
  pp.pprint(ret)
  return ret

def issues(x, page):
  res = fetch(x + '/issues?page=' + str(page) + '&q=is%3Aissue+is%3Aclosed')
  return res

def pages(soup):
  pgs = soup.select('div.pagination')
  if len(pgs) > 0:
    return int(pgs[0].find_all('a')[-2].string)
  else:
    return 1

def issuesInfo(soup):
  ret = []
  for issue in soup.select('div.js-issue-row'):
    ia = issue.select('.col-8 > a')[0]
    url = 'https://github.com' + ia.get('href')
    ts1 = issue.select('.col-8 > div > span > relative-time')[0].get('datetime')
    dt1 = datetime.strptime(ts1[0:10], '%Y-%m-%d')
    #ts0 = fetch(url).select('div.TableObject-item--primary > relative-time')[0].get('datetime')
    #ts0 = fetch(url).find_all('relative-time')[0].get('datetime')
    ts0 = fetch(url).select('h3.timeline-comment-header-text > a > relative-time')[0].get('datetime')
    dt0 = datetime.strptime(ts0[0:10], '%Y-%m-%d')
    ret.append({ 'title': ia.contents[0].encode('utf-8'),
                  'url':  url,
                  'opened': ts0,
                  'closed': ts1,
                  'delta':  (dt1 - dt0).days })
  return ret

def dunpIssues(iss):
  print(iss)

def actualizePRs():
  import prs
  ret = {}
  for compiler in mvps:
    ret[compiler] = filter(lambda x: x['closed'] < u'' + mvps[compiler], prs.prs[compiler])
  return ret

if __name__ == '__main__':
  #provision()
  #allIssuelike(lambda x: '/pulls?page=' + str(x) + '&q=is%3Apr+is%3Aclosed')
  #allIssuelike(lambda x: '/issues?page=' + str(x) + '&q=is%3Aissue+is%3Aclosed')
  pp.pprint(actualizePRs())
