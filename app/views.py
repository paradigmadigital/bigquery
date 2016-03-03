from flask import render_template, flash, redirect, Flask
from flask import request

import httplib2
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from unidecode import unidecode

app = Flask(__name__)

def query(where_data,cadena):
    # REPLACE WITH YOUR Project ID
    PROJECT_NUMBER = 'big-data-spain'
    # REPLACE WITH THE SERVICE ACCOUNT EMAIL FROM GOOGLE DEV CONSOLE
    SERVICE_ACCOUNT_EMAIL = '649657055739-compute@developer.gserviceaccount.com'

    # OBTAIN THE KEY FROM THE GOOGLE APIs CONSOLE
    # More instructions here: http://goo.gl/w0YA0
    #f = file('key.p12', 'rb')
    f = file('/home/ubuntu/bigquery/Big-Data-Spain-0471aefb46fe.p12','rb')
    key = f.read()
    f.close()

    credentials = SignedJwtAssertionCredentials(
        SERVICE_ACCOUNT_EMAIL,
        key,
        scope='https://www.googleapis.com/auth/bigquery')

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('bigquery', 'v2')
    datasets = service.datasets()
    jobs = service.jobs()

    #response = datasets.list(projectId=PROJECT_NUMBER).execute(http)

    #Filtramos por caracteres especiales
    #cadena = unidecode(where_data)
    #b = zip(cadena, unidecode(cadena))
    #where_ER = "".join([ "[%s%s]" % (x,y) if x!=y else x for x, y in b ])

    BODY_ARGS = {
        "timeoutMs": 42, # [Optional]
        "kind": "bigquery#queryRequest", # The resource type of the request.
        "datasetId": "big_data_spain_16", # [Required] A unique ID for this dataset, without the project name. 
        "maxResults": 42, # [Optional] 
        "query": "SELECT Event, Source, FirstName, LastName, Company, Email FROM [big-data-spain:big_data_spain_16.events_all_editons_normalize_aggregate] WHERE FirstName LIKE '%{where_data}%' OR FirstName LIKE '%{cadena}%' OR LastName LIKE '%{where_data}%' OR LastName LIKE '%{cadena}%' OR Company LIKE '%{where_data}%' OR Company LIKE '%{cadena}%' GROUP BY Event, Source, FirstName, LastName, Company, Email IGNORE CASE".format(where_data=where_data,cadena=cadena), 
  }

    #Para hacer consultas, debemos utilizar jobs
    #https://developers.google.com/resources/api-libraries/documentation/bigquery/v2/python/latest/bigquery_v2.jobs.html#get
    response = jobs.query(projectId=PROJECT_NUMBER,body=BODY_ARGS).execute(http)
    #for dataset in response['rows']:
    #  for field in dataset['f']:
    #      print '%s' % field['v']
    return response
    
@app.route('/search', methods=['GET'])
def search(where_data=None):
    return render_template('search.html', where_data=where_data)

@app.route('/result', methods=['POST'])
def result():
    where_data = request.form.get("whereData")
    cadena = unidecode(where_data)
    response = query(where_data.encode('utf-8'),cadena)
    return search(where_data=response)
    #return str(response)
    #return render_template('result',where_data=where_data)

#app.run(debug=True)
app.run(debug=False,host='0.0.0.0')

