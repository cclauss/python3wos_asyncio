#!/usr/bin/env python

# See: https://github.com/GoogleCloudPlatform/python-docs-samples

import json
from google.cloud import bigquery


def sync_query(query, max_packages=5000):
    client = bigquery.Client("annular-mercury-117813")
    query_results = client.run_sync_query(query.format(max_packages))
    query_results.run()
    rows, total_rows, page_token = query_results.fetch_data()
    return tuple(rows)


# Third query from https://langui.sh/2016/12/09/data-driven-decisions/
QUERY = """SELECT
  file.project,
  COUNT(*) as total_downloads,
FROM
  TABLE_DATE_RANGE(
    [the-psf:pypi.downloads],
    DATE_ADD(CURRENT_TIMESTAMP(), -31, "day"),
    DATE_ADD(CURRENT_TIMESTAMP(), -1, "day")
  )
GROUP BY
  file.project
ORDER BY
  total_downloads DESC
LIMIT {}"""

if __name__ == '__main__':
    results = sync_query(QUERY, 10000)
    with open('pypi_packages.json', 'w') as out_file:
        json.dump(results, out_file)
    print(len(results))
