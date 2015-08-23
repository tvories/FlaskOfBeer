from flask import jsonify
import os
import glob
import time
from . import api
from app import celery
from ..models import SensorData, TempSensor

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw(sensor_serial):
    device_folder2 = glob.glob(base_dir + sensor_serial)[0]
    device_file2 = device_folder2 + '/w1_slave'
    f = open(device_file2, 'r')
    lines = f.readlines()
    f.close()
    return lines


# Reads temp and returns Fahrenheit temperature
def read_temp_c(sensor_serial):
    lines = read_temp_raw(sensor_serial)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return round(temp_c, 2)


def read_temp_f(sensor_serial):
    temp_f = read_temp_c(sensor_serial) * 9.0 / 5.0 + 32.0
    return round(temp_f, 2)


@api.route('/temp/<sensor_serial>', methods=['GET'])
def get_temp(sensor_serial):
    return jsonify({'temp_f': read_temp_f(sensor_serial)})


@api.route('/temp/<int:numtemps>')
def get_multi_temps(numtemps):
    sensor_data = SensorData.query.all()
    sensor_arr = []
    if numtemps < len(sensor_data):
        i = 0
        while i < numtemps:
            sensor_arr.append(sensor_data[i].to_json())
            i += 1
        return jsonify(results=sensor_arr)
    else:
        i = 0
        while i < len(sensor_data):
            sensor_arr.append(sensor_data[i].to_json())
            i += 1
        return jsonify(results=sensor_arr)
