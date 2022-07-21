import setuptools
import os
from web import create_app as create_app_website
from api import create_app as create_app_api
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

app_web = create_app_website()
app_api = create_app_api()

apps = DispatcherMiddleware(app_web, {'/api': app_api})

# Lancement de l'application
if __name__ == '__main__':
    # clear image file directories
    for root, dirs, files in os.walk("api/data"):
        for file in files:
            os.remove(os.path.join(root, file))
    for root, dirs, files in os.walk("web/static/oct_image"):
        for file in files:
            os.remove(os.path.join(root, file))
    run_simple('127.0.0.1', 5000, apps, use_reloader=True, use_debugger=True, use_evalex=True, threaded=True)
    
