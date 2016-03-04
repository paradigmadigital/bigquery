#!/usr/bin/python
import sys
import logging
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/var/www/bigquery/big-data-spain_9ac768329273.json'
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/bigquery/")

from bigquery.app import app as application
#application.secret_key = 'Add your secret key'
