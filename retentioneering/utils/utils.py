import json
from google.cloud import bigquery


class Config(dict):
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            super(Config, self).__init__(json.load(f))

    def export(self, filename):
        with open(filename, 'wb') as f:
            json.dump(self, f)


def init_from_json(filename):
    settings = Config(filename)
    client = bigquery.Client.from_service_account_json(
        settings['settings']['service_account_path'],
        project=settings['settings']['project'])
    job_config = bigquery.QueryJobConfig()
    job_config.use_legacy_sql = True
    job_config.allow_large_results = True
    job_config.write_disposition = "WRITE_TRUNCATE"
    job_config.destination = client.dataset(settings['sql'].values()[0]['destination_table']['dataset']) \
        .table(settings['sql'].values()[0]['destination_table']['table'])

    return client, job_config
