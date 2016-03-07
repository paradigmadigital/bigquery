from flask import render_template, request, Flask, Response, redirect, url_for
from unidecode import unidecode

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials

from auth import requires_auth

app = Flask(__name__)


def query(search_term):

    credentials = GoogleCredentials.get_application_default()
    bigquery_service = build('bigquery', 'v2', credentials=credentials)

    try:
        query_request = bigquery_service.jobs()
        query_data = {
            'query': (
                "SELECT Event, Source, FirstName, LastName, Company, Email"
                " FROM [big-data-spain:big_data_spain_16.events_all_editons_normalize_aggregate]"
                " WHERE FirstName LIKE '%{search_term}%'"
                " OR LastName LIKE '%{search_term}%'"
                " OR Company LIKE '%{search_term}%'"
                " GROUP BY Event, Source, FirstName, LastName, Company, Email IGNORE CASE".format(search_term=search_term))
        }

        query_response = query_request.query(projectId='big-data-spain', body=query_data).execute()

    except HttpError as err:
        print('Error: {}'.format(err.content))
        raise err

    return query_response


@app.route('/', methods=['GET'])
@requires_auth
def search():
    return render_template('search.html')


@app.route('/', methods=['POST'])
@requires_auth
def result():
    search_term = unidecode(request.form.get("search_term")).strip()

    if search_term and len(search_term) > 2:
        results = query(search_term)
    else:
        results = None

    return render_template('search.html', results=results, search_term=search_term)


@app.route('/csv', methods=['GET'])
@requires_auth
def download_csv():
    search_term = request.args.get("search_term")

    if search_term:
        results = query(search_term)
    else:
        return redirect(url_for('search'))

    csv = 'Event;Source;FirstName;LastName;Company;Email\n'

    for row in results.get('rows', {}):
        csv += ';'.join([field['v'] if field['v'] is not None else '' for field in row['f']])
        csv += '\n'

    response = Response(csv,
                        mimetype="text/csv",
                        headers={"Content-disposition": "attachment; filename=export.csv"})
    return response

if __name__ == "__main__":
    app.run(debug=True)

