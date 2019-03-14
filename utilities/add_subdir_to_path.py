#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:47:44 2017

@author: ashish
This function allows us to add all subdirectories to sys.path
"""



import os, sys, inspect , linecache


# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
cmd_folder=cmd_folder.replace('utilities','')
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
        if os.path.isdir(os.path.join(a_dir, name))]

sub_dir=get_immediate_subdirectories(cmd_folder)
for folder in sub_dir:
    # use this if you want to include modules from a subfolder
    cmd_subfolder = cmd_folder+folder
    #os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],folder)))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)


