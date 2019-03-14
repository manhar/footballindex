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
This script is responsible for calling stored procedure in mySQL DB
@author: ashish
"""

#declare output directory
output_dir=my_config.ConfigSectionMap("logging")['output_dir']

    #Set variables

txn_date=datetime.today().strftime('%Y%m%d')
logfile=output_dir+"/logs/"+"computePlayerStats_"+txn_date+".log"
logging.basicConfig(filename=logfile,format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S',level=logging.DEBUG)


logging.info(" Compute Player stats : STARTED ")
mysql_populate_table.run_mysql_proc('computePlayerStats')
logging.info(" Compute Player stats : COMPLETED ")
