#!/usr/bin/env python
from config import SECRET, CREDENTIALS, PROJECT_ID, DATASET_ID, TABLE_ID, DATA, SCHEMA
import bigquery

if __name__ == "__main__":
    service = bigquery.build_service(SECRET, CREDENTIALS)    
    bigquery.load_from_gcs(service, PROJECT_ID, DATASET_ID, TABLE_ID, DATA, SCHEMA)
