from google.cloud import bigquery_datatransfer
import google.auth
import pandas as pd

class BigQuery:

    '''
    ref: https://cloud.google.com/bigquery/docs/scheduling-queries#python_3
    '''

    def __init__(self):
        credentials, project = google.auth.default()
        self.transfer_client = bigquery_datatransfer.DataTransferServiceClient(credentials=credentials)
        # Initialize request argument(s)

    ## Create method to read query and output the result in pandas df
    def read_query_to_df(self, query, project_id):
        df = pd.read_gbq(query, project_id)
        return df