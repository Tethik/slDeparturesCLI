#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import httplib2
import pickle, os
import conf
import re
import datetime
import time
from datetime import datetime, timedelta


class SiteDeparture:	
	
	namespace = '{http://www1.sl.se/realtidws/}' 
	
	def _ParseDisplayRow(self, row, groupOfLine):			
		cols = row.split(" ")
		#print cols		
		num = int(cols[0])
		dest = cols[1]
		if len(dest) <= 1:
			dest = cols[2]
		displaytime = ' '.join(cols[-2:])
		#print cols[-2]		
		expectedtime = datetime.now() 
		if cols[-2] != "Kort":
			expectedtime += timedelta(minutes=int(cols[-2]))
		
		#pattern = "([0-9]+) ([A-ö\\.]+) ([0-9]+ min|Kort tåg\\.)"
		#m = re.search(pattern, row)
		#print m.groups(0)		
		#print m
		
		return {
				"Type": "DpsMetro",
				"Name": groupOfLine + " " + str(num),				
				"Destination": dest,
				"DisplayTime": displaytime,
				"ExpectedDateTime": expectedtime.strftime("%Y-%m-%dT%X")
		}
	
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
		#print url
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
			
		
		departures += self.GetMetroDepartures(siteId)
		#print departures
		return departures
		
	def GetMetroDepartures(self, siteId):		
		departures = list()
		# I have to use the old api for the metro lines..	
		oldUrl = "https://api.trafiklab.se/sl/realtid/GetDepartures?siteId="+str(siteId)+"&key="+conf.__API_KEY__
		h = httplib2.Http()
		resp, content = h.request(oldUrl)		
		tree = ET.fromstring(content)
		for metro in tree.findall("{0}Metros/{0}Metro".format(self.namespace)):			
			groupOfLine = metro.find("{0}GroupOfLine".format(self.namespace)).text.split(" ")[1]
			departures.append(self._ParseDisplayRow(metro.find("{0}DisplayRow1".format(self.namespace)).text, groupOfLine))
			displayRow2 = metro.find("{0}DisplayRow2".format(self.namespace)).text
			if displayRow2:
				for row in displayRow2.split(","):
					try:
						departures.append(self._ParseDisplayRow(row, groupOfLine))	
					except:
						pass # sue me
		return departures

def test():
	s = SiteDeparture()
	departures = s.GetDepartures(9192)
	for dep in departures:
		print dep

#test()
