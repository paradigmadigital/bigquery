#!/usr/bin/python
import sys
import logging
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/var/www/bigquery/big-data-spain_9ac768329273.json'
os.environ['AUTH_USER'] = 'bds'
os.environ['AUTH_PASS'] = 'bdspass'

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/bigquery/")

from bigquery.app import app as application

