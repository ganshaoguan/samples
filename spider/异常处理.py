# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 11:27:14 2017

@author: dianjoy
"""

import urllib.error
import urllib.request

try:
    urllib.request.urlopen('http://www.csdn.net/')
except urllib.error.URLError as e:
    if hasattr(e, 'code'):
        print(e.code)
    if hasattr(e, 'reason'):
        print(e.reason)
except Exception as e:
	print(e)


