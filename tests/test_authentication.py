import mock

import service
from service.server import app


class TestAuthentication:

    def setup_method(self, method):
        self.app = app.test_client()

    @mock.patch.object(service.server.Form, 'validate')
    def test_sign_in_validates_user_input(self, mock_validate):
        self.app.post('/login')
        mock_validate.assert_called_once_with()

    @mock.patch('service.server.LOGIN_API_CLIENT.authenticate_user', return_value=False)
    def test_sign_in_calls_api_to_authenticate_user_when_form_valid(self, mock_authenticate):
        username = 'username1'
        password = 'password1'

        self.app.post('/login', data={'username': username, 'password': password})

        mock_authenticate.assert_called_once_with(username, password)

    @mock.patch('service.server.LOGIN_API_CLIENT.authenticate_user', return_value=False)
    def test_sign_in_does_not_call_api_when_form_invalid(self, mock_authenticate):
        self.app.post('/login', data={'username': '', 'password': ''})
        assert mock_authenticate.mock_calls == []

    @mock.patch('service.server.login_user')
    @mock.patch('service.server.LOGIN_API_CLIENT.authenticate_user', return_value=True)
    def test_sign_in_logs_user_in_when_authentication_successful(
            self, mock_authenticate, mock_login):
        username = 'username1'

        self.app.post('/login', data={'username': username, 'password': 'password1'})

        assert len(mock_login.mock_calls) == 1
        logged_in_user = mock_login.mock_calls[0][1][0]
        assert logged_in_user.user_id == username

    @mock.patch('service.server.login_user')
    @mock.patch('service.server.LOGIN_API_CLIENT.authenticate_user', return_value=False)
    def test_sign_in_does_not_log_user_in_when_authentication_unsuccessful(
            self, mock_authenticate, mock_login):

        response = self.app.post(
            '/login',
            data={'username': 'username1', 'password': 'password1'}
        )

        assert mock_login.mock_calls == []
        assert response.status_code == 200
        assert 'There was an error with your Username/Password' in response.data.decode()

    @mock.patch('service.server.current_user')
    @mock.patch('service.server.logout_user')
    def test_sign_out_logs_user_out_when_user_id_present(
            self, mock_logout_user, mock_current_user):

        mock_current_user.get_id.return_value = "user_id_123"

        response = self.app.get('/logout')

        mock_logout_user.assert_called_once_with()
        assert response.status_code == 302
        assert response.location.endswith('/login')

    @mock.patch('service.server.current_user')
    @mock.patch('service.server.logout_user')
    def test_sign_out_does_not_log_user_out_when_user_id_absent(
            self, mock_logout_user, mock_current_user):

        mock_current_user.get_id.return_value = None
        self.app.get('/logout')
        assert mock_logout_user.mock_calls == []
