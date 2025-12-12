import abc


class AbstractAuthenticator(abc.ABC):
    header_name = 'Authorization'
    value = None

    def __init__(self, value):
        self.value = value

    @property
    @abc.abstractmethod
    def header_template(self):
        return ''

    @property
    def headers(self):
        return {
            self.header_name: self.header_template.format(self.value)
        }


class BearerAuthenticator(AbstractAuthenticator):
    header_template = 'Bearer {}'


class SessionSSOAuthenticator(AbstractAuthenticator):
    header_template = 'SSO_SESSION_ID {}'


class AuthenticatorNegotiator:
    def __new__(self, bearer_token=None, sso_session_id=None):
        assert bearer_token or sso_session_id
        if bearer_token:
            return BearerAuthenticator(bearer_token)
        elif sso_session_id:
            return SessionSSOAuthenticator(sso_session_id)
