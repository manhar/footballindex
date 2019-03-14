import sys
sys.path.insert(0, '../utilities')
import add_subdir_to_path
import mysql_populate_table
import my_config
import datetime
import logging
from datetime import datetime, timedelta
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 04:18:09 2017
This script is a robot player and is responsible for buying/selling players from a portfolio depending on the indication receieved from predictor
@author: ashish
"""

#declare output directory
output_dir=my_config.ConfigSectionMap("logging")['output_dir']

    #Set variables

txn_date=datetime.today().strftime('%Y%m%d')
logfile=output_dir+"/logs/"+"robotplayer1"+txn_date+".log"
logging.basicConfig(filename=logfile,format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S',level=logging.DEBUG)


logging.info(" RobotPlayer1 : STARTED ")
#compute prediction
x=mysql_populate_table.run_mysql_proc_output('predictor')
#get predictor indication
print (type(x))


logging.info(" RobotPlayer1 : COMPLETED ")
