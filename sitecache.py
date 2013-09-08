import xml.etree.ElementTree as ET
import httplib2
import pickle, os


__API_KEY__ = 'ace842059e54f0d2f21512c4bb4465b0'
__SITECACHE_FILE__ = os.path.expanduser('~/.slDeparturesCLI/.sitecache')
__SITECACHE_DIR__ = os.path.expanduser('~/.slDeparturesCLI')

'''
A cache to reduce GetSite-calls to the api. 
'''
class SiteCache:	
	def __init__(self):
		self.vals = dict()
		self.loadCache();

	def _ApiCall(self, searchVal):
		h = httplib2.Http(".cache")
		resp, content = h.request("https://api.trafiklab.se/sl/realtid/GetSite?stationSearch="+searchVal+"&key="+__API_KEY__, "GET")
		print content
		tree = ET.fromstring(content)
		number = -1
		for site in tree[1]:
			print site.tag
			name = site.find('Name').text
			number = int(site.find('Number').text)
			self.vals[name] = number
		self.saveCache()
		return number
			

	def GetSiteId(self, searchVal):
		if searchVal in self.vals:
			return self.vals[searchVal]
		val = self._ApiCall(searchVal)
		self.vals[searchVal] = val
		return val
		
	def saveCache(self):		
		if not os.path.exists(__SITECACHE_DIR__):
			os.mkdir(__SITECACHE_DIR__)
		cacheFile = open(__SITECACHE_FILE__, 'w')
		pickle.dump(self, cacheFile)
		cacheFile.close()

	def loadCache(self):
		if not os.path.exists(__SITECACHE_FILE__):			
			return
		cacheFile = open(__SITECACHE_FILE__, 'r')
		cache = pickle.load(cacheFile)
		cacheFile.close()
		self.__dict__ = cache.__dict__
	
def test():
	s = SiteCache()
	v = s.GetSiteId('Stadshagen')
	print v

test()
