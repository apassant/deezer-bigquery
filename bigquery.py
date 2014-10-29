"""
Big Query helper scripts for loading and querying data
Based on samples from the official BigQuery documentation https://cloud.google.com/bigquery

The MIT License (MIT)

Copyright (c) 2014 Alexandre Passant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time
import pprint
import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools

def build_service(secret, credentials):
    """
    Build reference to a BigQuery service / API.
    
    Parameters
    ----------
    secret : string
        Path to the secret files
    credentials : string
        Path to the credentials files

    Returns
    -------
    out : object
        The service reference
    """
    flow = flow_from_clientsecrets(secret, scope="https://www.googleapis.com/auth/bigquery")
    storage = Storage(credentials)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, tools.argparser.parse_args([]))

    http = credentials.authorize(httplib2.Http())
    return build("bigquery", "v2", http=http)

def load_from_gcs(service, projectId, datasetId, tableId, data, schema):
    """
    Load data from Google Cloud Storage into BigQuery.

    Parameters
    ----------
    service : object
        The BQ service reference
    projectId : string
        The Google Cloud project ID
    datasetId : string
        The BQ dataset ID
    tableId : string
        The BQ table ID
    data : list(string)
        The data sources, as list of URIs
    schema : dict
        The JSON schema used to map JSON to BQ tables

    Returns
    -------
    out : bool
        Success / Failure

    """
    try:
        jobCollection = service.jobs()
        jobData = {
            "projectId": projectId,
            "configuration": {
                "load": {
                    "sourceUris": data,
                    "sourceFormat" : "NEWLINE_DELIMITED_JSON",
                    "ignoreUnknownValues" : True,
                    "schema": schema,
                    "destinationTable": {
                        "projectId": projectId,
                        "datasetId": datasetId,
                        "tableId": tableId
                    },
                }
            }
        }
        insertResponse = jobCollection.insert(projectId=projectId, body=jobData).execute()

        # Ping for status until it is done, with a short pause between calls.
        while True:
            job = jobCollection.get(projectId=projectId, jobId=insertResponse["jobReference"]["jobId"]).execute()
            if "DONE" == job["status"]["state"]:
                print "Done Loading!"
                return True
            print "Waiting for loading to complete..."
            time.sleep(10)

        if "errorResult" in job["status"]:
            print "Error loading table: ", pprint.pprint(job)
            return False

    except Exception as err:
        print "Error in loadTable: ", pprint.pprint(err)
        return False
        
        
def query(service, projectId, query, title=False):
    """
    Run a SQL query on BigQuery service.
    
    Parameters
    ----------
    service : object
        The BQ service reference
    projectId : string
        The Google Cloud project ID
    query : string
        The query (SQL)
    title : string (optional)
        The query title
    """
    response = service.jobs().query(projectId=projectId, body={ 
        'query': query
    }).execute()
    if title:
        print "\n###\t{title}".format(**{
            'title' : title
        })
    print response
    for row in response['rows']:
        print ('\t').join([field['v'] for field in row['f']])