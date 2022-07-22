# RetinAI web application
## Retinal Diagnosis by Image-Based Deep Learning


### 1. Install dependencies

<code>pip install requirements.txt</code>

### 2. Launch flask server with powershell

<code>$ env:FLASK_APP= "main"</code>

<code>$ flask run</code>

### 3. Access web app with navigator

<code> GET http:127.0.0.1:5000/</code>

1. First browse local directory to select one or many OCT images, open

2. Then click "Upload" button, to load images on web server

3. Finally click "Diagnose" button to get results


### 4. Consumming API

<code>GET http:127.0.0.1:5000/api</code>

1. Get model architecture

    HTTP Request : <code>GET http:127.0.0.1:5000/api/model</code>

2. Get model metrics

    HTTP Request : <code>GET http:127.0.0.1:5000/api/metrics</code>

3. Get model classes

    HTTP Request : <code>GET http:127.0.0.1:5000/api/classes</code>

4. Get diagnosis

    HTTP Request : <code>POST http:127.0.0.1:5000/api</code>

    Query parameters :

    | Type | Params | Values |
    --------------------------
    | POST | files | a list of dict like '{'file': <file>} |


    Response

    | Status | Response |
    --------------------------
    | 200 | { "diagnosis": [
                {
                    "filename": <string>,
                    "result": <integer>,
                    "classes":<string>
                }
            ]} |

