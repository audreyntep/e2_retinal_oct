import setuptools
from web import create_app as create_app_website
from api import create_app as create_app_api
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

app_web = create_app_website()
app_api = create_app_api()

apps = DispatcherMiddleware(app_web, {'/api': app_api})

# Lancement de l'application
if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, apps, use_reloader=True, use_debugger=True, use_evalex=True, threaded=True)
    
