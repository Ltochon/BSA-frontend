import os
from random import randint
import sys
import requests
import json
from datetime import datetime, timedelta

import bme680
import time

from flask import Flask, jsonify, make_response, send_file, send_from_directory, request
from flask import render_template

app = Flask(_name_, static_folder='files')


class Bme680_manager:
    
    def _init_(self):
        
        try:
            self.__sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.__sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        
        
        self.__sensor.set_humidity_oversample(bme680.OS_2X)
        self.__sensor.set_pressure_oversample(bme680.OS_4X)
        self.__sensor.set_temperature_oversample(bme680.OS_8X)
        self.__sensor.set_filter(bme680.FILTER_SIZE_3)
        self.__sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

        self.__sensor.set_gas_heater_temperature(320)
        self.__sensor.set_gas_heater_duration(150)
        self.__sensor.select_gas_heater_profile(0)
                
        
    
    def get_sensor_data(self):
         sensor = self.get_sensor()
         sensor.get_sensor_data() # function from original lib, to update sensor inputs
         return {'humidity': sensor.data.humidity,
                    'gas_resistance': sensor.data.gas_resistance,
                    'temperature': sensor.data.temperature}
    
    def get_gas_baseline(self,t):
        sensor = self.get_sensor()
        burn_in_data = []
        i = 0
        while i < t+3:
            time.sleep(1)
            if sensor.get_sensor_data() and sensor.data.heat_stable:
                gas = sensor.data.gas_resistance
                burn_in_data.append(gas)
                i+=1
        gas_baseline = sum(burn_in_data[3:t+3]) / t
        return gas_baseline
    
    def get_air_quality(self,g_b):
        sensor = self.get_sensor()
        gas = sensor.data.gas_resistance
        gas_offset = g_b - gas
        hum_baseline = 40
        hum_weighting = 0.25
        hum = sensor.data.humidity
        hum_offset = hum - hum_baseline
        if hum_offset > 0:
            hum_score = (100 - hum_baseline - hum_offset)
            hum_score /= (100 - hum_baseline)
            hum_score *= (hum_weighting * 100)

        else:
            hum_score = (hum_baseline + hum_offset)
            hum_score /= hum_baseline
            hum_score *= (hum_weighting * 100)
            
        if gas_offset > 0:
            gas_score = (gas / g_b)
            gas_score *= (100 - (hum_weighting * 100))

        else:
            gas_score = 100 - (hum_weighting * 100)
        air_quality_score = hum_score + gas_score
        return air_quality_score
        
    def get_sensor(self):
        return self.__sensor

@app.route("/")
def hello(name=None):

    base = request.base_url
    responsemusic = requests.get("https://api.deezer.com/track/" + str(randint(210000,15000000))).json()
    preview = responsemusic["preview"]
    cover = responsemusic["album"]["cover"]
    titlemusic = responsemusic["title"]
    artist = responsemusic["artist"]["name"]
    responseinfo = requests.get("https://newsapi.org/v2/top-headlines?country=ch&apiKey=378f666235574b82802cb27ae05424eb").json()
    article = responseinfo["articles"][0]
    title = article["title"]
    urltoimage = article["urlToImage"]
    content = article["content"].replace('\r\n', ' $ ')
    url = article["url"]
    return render_template('base.html', title = title, content = content, urltoimage = urltoimage, url = url, cover = cover,artist = artist, titlemusic = titlemusic, preview = preview, base = base)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route("/data/")
def data():
    try:
        sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    except (RuntimeError, IOError):
        sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

    
    sensor_manager = Bme680_manager()

    gas_baseline = sensor_manager.get_gas_baseline(2)
    airqual = round(sensor_manager.get_air_quality(gas_baseline))


    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    hum = round(sensor.data.humidity)
    temp = round(sensor.data.temperature)
    dic = {"aq" : airqual, "hum" : hum, "temp" : temp}
    return jsonify(dic)

@app.route("/forecast/")
def testf():
    uri = "https://bsaflaskapp-mdefaecyva-oa.a.run.app/forecast/"
    try:
        uResponse = requests.get(uri)
        
    except requests.ConnectionError:
       return "Connection Error"   
    base = request.base_url.split("forecast/")[0]
    data = uResponse.json()
    return render_template("forecast.html",data = data["img"], base = base)

@app.route("/current/")
def testc():
    uri = "https://bsaflaskapp-mdefaecyva-oa.a.run.app/current/"
    try:
        uResponse = requests.get(uri)
        
    except requests.ConnectionError:
       return "Connection Error"   
    base = request.base_url.split("current/")[0]
    data = uResponse.json()
    return render_template("current.html",data = data["img"], base = base)

if _name_ == "_main_":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))