import os
from web import create_app as create_app_website
from api import create_app as create_app_api
from api.first_model.app import app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple


# modifie le type MIME des scripts js (remplace "text/plain")
import mimetypes
mimetypes.add_type('text/javascript', '.js')


app_web = create_app_website()
app_api = create_app_api()
apps = DispatcherMiddleware(app_web, {'/api': app_api, '/first_model': app})

# Run flask multithreading
if __name__ == '__main__':
    
    # clear image files uploaded in app and api directories
    for root, dirs, files in os.walk("api/data/diagnoses/"):
        for file in files:
            os.remove(os.path.join(root, file))
    for root, dirs, files in os.walk("web/static/oct_image"):
        for file in files:
            os.remove(os.path.join(root, file))

    run_simple('127.0.0.1', 5000, apps, use_reloader=True, use_debugger=True, use_evalex=True, threaded=True)
    
