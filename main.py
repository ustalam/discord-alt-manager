import webview
from src.api import API

if __name__ == '__main__':

    api = API()
    window = webview.create_window(
        'Discord Alt Manager', 
        "index.html", 
        frameless=True, 
        width=800, 
        height=600, 
        resizable=True, 
        min_size=(800, 600), 
        easy_drag = True,
        js_api=api
    
    )
    api.set_window(window)
    webview.start()