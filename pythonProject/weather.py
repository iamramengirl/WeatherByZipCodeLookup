from flask import Flask, render_template, request

import json
import urllib.request
import datetime
import calendar
import os
import sys

from pytz import timezone

app = Flask(__name__)

@app.route('/', methods =['POST', 'GET'])
def weather():
	if request.method == "GET":
		return render_template("index.html", data=None)
	elif request.method == "POST":
		zipcode = request.form['zipcode']

	zipcode = zipcode + ',jp'

	api = 'ecbe56994eea06c2715ab24224923c4d'

	url = 'http://api.openweathermap.org/data/2.5/forecast?zip=' + zipcode + '&APPID=' + api
	print("url:", url)
	source = urllib.request.urlopen(url).read()
	print("json:", source)

	data_lst = json.loads(source)

	weather_dt = []
	temp = []
	for i in range(20):
		if i in [0,3,11]:
			w_dt = datetime.datetime.strptime(data_lst['list'][i]['dt_txt'][0:10], '%Y-%m-%d')
			weather_dt.append(data_lst['list'][i]['dt_txt'][0:10] + " " + calendar.day_abbr[w_dt.weekday()])
			temp.append("Min:" + str(data_lst['list'][i]['main']['temp_min']) + \
						"° Max:" + str(data_lst['list'][i]['main']['temp_max']) + "°")

	# data for variable list_of_data
	data = {
		"country_name": str(data_lst['city']['country']),
		"city_name": str(data_lst['city']['name']),
		"lat": str(data_lst['city']['coord']['lat']),
		"lon": str(data_lst['city']['coord']['lon']),
		"forecast0": str(data_lst['list'][0]['weather'][0]['main']),
		"forecast0icon": str(data_lst['list'][0]['weather'][0]['icon']),
		"forecast0dt" : str(weather_dt[0]),
		"forecast0temp" : str(temp[0]),
		"forecast1": str(data_lst['list'][3]['weather'][0]['main']),
		"forecast1icon": str(data_lst['list'][3]['weather'][0]['icon']),
		"forecast1dt": str(weather_dt[1]),
		"forecast1temp" : str(temp[1]),
		"forecast2": str(data_lst['list'][11]['weather'][0]['main']),
		"forecast2icon": str(data_lst['list'][11]['weather'][0]['icon']),
		"forecast2dt": str(weather_dt[2]),
		"forecast2temp": str(temp[2])
	}
	print("data:", data)

	return render_template('index.html', data=data)

@app.errorhandler(400)
def bad_request_error(e):
	return render_template('error.html'), 400

@app.errorhandler(404)
def not_found_error(e):
	return render_template('error.html'), 404

@app.errorhandler(500)
def internal_error(e):
	return render_template('error.html'), 500

if __name__ == '__main__':
	app.run(debug=True)
