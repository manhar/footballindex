#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 09:24:36 2017

@author: ashish
"""


import sys
sys.path.insert(0, '../utilities')
import add_subdir_to_path , my_utilities
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

txn_date_log=datetime.today().strftime('%Y%m%d')
logfile=output_dir+"/logs/"+"predictor_backfill"+txn_date_log+".log"
football_feed_acquisition_date=output_dir+"/data/football_feed_acquisition_date.dat"
logging.basicConfig(filename=logfile,format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S',level=logging.DEBUG)

txn_datetime=my_utilities.read_from_file(football_feed_acquisition_date,1)
print ([txn_datetime])

#txn_datetime= '2017-05-01 00:00:00'
txn_datetime= '2017-05-07 02:33:38'

start_date='2017-05-27 09:12:00'

while txn_datetime <= start_date :
    print(txn_datetime)
    mysql_populate_table.run_mysql_proc('predictor_backfill', [txn_datetime])
    txn_datetime=(datetime.strptime(txn_datetime, '%Y-%m-%d %H:%M:%S')  + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')

