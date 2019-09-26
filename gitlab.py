from datetime import datetime
from bs4 import BeautifulSoup
import os
import sys
import requests as r
from subprocess import check_output
import time
import random
import pprint

pp = pprint.PrettyPrinter(indent=2)

repos = [ 'https://gitlab.com/morley-framework/morley' ]      # 2019-08-14 ~> 20558

mvps0 = [ '2019-10-22' ]

def mkMvps(xs, ys):
  ret = {}
  for j,x in enumerate(xs):
    ret[os.path.basename(x)] = ys[j]
  return ret

mvps = mkMvps(repos, mvps0)

data = 'data'

# TODO lawls, fetch also turns out to be a parameter
def fetch(url):
  print >> sys.stderr, "Fetching " + url + "..."
  return BeautifulSoup(check_output(["sh", "./scrape.sh", url, "2>/dev/null"], stderr=None),
                       'html.parser')

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
  return ret

def issues(x, page):
  res = fetch(x + '/issues?page=' + str(page) + '&q=is%3Aissue+is%3Aclosed')
  return res

# TODO: move pages function into gitlab/hub dependent file,
# determine which pages function to use based on URL.
def pages(soup):
  pgs = soup.select('.page-link')
  if len(pgs) > 0:
    return int(pgs[-2].string)
  else:
    return 1

# TODO: see pages
def issuesInfo(soup):
  ret = []
  for issue in soup.select('.issuable-info-container'):
    ia = issue.select('div > div > span > a')[0]
    url = 'https://gitlab.com' + ia.get('href')
    ts0 = issue.select('div > div > span > time')[0].get('datetime')
    dt0 = datetime.strptime(ts0[0:10], '%Y-%m-%d')
    ts1 = fetch(url).select('.js-mr-widget-author > time')[0].get('data-original-title')
    dt1 = datetime.strptime(ts1[0:-9], '%b %d, %Y %H:%M%p')
    ret.append({ 'title': ia.contents[0].encode('utf-8'),
                  'url':  url,
                  'opened': ts0,
                  'closed': ts1,
                  'delta':  (dt1 - dt0).days })
  return ret

def dunpIssues(iss):
  print(iss)

def actualizeIssuelike(issuelikeDict):
  ret = {}
  for compiler in mvps:
    ret[compiler] = filter(lambda x: x['closed'] < u'' + mvps[compiler], issuelikeDict[compiler])
  return ret

if __name__ == '__main__':
  #import prs
  #import issues
  #provision()
  ret = allIssuelike(lambda page: '/merge_requests?page=' + str(page) + '&scope=all&state=merged')
  pp.pprint(ret)
  #allIssuelike(lambda x: '/issues?page=' + str(x) + '&q=is%3Aissue+is%3Aclosed')
  #pp.pprint(actualizeIssuelike(prs.prs))
  #pp.pprint(actualizeIssuelike(issues.issues))
