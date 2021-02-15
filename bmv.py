import requests
import json
import jwt
import os
import inspect
from datetime import datetime, timedelta



class GBM:

    def __init__(self, username, password, clientid):
        self.username = username
        self.password = password
        self.clientId = clientid
        self.latest_market = datetime.now() - timedelta(minutes=5)
        self.tokenRefresher = ''
        self.token = self.get_token()
        self.market = self.get_market()
        

    def validate_token(self):
        token_info = jwt.decode(self.token, options={"verify_signature": False})
        return datetime.now() < datetime.fromtimestamp(token_info['exp']) - timedelta(minutes=5)

    def execute_request(self, url: str, payload: dict, token=None):
        headers = {
                'Content-Type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
        if token:
            headers['Authorization'] = 'Bearer ' + token
        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload, indent=2))
        content = json.loads(response.content)
        print(f"request executed from: {inspect.stack()[1][3]}")
        return content

    def get_token(self):
        url = 'https://auth.gbm.com/api/v1/session/user'
        payload = {'clientId': self.clientId,
                   'user': self.username, 'password': self.password}
        content = self.execute_request(url, payload)
        try:
            token = content['accessToken']
            self.tokenRefresher = content['refreshToken']
        except:
            print(content)
        return token

    def refresh_token(self):
        url = 'https://auth.gbm.com/api/v1/session/user/refresh'
        payload = {"refreshToken": self.tokenRefresher,
                   "clientId": self.clientId}
        content = self.execute_request(url, payload)
        try:
            token = content['accessToken']
        except:
            print(content)
        return token

    def get_market(self):
        if not self.validate_token():
            self.token = self.refresh_token()
        if self.latest_market + timedelta(minutes=2) < datetime.now():
            url = "https://homebroker-api.gbm.com/GBMP/api/Market/GetMarketPriceMonitorDetail/"
            payload = {"isOnLine": "true", "instrumentType": 0}
            content = self.execute_request(url, payload, self.token)
            self.latest_market = datetime.now()
        else:
            content = self.market
            print('same market')
        return content

    
    def get_symbol(self, stock: str):
        try:
            symbol = list(filter(lambda person: stock.upper() in person['symbol'], self.get_market()))[0]
        except:
            symbol = list(filter(lambda person: stock.lower() in person['issueName'].lower(), self.get_market()))[0]
        return symbol
