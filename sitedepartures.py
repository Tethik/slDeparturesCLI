#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import httplib2
import pickle, os
import conf

class SiteDeparture:	
	
	namespace = '{http://www1.sl.se/realtidws/}' 
	
	def _CreateDeparture(self, xmlObj):
		return {
				"Type": xmlObj.tag.replace(self.namespace, ''),
				"Name": xmlObj.find("{0}LineNumber".format(self.namespace)).text,			
				"Destination": xmlObj.find("{0}Destination".format(self.namespace)).text,	
				"ExpectedDateTime": xmlObj.find("{0}ExpectedDateTime".format(self.namespace)).text,
				"DisplayTime": xmlObj.find("{0}DisplayTime".format(self.namespace)).text,
		};

	def GetDepartures(self, siteId):		
		departures = list()
		h = httplib2.Http()
		url = "https://api.trafiklab.se/sl/realtid/GetDpsDepartures?siteId="+str(siteId)+"&key="+conf.__API_KEY__
		resp, content = h.request(url)		
		tree = ET.fromstring(content)		
		for bus in tree.findall("{0}Buses/{0}DpsBus".format(self.namespace)):
			departures.append(self._CreateDeparture(bus))
			
		for tram in tree.findall("{0}Trams/{0}DpsTram".format(self.namespace)):
			departures.append(self._CreateDeparture(tram))
		
		for metro in tree.findall("{0}Metros/{0}DpsMetro".format(self.namespace)):
			departures.append(self._CreateDeparture(metro))
			
		for train in tree.findall("{0}Train/{0}DpsTrain".format(self.namespace)):
			departures.append(self._CreateDeparture(train))
				
		return departures

def test():
	s = SiteDeparture()
	departures = s.GetDepartures(9192)
	for dep in departures:
		print dep

#test()
