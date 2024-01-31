import json, subprocess, os
from src.crypt import Crypt

class Data:

    def __init__(self):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.key = subprocess.check_output('wmic csproduct get uuid', startupinfo=si).decode().split('\n')[1].strip()
        self.crypt = Crypt(self.key)

        if not os.path.exists('.d'):
            os.mkdir('.d')

        if not os.path.exists('.d/data.json'):
           self.save({'data': []})


    def load(self):
        try:
            with open('.d/data.json', 'r') as f:
                data = json.load(f)
                return json.loads(self.crypt.decrypt(data))
        except Exception as err:
            print(err)
            return {}

    def save(self, data):

        data = json.dumps(data)
        data = self.crypt.encrypt(data)

        with open('.d/data.json', 'w') as f:
            json.dump(data.decode(), f)
