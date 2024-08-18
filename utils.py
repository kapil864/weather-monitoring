from models import TempData
from sqlalchemy import func, desc, select, alias
from dbconnection import SessionLocal
from datetime import datetime, timedelta, timezone


def most_frequent_weather(session, time_delta):
    """Calculates the most frequent weather condition for each city.

    Args:
        session: SQLAlchemy session object.
        model: The SQLAlchemy model class.

    Returns:
        A list of tuples containing city and most frequent weather condition.
    """
    last_24_hours = datetime.now(tz=timezone.utc) - timedelta(days=1)

    weather_counts = alias(select(TempData.city, TempData.wethercondition, func.count('*').label('count'))
                           .group_by(TempData.city, TempData.wethercondition).filter(TempData.time >= last_24_hours))

    subquery = alias(select(func.max(weather_counts.c.count))
                     .where(weather_counts.c.city == weather_counts.c.city))

    # Main query
    query = select(weather_counts.c.city, weather_counts.c.wethercondition) \
        .select_from(weather_counts) \
        .where(weather_counts.c.count == subquery)
    
    return session.execute(query).fetchall()

# def get_max(session, field, model, time_delta):


def create_aggregates():
    session = SessionLocal()
    last_24_hours = datetime.now(tz=timezone.utc) - timedelta(days=1)

    most_frequent_weather_data = most_frequent_weather(session, TempData)

    # Construct the query
    query = session.query(TempData.city,
                          func.max(TempData.temp).label('max_temp'),
                          func.min(TempData.temp).label('min_temp'),
                          func.avg(TempData.temp).label('avg_temp'))

    # Filter for data within the specified timeframe
    query = query.filter(TempData.time >= last_24_hours)

    # Group by city to get aggregates for each city
    query = query.group_by(TempData.city)

    # Execute the query and fetch results
    results = query.all()

    print(most_frequent_weather)

    # Access results as tuples with city, max_temp, min_temp, avg_temp
    for city, max_temp, min_temp, avg_temp in results:
        print(f"City: {city}, Max Temp: {max_temp}, Min Temp: {min_temp}, Avg Temp: {avg_temp}")

create_aggregates()