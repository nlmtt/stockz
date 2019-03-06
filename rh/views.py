import logging

from django.shortcuts import render
from django.http import HttpResponse

import requests

from .robinhood import Robinhood

log = logging.getLogger(__name__)

def index(request):
	log.error(1)
	rh = Robinhood()
	print(2)
	rs = rh.get_accounts()
	print(3)
	try:
		cash = rs.json()['results'][0]['margin_balances']['cash']
	except Exception as e:
		print(4)
		print(e)
	return HttpResponse('$' + cash)

# TODO implement Robinhood class which can login and maintain session
# TODO implement persisting to DB
# TODO add styling
