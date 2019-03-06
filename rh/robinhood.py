import logging
import os

import requests

log = logging.getLogger(__name__)

class Robinhood:
	def __init__(self):
		log.error('Creating session')
		self.session = requests.session()
		self.session.headers = {
			"Accept": "*/*", 
			"Accept-Encoding": "gzip, deflate", 
			"Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5", 
			"Content-Type": "application/x-www-form-urlencoded; charset=utf-8", 
			"X-Robinhood-API-Version": "1.0.0", 
			"Connection": "keep-alive", 
			"User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)" 
		}
		log.error('Trying to login')
		self.login()

	def get_accounts(self):
		rs = self.session.get('https://api.robinhood.com/accounts/')
		return rs

	def login(self):
		log.error('Retrieving username and password')
		data = {
			'username': os.environ['RHUSR'],
			'password': os.environ['RHPWD'], # TODO store password encrypted
			'grant_type': 'password',
			'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS'
		}
		log.error('Got usrnm and pswd')
		if 'Autorization' not in self.session.headers:
			log.error('Actually logging in')
			r = self.session.post('https://api.robinhood.com/oauth2/token/',data=data,timeout=15)
			if r.status_code == 200:
				log.error('Logged in')
				self.authenticated = True
				data = r.json()
				self.access_token = data['access_token']
				self.refresh_token = data['refresh_token']
				self.session.headers['Authorization'] = 'Bearer ' + self.access_token
				return True
			log.error('Failed to login')

	def logout(self):
		del self.session.headers['Authorization']
		self.session.close()


if __name__=='__main__':
	rh = Robinhood()
	assert rh.authenticated == True
	rh.logout()
	assert 'Authorization' not in rh.session.headers