import threading, logging
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.DEBUG)

class Account:

    def __init__(self):

        self.token = None
        self.driver = None


    def set_token(self, token):
        self.token = token
        return True

    def get_token(self):
        self.driver = Driver(uc=True)
        self.driver.set_window_size(800, 600)

        self.driver.get('https://www.discord.com/login')
        try:
            WebDriverWait(self.driver, 300).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#app-mount > div.appAsidePanelWrapper__714a6 > div.notAppAsidePanel__9d124 > div.app_b1f720 > div > div.layers__1c917.layers_a23c37 > div > div > div > div > div > section > div.container_ca50b9 > div.avatarWrapper_ba5175.withTagAsButton_cc125f > div.wrapper_edb6e0.avatar_f8541f'))
            )   
        except:
            print('timed out')
        
        self.token = self.driver.execute_script("""
        
            let token = 
            (
                webpackChunkdiscord_app.push(
                    [
                        [''],
                        {},
                        e => {
                            m = [];
                            for (let c in e.c)
                                m.push(e.c[c])
                        }
                    ]
                ),
                m
            ).find(
                m => m?.exports?.default?.getToken !== void 0
            ).exports.default.getToken()
            return token;
        """)
        self.driver.quit()
        return self.token
        
    def login_worker(self):

        self.driver = Driver(uc=True)
        self.driver.set_window_size(800, 600)

        self.driver.get('https://www.discord.com/login')
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]"))
        )

        self.driver.execute_script("""
            let token = "%s";
            function login(token) {
              	setInterval(() => {
                	document.body.appendChild(
                	  	document.createElement`iframe`
                	).contentWindow.localStorage.token = `"${token}"`;
              	}, 50);
              	setTimeout(() => {
                	location.reload();
              	}, 2500);
            }
            login(token);
        """ % self.token)

        while self.driver:
            pass


    def login(self):
        threading.Thread(target=self.login_worker).start()
