#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plot
plot.style.use('seaborn-whitegrid')
import numpy as np

import mvpissues

issues = mvpissues.issues
issues['morley'] = []

import gitlabprs
import mvpprs
import pprint

prs = mvpprs.prs
prs['morley'] = gitlabprs.prs['morley']

pp = pprint.PrettyPrinter(indent=2)

def mkFreqs(points, selector):
  if len(points) == 0:
    return []
  freqs = {}
  for x in points:
    s = selector(x)
    if s in freqs:
      freqs[s] = freqs[s] + 1
    else:
      freqs[s] = 1
  return sorted(freqs.items(), key=lambda kv: kv[0])

def mkAllFreqs(xs, selector):
  allFreqs = {}
  for points in xs:
    allFreqs[points] = mkFreqs(xs[points], selector)
  return allFreqs

def sortByFrequency(freqs):
  return sorted(freqs, key=lambda kv: kv[1])

def unzip(xs):
  ret = [[],[]]
  for j in xs:
    ret[0].append(j[0])
    ret[1].append(j[1])
  return ret

def render(x, y, xlabel, ylabel, title):
  if(len(x) == 0):
    return
  if(len(y) == 0):
    return
  _fig, ax = plot.subplots()
  ax.set_xticks(x)
  plot.plot(x, y, 'ro')
  plot.title(title)
  plot.xlabel(xlabel)
  plot.ylabel(ylabel)
  plot.show()

def filterRelevantIssues(points):
  return filter(lambda x: x[0] <= 3*30 and x[0] >= 2, points)
def filterRelevantPrs(points):
  return filter(lambda x: x[0] <= 3*30, points)

def groupByDelta(points):
  def getSndByFst(x, ys):
    for y in ys:
      if y[0] == x:
        return y[1]
    return 0
  ret = []
  prev = -1 
  for curr in [0,1,2,3,4,5,10,20,30,40,60,90]:
    occurrences = 0
    for j in range(prev + 1, curr + 1):
      occurrences = occurrences + getSndByFst(j, points)
    if occurrences > 0:
      if curr == prev + 1:
        ret.append([str(curr), occurrences])
      else:
        ret.append([str(prev + 1) + '-' + str(curr), occurrences])
    prev = curr
  return ret

if __name__ == '__main__':
  allIssuesByDelta = mkAllFreqs(issues, lambda x: x['delta'])
  allPrsByDelta = mkAllFreqs(prs, lambda x: x['delta'])
  for compiler in allIssuesByDelta:
    #xy = unzip(filterRelevantIssues(allIssuesByDelta[compiler]))
    xy = unzip(groupByDelta(filterRelevantIssues(allIssuesByDelta[compiler])))
    #render(xy[1], xy[0], 'amount of issues closed', 'days', compiler + u' issues (ν)')
    #xy1 = unzip(filterRelevantPrs(allPrsByDelta[compiler]))
    xy1 = unzip(groupByDelta(filterRelevantPrs(allPrsByDelta[compiler])))
    render(xy1[1], xy1[0], 'amount of PRs closed', 'days', compiler + u' pull requests (ν)')
