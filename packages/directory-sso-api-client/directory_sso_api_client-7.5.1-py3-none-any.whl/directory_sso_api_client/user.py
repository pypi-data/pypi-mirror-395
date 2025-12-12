import json
from collections import OrderedDict

import pkg_resources
import urllib3
from directory_client_core.authentication import AuthenticatorNegotiator
from directory_client_core.base import AbstractAPIClient
from tenacity import retry, stop_after_attempt, wait_exponential


class UserAPIClient(AbstractAPIClient):
    site_root_url = ''
    endpoints = {
        'session_user': 'api/v1/session-user/',
        'oauth2_user_profile': 'oauth2/user-profile/v1/',
        'last_login': 'api/v1/last-login/',
        'check_password': 'api/v1/password-check/',
        'regenerate_verification': 'api/v1/verification-code/regenerate/',
        'verify_verification': 'api/v1/verification-code/verify/',
        'user_create': 'api/v1/user/',
        'user_create_profile': 'api/v1/user/profile/',
        'user_update_profile': 'api/v1/user/profile/update/',
        'user_page_views': 'api/v1/user/page-view/',
        'user_lesson_completed': 'api/v1/user/lesson-completed/',
        'user_questionnaire': 'api/v1/user/questionnaire/',
        'user_data': 'api/v1/user/data/',
        'user_login': 'accounts/login/',
        'user_logout': 'accounts/logout/',
        'account_create': 'api/v2/account/',
        'regenerate_account_verification_code': 'api/v2/verification-code/regenerate/',
        'verify_account_verification_code': 'api/v2/verification-code/verify/',
        'get_account_user': 'api/v2/account-user/',
        'reset_password_invitation': 'api/v2/accounts/password/reset/',
        'reset_password_change': 'api/v2/accounts/password/reset/change/',
        'check_token': 'api/v2/accounts/password/reset/validate/token/',
    }
    version = pkg_resources.get_distribution(__package__).version

    def __init__(self, site_root_url='', *args, **kwargs):
        self.site_root_url = site_root_url
        super().__init__(*args, **kwargs)

    def get_session_user(self, session_id, authenticator=None):
        return self.get(
            url=self.endpoints['session_user'],
            params={'session_key': session_id},
            authenticator=authenticator,
        )

    def get_oauth2_user_profile(self, bearer_token):
        return self.get(
            url=self.endpoints['oauth2_user_profile'], authenticator=AuthenticatorNegotiator(bearer_token=bearer_token)
        )

    def regenerate_verification_code(self, data, authenticator=None):
        return self.post(
            url=self.endpoints['regenerate_verification'],
            data=data,
            authenticator=authenticator,
        )

    def verify_verification_code(self, data, authenticator=None):
        return self.post(
            url=self.endpoints['verify_verification'],
            data=data,
            authenticator=authenticator,
        )

    def check_password(self, session_id, password, authenticator=None):
        url = self.endpoints['check_password']
        data = OrderedDict([('session_key', session_id), ('password', password)])
        return self.post(
            url,
            data,
            authenticator=authenticator,
        )

    def get_last_login(self, start=None, end=None, authenticator=None):
        params = {}
        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end
        params = params or None

        return self.get(
            url=self.endpoints['last_login'],
            params=params,
            authenticator=authenticator,
        )

    def create_user(self, email, password, authenticator=None, mobile_phone_number=None, is_eyb_user=None):
        url = self.endpoints['user_create']
        data = OrderedDict(
            [
                ('email', email),
                ('password', password),
                ('mobile_phone_number', mobile_phone_number),
                ('is_eyb_user', is_eyb_user),
            ]
        )
        return self.post(
            url,
            data,
            authenticator=authenticator,
        )

    def create_user_profile(self, sso_session_id, data):
        authenticator = AuthenticatorNegotiator(sso_session_id=sso_session_id)
        url = self.endpoints['user_create_profile']
        return self.post(url, data, authenticator=authenticator)

    def update_user_profile(self, sso_session_id, data):
        authenticator = AuthenticatorNegotiator(sso_session_id=sso_session_id)
        url = self.endpoints['user_update_profile']
        return self.patch(url, data, authenticator=authenticator)

    def set_user_page_view(self, sso_session_id, service, page):
        authenticator = AuthenticatorNegotiator(sso_session_id=sso_session_id)
        url = self.endpoints['user_page_views']
        return self.post(url, {'service': service, 'page': page}, authenticator=authenticator)

    def get_user_page_views(self, sso_session_id, service, page):
        authenticator = AuthenticatorNegotiator(sso_session_id=sso_session_id)
        url = self.endpoints['user_page_views']
        return self.get(url, {'service': service, 'page': page}, authenticator=authenticator)

    def get_user_lesson_completed(self, sso_session_id, service, lesson_page):
        authenticator = AuthenticatorNegotiator(sso_session_id=sso_session_id)
        url = self.endpoints['user_lesson_completed']
        return self.get(url, {'service': service, 'lesson': lesson_page}, authenticator=authenticator)

    def set_user_lesson_completed(self, sso_session_id, service, lesson_page, lesson, module):
        authenticator = AuthenticatorNegotiator(sso_session_id=sso_session_id)
        url = self.endpoints['user_lesson_completed']
        return self.post(
            url,
            {
                'service': service,
                'lesson_page': lesson_page,
                'lesson': lesson,
                'module': module,
            },
            authenticator=authenticator,
        )

    def delete_user_lesson_completed(self, sso_session_id, service, lesson):
        authenticator = AuthenticatorNegotiator(sso_session_id=sso_session_id)
        url = self.endpoints['user_lesson_completed']
        return self.delete(url, {'service': service, 'lesson': lesson}, authenticator=authenticator)

    def get_user_questionnaire(self, sso_session_id, service):
        url = self.endpoints['user_questionnaire']
        return self.get(url, {'service': service}, authenticator=AuthenticatorNegotiator(sso_session_id=sso_session_id))

    def set_user_questionnaire_answer(self, sso_session_id, service, question_id, answer):
        url = self.endpoints['user_questionnaire']
        return self.post(
            url,
            {'service': service, 'question_id': question_id, 'answer': answer},
            authenticator=AuthenticatorNegotiator(sso_session_id=sso_session_id),
        )

    def get_user_data(self, sso_session_id, name):
        url = self.endpoints['user_data']
        return self.get(url, {'name': name}, authenticator=AuthenticatorNegotiator(sso_session_id=sso_session_id))

    def set_user_data(self, sso_session_id, data, name):
        url = self.endpoints['user_data']
        return self.post(
            url, {'data': data, 'name': name}, authenticator=AuthenticatorNegotiator(sso_session_id=sso_session_id)
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def user_login(self, data, csrf_token=None):
        csrf_token = self.get_csrf_token()
        data['csrfmiddlewaretoken'] = csrf_token
        return self.post(
            self.endpoints['user_login'],
            data=data,
            csrf_token=csrf_token,
            cookies={'csrftoken': csrf_token},
            convert_data_to_json=False,
            content_type='application/x-www-form-urlencoded',
            allow_redirects=False,
            header_origin=self.site_root_url,
            header_referer=self.site_root_url,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def user_logout(self, cookies={}):
        csrf_token = self.get_csrf_token()
        return self.post(
            self.endpoints['user_logout'],
            csrf_token=csrf_token,
            cookies={'csrftoken': csrf_token, **cookies},
            content_type='text/plain',
            allow_redirects=False,
            header_origin=self.site_root_url,
            header_referer=self.site_root_url,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def get_csrf_token(self):
        url = '/csrf/'
        response = self.get(url)
        response.raise_for_status()

        try:
            json_object = json.loads(response.content.decode('utf-8'))
        except ValueError:
            raise urllib3.exceptions.HTTPError('Bad Request')
        else:
            csrf_token = json_object.get('csrftoken', None)
            return csrf_token

    """
    Account v2 APIs with exponential backoff
    """

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def create_account(self, email, password, authenticator=None):
        url = self.endpoints['account_create']
        data = OrderedDict(
            [
                ('email', email),
                ('password', password),
            ]
        )
        return self.post(
            url,
            data,
            authenticator=authenticator,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def regenerate_account_verification_code(self, data, authenticator=None):
        return self.post(
            url=self.endpoints['regenerate_account_verification_code'],
            data=data,
            authenticator=authenticator,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def verify_account_verification_code(self, data, authenticator=None):
        return self.post(
            url=self.endpoints['verify_account_verification_code'],
            data=data,
            authenticator=authenticator,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def get_account_user(self, hashed_uuid, authenticator=None):
        url = self.endpoints['get_account_user']
        return self.get(url, {'hashed_uuid': hashed_uuid}, authenticator=authenticator)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def send_password_reset_email(self, data, authenticator=None):
        url = self.endpoints['reset_password_invitation']
        return self.post(url, data, authenticator=authenticator)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def send_password_reset_change(self, data, authenticator=None):
        url = self.endpoints['reset_password_change']
        return self.post(url, data, authenticator=authenticator)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def check_reset_password_token(self, data, authenticator=None):
        url = self.endpoints['check_token']
        return self.post(url, data, authenticator=authenticator)
