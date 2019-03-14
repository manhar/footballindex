#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 09:46:48 2017

@author: ashish
"""

import http.client
import json

football_data_api_token='2da2be90ffb14373b360d92dd283d2e8'
http_header='X-Auth-Token'

connection = http.client.HTTPConnection('api.football-data.org')
headers = { http_header: football_data_api_token, 'X-Response-Control': 'minified' }
connection.request('GET', '/v1/competitions', None, headers )
response = json.loads(connection.getresponse().read().decode())

print (response)