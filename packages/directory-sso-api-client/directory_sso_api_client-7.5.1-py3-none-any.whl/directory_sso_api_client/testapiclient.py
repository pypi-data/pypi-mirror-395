import pkg_resources
from directory_client_core.base import AbstractAPIClient

from directory_sso_api_client.user import UserAPIClient


class DirectorySSOTestAPIClient(AbstractAPIClient):
    endpoints = {'user_by_email': 'testapi/user-by-email/{email}/'}
    version = pkg_resources.get_distribution(__package__).version

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = UserAPIClient(*args, **kwargs)

    def get_user_by_email(self, email, authenticator=None):
        url = self.endpoints['user_by_email'].format(email=email)
        return self.get(url=url, authenticator=authenticator)

    def delete_user_by_email(self, email, authenticator=None):
        url = self.endpoints['user_by_email'].format(email=email)
        return self.delete(url=url, authenticator=authenticator)

    def flag_user_email_as_verified_or_not(self, email, verified, authenticator=None):
        url = self.endpoints['user_by_email'].format(email=email)
        data = {"is_verified": verified}
        return self.patch(url=url, data=data, authenticator=authenticator)
