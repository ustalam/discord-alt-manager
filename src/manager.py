import requests, threading

from src.data import Data

class Manager:

    def __init__(self):
        self.data = Data()
        self.accounts = Data().load()
        
    def validate_token(self, token: str):
        
        r = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token})
        if r.status_code == 200:
            return True
        else:
            return False    

    def parse_token_data(self, token: str, data: dict):
        if any(value is None for value in data.values()):
            r = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token})
            if r.status_code == 200:
                req_data = r.json()
                
                data['username'] = req_data['username']
                data['display_name'] = req_data['global_name']
                data['id'] = req_data['id']
                data['avatar'] = req_data['avatar']
                print('[manager] ~ fixed token')
                return data
            else:
                print('[manager] ~ invalid response from token parser')
                return data
        return data

    def add_account(self, token: str):
        if self.validate_token(token):
            account = self.parse_token_data(token, {
                'token': token,
                'username': None,
                'display_name': None,
                'id': None,
                'avatar': None,
            })
            self.accounts['data'].append(account)
            self.data.save(self.accounts)
            print('[manager] ~ added account')
            return account
        else:
            print('[manager] ~ invalid token')
            return False

    def remove_account(self, token: str):
        for account in self.accounts['data']:
            print(account['token'])
            if account['token'] == token:
                self.accounts['data'].remove(account)
                self.data.save(self.accounts)
                print('[manager] ~ removed account')
                return account

        print('[manager] ~ account not found')
        return False  
                

    def load_accounts(self):
        print('[manager] ~ loading accounts')

        for ind, account in enumerate(self.accounts['data']):
            if self.validate_token(account['token']):
                account = self.parse_token_data(account['token'], account)
                self.accounts['data'][ind] = account
                print(f'[manager] ~ loaded account {account["username"]}')
               
            else:
                print('[manager] ~ invalid token')
                self.accounts['data'].remove(account)
             
                print('[manager] ~ removed account')
        
        
        self.data.save(self.accounts)
        print('[manager] ~ loaded accounts')

    def get_account(self, token: str):
        for account in self.accounts['data']:
            if account['token'] == token:
                return account
        return None
    
    def get_accounts(self):
        return self.accounts['data']

    def get_account_by_id(self, userid: str):
        for account in self.accounts['data']:
            if account['id'] == userid:
                return account
        return None

    def run(self):
        self.load_accounts()
