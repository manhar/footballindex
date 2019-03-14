#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 08:30:33 2017

@author: ashish
"""

import os, sys, inspect , linecache


#function to write data to a file
def write_to_file(file_name, data):
    result=False
    try:
        with open(file_name, 'w') as datafile:
                datafile.write(data)
                result=True
        datafile.close()
    except Exception as e :
        print("Error while writing to file "+str(e))
    return result

#function to read from a file
def read_from_file(file_name, line_to_read):
    line=""
    try:
        line = linecache.getline(file_name, line_to_read ).rstrip()
        #print(line)
    except Exception as e :
        print("Error while reading to file "+str(e))
    return line

