from datetime import datetime
import random
from app.models import SensorData, TempSensor

glob_hour = 0
glob_minute = 0
glob_day = 1
times = []
i = 0

def gen_fake_temps():
    sensor_data = SensorData()
    sensor_data.temp_sensor_id = 1
    sensor_data.timestamp = gen_timestamp()
    sensor_data.value = random.randint(6500, 7500) / 100.00
    return sensor_data


def gen_timestamp():
    global glob_hour
    global glob_minute
    global glob_day
    strtime = 'Aug {2} 2015 {0}:{1}'
    timestamp = datetime.strptime(strtime.format(glob_hour, glob_minute, glob_day), '%b %d %Y %H:%M')
    if glob_hour == 23:
        glob_day += 1
        glob_minute = 0
        glob_hour = 0
    elif glob_minute == 50:
        glob_hour += 1
        glob_minute = 0
    else:
        glob_minute += 10
    return timestamp
