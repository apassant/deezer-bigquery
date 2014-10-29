#!/usr/bin/env python
import os
import importlib
import re

from config import SECRET, CREDENTIALS, QUERIES, PROJECT_ID
import bigquery

if __name__ == '__main__':
    service = bigquery.build_service(SECRET, CREDENTIALS)
    for f in os.listdir('./' + QUERIES):
        if re.match('q[0-9]*\.py$', f):
            module = importlib.import_module("%s.%s" %(QUERIES, f[:-3]))
            query, title = (getattr(module, "query"), getattr(module, "title"))
            bigquery.query(service, PROJECT_ID, query, title)