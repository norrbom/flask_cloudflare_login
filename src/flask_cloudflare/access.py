from os import getenv
import json
import requests
import jwt
import logging
from .cache import cache


log = logging.getLogger(__name__)


class CfUser():

    def __init__(self, email=None, groups=[]):
        self.id = email
        self.groups = groups

    def __repr__(self):
        return self.id
    
    def __dict__(self):
        return {
            "id": self.id,
            "groups": self.groups
        }

    def __str__(self):
        return str(self.__dict__())
    
    def to_json(self):
        return json.dumps(self.__dict__())

    """
    Methods that Flask-Login expects user objects to have.
    """

    __hash__ = object.__hash__

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No id attribute") from None

    def __eq__(self, other):
        if isinstance(other, CfUser):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


def clear_cache(token, group_filter):
    cache.delete_memoized(get_payload, token)
    cache.delete_memoized(get_groups, token, group_filter)


def __get_public_keys():
    """
    Returns a list of RSA public keys usable by PyJWT.
    """
    CF_CERTS_URL = f"https://{getenv('CF_TEAM_DOMAIN')}/cdn-cgi/access/certs"
    public_keys = []
    log.debug(f'calling {CF_CERTS_URL}')
    try:
        r = requests.get(CF_CERTS_URL)
        jwk_set = r.json()
        for key_dict in jwk_set['keys']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(
                json.dumps(key_dict))
            public_keys.append(public_key)
    except requests.exceptions.HTTPError as http_err:
        log.error(http_err.args[0])
    except Exception as err:
        log.error('An error occurred when fetching cloudflare public keys')
        log.error(str(err))
    return public_keys


def get_token(request):
    if getenv('CF_TEST_TOKEN'):
        return getenv('CF_TEST_TOKEN')
    if request:
        token = ''
        if 'CF_Authorization' in request.cookies:
            token = request.cookies['CF_Authorization']
            return token
        else:
            log.error('CF_Authorization cookie not found')
    return None


# cache result using token as key
@cache.memoize(3600)
def get_payload(token):
    """
    Returns a JWT payload from a validated JWT token

    :param token: The JWT token from Cloudflare
    """
    keys = __get_public_keys()

    # Loop through the keys since we can't pass the key set to the decoder
    valid_token = False
    for key in keys:
        try:
            payload = jwt.decode(
                token, key=key,
                audience=getenv("CF_POLICY_AUD"), algorithms=['RS256']
                )
            valid_token = True
            break
        except Exception:
            pass
    if not valid_token:
        log.error(f"token is not valid: {token}")
        return None
    log.info('token is valid')
    return payload


# cache result using token as key
@cache.memoize(3600)
def get_groups(token, group_filter):
    """
    Returns a list of groups from Cloudflare identity lookup API

    :param token: The JWT token from Cloudflare
    :type token: str
    :param group_filter: a string that filters groups on names using string match
    :type group_filter: str
    """
    groups = []
    CF_IDENTITY_URL = f"https://{getenv('CF_TEAM_DOMAIN')}/cdn-cgi/access/get-identity"
    headers = {"cookie": f"CF_Authorization={token}"}
    log.debug(f"calling {CF_IDENTITY_URL}")
    try:
        r = requests.get(CF_IDENTITY_URL, headers=headers)
        r.raise_for_status()
        for g in r.json()['groups']:
            if group_filter:
                if group_filter in g.get('name'):
                    groups.append(g)
            else:
                groups.append(g)
        log.debug(json.dumps(groups))
        return groups
    except requests.exceptions.HTTPError as http_err:
        log.error(http_err.args[0])
    except Exception as err:
        log.error('An error occurred when fetching cloudflare identity')
        log.error(str(err))
