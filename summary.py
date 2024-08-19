import datetime
from config import *

from elasticsearch import Elasticsearch
from elastic_op import (
    connect_elasticsearch,
    send_document,
    load_aggreagate_query,
    execute_search_query,
    execute_delete_query,
    load_delete_query)

aggregate_query = load_aggreagate_query()
delete_query = load_delete_query()


def get_summry():
    es = connect_elasticsearch(ELASTIC_URL, USERNAME, PASSWORD)
    result = execute_search_query(es, DAILY_WEATHER_INDEX, aggregate_query)
    summary = []
    if result.meta.status == 200:
        for aggreates in result["aggregations"]["cities"]["buckets"]:
            summary.append(
                {
                    "city": aggreates["key"],
                    "avg_temp": aggreates["avg_temp"]["value"],
                    "min_temp": aggreates["min_temp"]["value"],
                    "max_temp": aggreates["max_temp"]["value"],
                    "dominant_weather": aggreates["dominant_weather"]["buckets"][0]["key"],
                    "timestamp": datetime.datetime.now(datetime.timezone.utc)
                })
    es.close()
    return summary


def delete_old_data(es: Elasticsearch):
    response = execute_delete_query(
        es, index=DAILY_WEATHER_INDEX, query=delete_query)
    if response.meta.status == 200:
        print("Old data deleted")


def send_summary_to_elastic():
    summaries = get_summry()
    if len(summaries) != 0:
        es = connect_elasticsearch(ELASTIC_URL, USERNAME, PASSWORD)
        for summary in summaries:
            send_document(es, index=SUMMARY_INDEX, document=summary)
        delete_old_data(es)
        es.close()


send_summary_to_elastic()
