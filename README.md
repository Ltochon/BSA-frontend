[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)    
[![Npm package license](https://badgen.net/npm/license/discord.js)](https://npmjs.com/package/discord.js)

# BSA_IoT_Project_Frontend

## Goal
This repository contains the frontend to deploy on the IoT device. This interface is constituted of 3 pages.
1) First page displays the current inside temperature, humidity and air quality values gotten by the sensor on the raspberry. Furthermore, with the help of Google Cloud AutoML, this page displays an inside air quality prediction in 30 minutes. To add more fun, we implemented a call to *Newsapi* to get the latest big news in Swiss and a call to *Deezer* to propose a song to listen to the user.
2) Second page displays the current outside weather with the help of *OpenWeatherMap*'s API.
3) Third page displays the forcast outside weather for the five next days with the help of *OpenWeatherMap*'s API.

## How to use it
To launch the interface just type this line in the root folder :

```py
python3 main.py
```