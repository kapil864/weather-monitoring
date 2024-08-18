from json import load

ELASTIC_URL = None
USERNAME = None
PASSWORD = None
WEATHER_API_TOKEN = None
CITIES = None
SCHEDULE = None
DAILY_WEATHER_INDEX = None
SUMMARY_INDEX = None


def load_config():
    file = open('config/global_config.json', 'r')
    config = load(file)
    file.close()
    global ELASTIC_URL
    global USERNAME
    global PASSWORD
    global WEATHER_API_TOKEN
    global CITIES
    global SCHEDULE
    global DAILY_WEATHER_INDEX
    global SUMMARY_INDEX
    ELASTIC_URL = config["ELASTIC_URL"]
    USERNAME = config["USERNAME"]
    PASSWORD = config["PASSWORD"]
    WEATHER_API_TOKEN = config["WEATHER_API_TOKEN"]
    CITIES = config["CITIES"]
    SCHEDULE = config["SCHEDULE_IN_SECOND"]
    DAILY_WEATHER_INDEX = config["DAILY_WEATHER_INDEX"]
    SUMMARY_INDEX = config["SUMMARY_INDEX"]


load_config()
