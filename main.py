import asyncio
import aioschedule as schedule
from typing import List
from task import create_data, call_weather_api
from elastic_op import connect_elasticsearch, send_document
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import func

ELASTIC_URL = 'https://0.0.0.0:9200'
USERNAME = 'elastic'
PASSWORD = '123456'
WEATHER_API_TOKEN = 'dad850f6614d36b0f9bf9d002d078de7'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
SCHEDULE = 60
DAILY_WEATHER_INDEX = 'weather-17-08-2024'



async def my_task(cities: List[str] = CITIES):
    es = connect_elasticsearch(ELASTIC_URL, USERNAME, PASSWORD)
    for city in cities:
        document = create_data(call_weather_api(WEATHER_API_TOKEN, city))
        send_document(es, DAILY_WEATHER_INDEX, document=document)
    es.close()


async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    schedule.every(SCHEDULE).seconds.do(my_task)
    await run_scheduler()

# Start the async loop
asyncio.run(main())
