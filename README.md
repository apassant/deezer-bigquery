Insights from 500,000 Deezer playlists using Google’s BigQuery
==============================================================

* http://apassant.net/2014/10/27/500000-deezer-playlists-google-big-query
* This repo contains the various scripts used to run the experiment
* Dataset is split into 9 JSON files (About 1Go total) at http://storage.googleapis.com/deezer-playlists/[1-9].json.gz
* Data comes from the Deezer API. By using it, you agree to the Deezer API TOS at http://developers.deezer.com/api
* I'm making it available publicly for experimental purposes. If you're a Deezer representative and want it to be removed, please contact me at http://apassant.net

Replicate the experiment
------------------------

### Setting-up your environment
- Create a Google Cloud project
- Set-up your authorization details using https://cloud.google.com/bigquery/authorization#clientsecrets
- Setup BigQuery for your Google Cloud project
- Copy `config.py.dist` into `config.py` and edit your project details

### Loading the dataset
- Run `load.py` and accept the oAuth screen (this will create a `bigquery_credentials.dat` file)
- Wait until it loads all JSON files from Google Cloud Storage into your Big Query project

### Querying the dataset
- Run query.py to query the dataset
- Add additional queries by creating new files in `/queries`