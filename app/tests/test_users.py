from app.main import testclient as client
import time


asd = None
class TestUser:
    response_credentials = None

    def test_read_main(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {'data': 'Ruta'}

    def test_login_without_register_user(self):
        form_data = {'username': 'corack', 'password':'12345'}
        response = client.post('/user/login', data=form_data)
        assert response.status_code == 401
        assert response.json() == {"detail": "Credenciales inválidas"}

    def test_create_user(self):
        body = {'username': 'corack', 'email': 'orcheko@gmail.com','password':'12345'}
        response = client.post('/user/create', json=body)
        assert response.status_code == 200
        assert response.json().get('username') == 'corack'
        assert response.json().get('email') == 'orcheko@gmail.com'
        assert response.json().get('id') == 1

    def test_login(self):
        # test_create_user()
        form_data = {'username': 'corack', 'password':'12345'}
        response = client.post('/user/login', data=form_data)
        TestUser.response_credentials = response.json()
        assert response.status_code == 200
        assert response.json().get('access_token')
        assert response.json().get('refresh_token')
        assert response.json().get('token_type') == 'bearer'

    def test_refresh_token(self):
        refresh_token = TestUser.response_credentials.get('refresh_token')
        response = client.get('/user/refresh_token', params={'token': refresh_token})
        TestUser.response_credentials['access_token'] = response.json().get('access_token')
        assert response.status_code == 200
        assert response.json().get('access_token')
        assert response.json().get('token_type') == 'bearer'
    
    def test_invalid_refresh_token(self):
        refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjb3JhY2siLCJleHAiOjE3MDM3MTg3NDh9.8YAOxE76YulFDbdW6POqMgM0KgmldjlgwlMog_1uMDF"
        response = client.get('/user/refresh_token', params={'token': refresh_token})
        assert response.status_code == 400
        assert response.json() == {"detail": "No se han podido validar las credenciales"}

    def test_create_user_with_same_data(self):
        body = {'username': 'corack', 'email': 'orcheko@gmail.com','password':'12345'}
        response = client.post('/user/create', json=body)
        assert response.status_code == 400
        assert response.json() == {"detail": "Ya existe un usuario con ese username o email"}

    def test_access_restricted_content(self):
        access_token = 'Bearer ' + TestUser.response_credentials.get('access_token')
        response = client.get('/user/info', headers={'Authorization': access_token})
        assert response.status_code == 200
        assert response.json() == {'username': 'corack', 'email': 'orcheko@gmail.com'}

    def test_revoke_restricted_content_without_token(self):
        response = client.get('/user/info')
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_revoke_restricted_content_with_token(self):
        access_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjb3JhY2siLCJleHAiOjE3MDM3MTIwMzZ9.GRc3jkPRArFgppmyp6QkAS4XZMx804dWaAC9HqB-6K8'
        response = client.get('/user/info', headers={'Authorization': access_token})
        assert response.status_code == 400
        assert response.json() == {"detail": "No se han podido validar las credenciales"}

    def test_logout(self):
        access_token = 'Bearer ' + TestUser.response_credentials.get('access_token')
        response = client.get('/user/logout', headers={'Authorization': access_token})
        TestUser.response_credentials = response.json()
        assert response.status_code == 200
        assert response.json().get('msg') == 'Se ha cerrado la sesión'
    
    def test_restricted_content_after_logout(self):
        access_token = 'Bearer ' + TestUser.response_credentials.get('access_token')
        time.sleep(1)
        response = client.get('/user/info', headers={'Authorization': access_token})

        assert response.status_code == 400
        assert response.json() == {'detail': 'No se han podido validar las credenciales'}