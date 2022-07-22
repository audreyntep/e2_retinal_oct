# RetinAI web application - MedTech by Audrey Ntep
## Retinal Diagnosis by Image-Based Deep Learning

Windows configuration

### 1. Install dependencies

<code>pip install requirements.txt</code>

### 2. Launch flask local server with Powershell

<code>$ env:FLASK_APP= "main"</code>

<code>$ flask run</code>

### 3. Access web app with navigator

<code> GET http:127.0.0.1:5000/</code>

1. First browse local directory to select one or many OCT images, open

2. Then click "Upload" button, to load images on web server

3. Finally click "Diagnose" button to get results :

    - CNV and DME retinas are red

    - Drusen retina is orange

    - Normal retina is green


### 4. Consumming API

<code>GET http:127.0.0.1:5000/api</code>

1. Get model architecture

    <code>GET http:127.0.0.1:5000/api/model</code>

2. Get model metrics

    <code>GET http:127.0.0.1:5000/api/metrics</code>

3. Get model classes

    <code>GET http:127.0.0.1:5000/api/classes</code>

4. Get diagnosis

    <code>POST http:127.0.0.1:5000/api</code>

    **Query parameters :**

    | Type | Params | Values |
    |:-----|:-------|:-------|
    | POST | files | [{'file': *< file1 >*}, {'file': *< file2 >*}] |


    **Response :**

    | Status | Response |
    |:-----|:-------|
    | 200 | { "diagnosis": [{"filename": *< string >*,"result": *< integer >*,"classes":*< string >*}] } |
    | 204 | File not found or no file received |



### 5. Data storage

OCT image files are temporary stored in web app server : <code>'/static/oct_image'</code>

OCT image files are temporary stored in api server : <code>'/data'</code>