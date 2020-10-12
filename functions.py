import requests
from bs4 import BeautifulSoup as Soup
import json

def get_alfabank(data):
	parser = "html.parser"
	response = requests.get(data['api_url'])
	currencies = Soup(Soup(response.text, parser).description.text, parser).find_all("tr")
	dollar, euro = list(currencies[1]), list(currencies[2])
	data['buy']['USD'] = float(dollar[1].text)
	data['buy']['EUR'] = float(euro[1].text)
	data['sell']['USD'] = float(dollar[2].text)
	data['sell']['EUR'] = float(euro[2].text)
	return data

def get_tinkoff(data):
	response = requests.get(data['api_url']).json()
	category = 'DebitCardsTransfers'
	for rate in response['payload']['rates']:
		if rate['category'] == category:
			if rate['fromCurrency']['name'] in ['USD', 'EUR'] and rate['toCurrency']['name'] == 'RUB':
				data['buy'][rate['fromCurrency']['name']] = float(rate['buy'])
				data['sell'][rate['fromCurrency']['name']] = float(rate['sell'])
	return data    		

def get_sberbank(data):
	for currency in data['api_url'].keys():
		response = requests.get(data['api_url'][currency]).json()
		code = '840' if currency == 'USD' else '978'
		data['buy'][currency] = float(response['base'][code]['0']['buyValue'])
		data['sell'][currency] = float(response['base'][code]['0']['sellValue'])
	return data
	

def exchange_rates_request(params):
	try:
		params['Alfabank'] = get_alfabank(params['Alfabank'])
	except:
		pass
	try:
		params['Tinkoff'] = get_tinkoff(params['Tinkoff'])
	except:
		pass
	try:
		params['Sberbank'] = get_sberbank(params['Sberbank'])
	except:
		pass