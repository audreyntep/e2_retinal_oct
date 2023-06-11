import pytest
import requests

# URL de l'API
api_url = 'http://127.0.0.1:5000/first_model'

def test_index():
    # Envoyer une requête GET à l'API
    response = requests.get(api_url+'/')
    # Vérifier la réponse
    assert response.text == 'Retinal OCT prediction API'

@pytest.fixture
def image_path():
    # Chemin vers l'image de test
    return 'api/first_model/test_img.jpeg'

def test_prediction(image_path):
    # Ouvrir l'image en tant que fichier binaire
    with open(image_path, 'rb') as file:
        # Envoyer la requête POST à l'API
        response = requests.post(api_url+'/predict', files={'file': file})
    # Vérifier la réponse
    assert response.status_code == 200
    result = response.json()['result']
    assert isinstance(result, str)

# Exécutez les tests avec pytest
pytest.main()
