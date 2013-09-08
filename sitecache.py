#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: UTF-8

import xml.etree.ElementTree as ET
import httplib2
import pickle, os, gflags
import conf


gflags.DEFINE_bool("verbose", False, "Prints debug messages")
gflags.DEFINE_bool("clearcache", False, "Clear cache for station lookup")

'''
A cache to reduce GetSite-calls to the api. 
'''
class SiteCache:	
	namespace = '{http://www1.sl.se/realtidws/}'

	def __init__(self):
		self.vals = dict()
		if gflags.FLAGS.clearcache:
			self.saveCache() # should clear by overwriting with empty..
		self.loadCache();

	def _ApiCall(self, searchVal):
		if gflags.FLAGS.verbose:
			print "Searching for {0}".format(searchVal)
		h = httplib2.Http(".cache")
		resp, content = h.request("https://api.trafiklab.se/sl/realtid/GetSite?stationSearch="+searchVal+"&key="+conf.__API_KEY__, "GET")		
		if gflags.FLAGS.verbose:
			print content
		tree = ET.fromstring(content)		
		number = -1
		for site in tree.findall("{0}Sites/{0}Site".format(self.namespace)):			
			number = int(site.find("{0}Number".format(self.namespace)).text)
			name = site.find("{0}Name".format(self.namespace)).text		
			self.vals[name] = number
		return number			

	def GetSiteId(self, searchVal):
		if searchVal in self.vals:
			return self.vals[searchVal]
		val = self._ApiCall(searchVal)
		self.vals[searchVal] = val
		self.saveCache()
		return val
		
	def saveCache(self):		
		if not os.path.exists(conf.__SITECACHE_DIR__):
			os.mkdir(conf.__SITECACHE_DIR__)
		cacheFile = open(conf.__SITECACHE_FILE__, 'w')
		pickle.dump(self, cacheFile)
		cacheFile.close()

	def loadCache(self):
		if not os.path.exists(conf.__SITECACHE_FILE__):	
			print "no cachefile found"
			return
		cacheFile = open(conf.__SITECACHE_FILE__, 'r')
		cache = pickle.load(cacheFile)
		cacheFile.close()
		self.__dict__ = cache.__dict__
	
def test():
	s = SiteCache()
	v = s.GetSiteId('Stadshagen')
	print v

#test()
