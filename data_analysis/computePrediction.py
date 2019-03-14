#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 07:49:11 2017

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
logfile=output_dir+"/logs/"+"predictor_"+txn_date_log+".log"
football_feed_acquisition_date=output_dir+"/data/football_feed_acquisition_date.dat"
logging.basicConfig(filename=logfile,format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S',level=logging.DEBUG)

txn_datetime=my_utilities.read_from_file(football_feed_acquisition_date,1)
print ([txn_datetime])

logging.info(" Compute predictor : STARTED ")
mysql_populate_table.run_mysql_proc('predictor', [txn_datetime])
logging.info(" Compute predictor : COMPLETED ")
