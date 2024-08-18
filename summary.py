import datetime
from elastic_op import connect_elasticsearch, send_document, load_query, execute_query

ELASTIC_URL = 'https://0.0.0.0:9200'
USERNAME = 'elastic'
PASSWORD = '123456'
WEATHER_API_TOKEN = 'dad850f6614d36b0f9bf9d002d078de7'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
SCHEDULE = 60
DAILY_WEATHER_INDEX = 'weather-*'
SUMMARY_INDEX = 'summary'

aggregate_query = load_query()


def get_summry():
    es = connect_elasticsearch(ELASTIC_URL, USERNAME, PASSWORD)
    result = execute_query(es, DAILY_WEATHER_INDEX, aggregate_query)
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


def send_summary_to_elastic():
    summaries = get_summry()
    if len(summaries) != 0:
        es = connect_elasticsearch(ELASTIC_URL, USERNAME, PASSWORD)
        for summary in summaries:
            send_document(es, index=SUMMARY_INDEX, document=summary)
        es.close()


send_summary_to_elastic()
