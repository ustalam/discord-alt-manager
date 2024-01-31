import webview
from src.manager import Manager
from src.account import Account
class API:

    # stuff
    def __init__(self):
        self.window = None
        self.manager = Manager()
        self.manager.run()

    def set_window(self, window):
        self.window = window
        self.manager = Manager()

    # window controls
    def close(self):
        self.window.destroy()
        exit()

    def minimize(self):
        self.window.minimize()

    # manager
    def get_accounts(self) -> dict:
        return self.manager.get_accounts()
        
    def add_account(self, token: str):
        return self.manager.add_account(token)

    def remove_account(self, userid: str):
        token = self.manager.get_account_by_id(userid)['token']
        return self.manager.remove_account(token)
                
    def trade_id_for_token(self, userid: str):
        return self.manager.get_account_by_id(userid)['token']

    def get_account_token(self):
        acc = Account()
        return acc.get_token()

    def login(self, userid: str):
        account = self.manager.get_account_by_id(userid)
        
        acc = Account()
        acc.set_token(account['token'])
        acc.login()

        return account