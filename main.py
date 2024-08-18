import asyncio
import aioschedule as schedule
from typing import List
from task import create_data, call_weather_api
from send_to_elastic import connect_elasticsearch, send_document
import models
from dbconnection import engine, SessionLocal
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import func

ELASTIC_URL = 'https://0.0.0.0:9200'
USERNAME = 'elastic'
PASSWORD = '123456'
WEATHER_API_TOKEN = 'dad850f6614d36b0f9bf9d002d078de7'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
SCHEDULE = 60
DAILY_WEATHER_INDEX = 'weather-17-08-2024'


models.Base.metadata.create_all(bind=engine)


async def my_task(cities: List[str] = CITIES):
    es = connect_elasticsearch(ELASTIC_URL, USERNAME, PASSWORD)
    for city in cities:
        document = create_data(call_weather_api(WEATHER_API_TOKEN, city))
        send_document(es, DAILY_WEATHER_INDEX, document=document)

async def create_day_summary():
    # Filter for data within the last 24 hours
    pass


async def my_task2(cities: List[str] = CITIES):
    session = SessionLocal()
    for city in cities:
        document = create_data(call_weather_api(WEATHER_API_TOKEN, city))
        data = models.TempData(city=document['city'], temp=document['temp'], wethercondition=document['main'],
                               time=document['timestamp'], feels_like=document['feels_like'])
        session.add(data)
        session.commit()
        session.refresh(data)
    session.close()


async def run_scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    schedule.every(SCHEDULE).seconds.do(my_task)
    await run_scheduler()

# Start the async loop
asyncio.run(main())
