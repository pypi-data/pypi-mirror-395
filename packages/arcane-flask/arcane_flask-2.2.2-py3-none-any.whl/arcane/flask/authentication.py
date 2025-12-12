import functools
import inspect
import time
import json
from typing import Callable, Optional, Union, Dict
import logging

import backoff
from firebase_admin import auth as firebase_auth
from flask import request
from pydash import get
from google.cloud.exceptions import ServiceUnavailable

from arcane.core import CLIENTS_PARAM, ALL_CLIENTS_RIGHTS, RightsLevelEnum, GOOGLE_EXCEPTIONS_TO_RETRY, BadRequestError
from arcane.datastore import Client as DatastoreClient
from arcane.pubsub import Client as PubSubClient
import concurrent.futures

from .tracking import send_tracking_information

CLIENTS_KIND = 'base-clients'
USERS_KIND = 'users'

rights_mapper = {
    '0': "None",
    '1': "Viewer",
    '2': "Editor",
    '3': "Admin"
}

class IncorrectAccessRightsRouteImplementation(TypeError):
    pass

def check_access_rights(service: str,
                        required_rights: int,
                        service_user_right: str,  # should be something like ValueOf[UserRightsEnum]
                        datastore_client: DatastoreClient,
                        pubsub_client: PubSubClient,
                        kwargs_name_and_path_to_get: Dict[str, str] = {},
                        receive_rights_per_client: bool=False,
                        auth_enabled: bool=True,
                        project: str = None,
                        timeout: Optional[int] = None,
                        ) -> Callable[[Callable], Callable]:
    """
    This functions checks the authorizations from the current HTTP call.
    /!\ Must be the last decorator (right above the decorated function) when there are multiples decorators on
    a function in order to get job_func_signature.
    if receive_rights_per_client is set to True, function must accept an argument corresponding to CLIENTS_PARAM either
    as the last positional argument or as an named argument.
    :param kwargs_name_and_path_to_get: A dictionnary where the key is the name of the key we want to store the kwarg as and the value is the path to the value in the args ('test.value').
    """
    if required_rights == RightsLevelEnum.NONE and not receive_rights_per_client:
        def dummy_check_rights(job_func: Callable) -> Callable:
            return job_func
        return dummy_check_rights

    def check_rights(job_func: Callable) -> Callable:

        if receive_rights_per_client:
            error_message_clients = \
                "CHECK_ACCESS_RIGHTS incompatibility:\n" \
                f'function {job_func.__name__} should have an explicit argument "{CLIENTS_PARAM}' \
                "if receive_rights_per_client is set to True. \n"\
                "The argument must either be the last positional argument or a named argument"
            job_func_signature = inspect.getfullargspec(job_func)
            if (not job_func_signature.args or CLIENTS_PARAM != job_func_signature.args[-1]) \
                    and CLIENTS_PARAM not in job_func_signature.kwonlyargs:
                if CLIENTS_PARAM in job_func_signature.args:
                    error_message_clients += f'\n {CLIENTS_PARAM} is present in positional argument but not in last position.'
                raise IncorrectAccessRightsRouteImplementation(error_message_clients)

        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            start = time.time()
            is_appengine_cron = request.headers.get('X-Appengine-Cron', False)

            if is_appengine_cron:
                logging.info("App Engine calls service : " + service)
                return job_func(*args, **kwargs)

            claims = {}
            origin = ''
            # Check feature rights
            if auth_enabled:
                token = str(request.headers.get('Authorization', '')).split(' ').pop()
                origin = str(request.headers.get('origin', ''))
                try:
                    claims = verify_token(token)
                except (firebase_auth.ExpiredIdTokenError,
                        firebase_auth.RevokedIdTokenError,
                        firebase_auth.InvalidIdTokenError) as e:
                    if required_rights != RightsLevelEnum.NONE:
                        return {'detail': 'You don\'t have access to Adscale resources\n', 'firebase_log': str(e)}, 401
                except ValueError as e:
                    return {'detail': str(e)}, 401

                try:
                    _check_feature_right_access(
                        claims,
                        required_rights,
                        service_user_right
                    )
                except BadRequestError:
                    rights = _get_level_access_for_a_feature_from_claims(claims, service_user_right)
                    return {'detail': f"You don't have access to this resource : your rights are "
                            f"'{rights_mapper.get(str(rights), '0')}' for service '{service}'. "
                            f"You need '{rights_mapper.get(str(required_rights), '0')}'.",
                            'claims': f"Your current rights are {json.dumps(claims, indent=4, sort_keys=True)}"}, 401

            # Fill authorized_clients
            if receive_rights_per_client:
                if not auth_enabled:
                    authorized_clients = [ALL_CLIENTS_RIGHTS]
                else:
                    # Value defined for service to service calls
                    service_authorized_clients = claims.get('authorized_clients')
                    db_user_id = claims.get('db_user_id')
                    if service_authorized_clients and not db_user_id:
                        authorized_clients = service_authorized_clients
                    else:
                        if not db_user_id:
                            authorized_clients = []
                        else:
                            user = datastore_client.get_entity(USERS_KIND, int(db_user_id))
                            if user is None:
                                authorized_clients = []
                            else:
                                authorized_clients = user.get('authorized_clients', [])

                if ALL_CLIENTS_RIGHTS in authorized_clients:
                    authorized_clients.remove(ALL_CLIENTS_RIGHTS)
                    clients_query = datastore_client.query()
                    clients_query.kind = CLIENTS_KIND
                    clients_query.keys_only()
                    authorized_clients = [client_entity.key.name for client_entity in clients_query.fetch()]

                kwargs[CLIENTS_PARAM] = sorted(set(authorized_clients))
            try:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(job_func, *args, **kwargs)
                    func_response = future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                func_response = {'detail': 'Request Timeout'}, 504
            except Exception as e:
                func_response = {'detail': f'Server Error: {str(e)}'}, 500

            end = time.time()

            additionnal_info = {}
            for key, path in kwargs_name_and_path_to_get.items():
                additionnal_info[key] = get(kwargs, path)
            if len(additionnal_info.keys()) == 0:
                additionnal_info = None

            if auth_enabled:
                status_code = 200
                if type(func_response) == tuple and type(func_response[1]) == int and func_response[1] >= 100 and func_response[1] < 599:
                    status_code = func_response[1]
                elif type(func_response) == int and func_response >= 100 and func_response < 599:
                    status_code = func_response

                try:
                    send_tracking_information(
                        email=claims['email'],
                        service=service,
                        function_name=job_func.__name__,
                        origin=origin,
                        project=project,
                        execution_time=end - start,
                        additionnal_info=additionnal_info,
                        status_code=status_code,
                        pubsub_client=pubsub_client,
                        datastore_client=datastore_client)
                except (KeyError, ServiceUnavailable):
                    # Failing to send tracking info should not impact feature usability
                    pass

            return func_response

        return wrapper
    return check_rights


@backoff.on_exception(backoff.expo, (GOOGLE_EXCEPTIONS_TO_RETRY), max_tries=3)
def verify_token(token: str) -> Dict:
    claims = firebase_auth.verify_id_token(token)
    return claims


def check_feature_right_of_authenticated_user(
    required_rights: int,
    service_user_right: str,
    auth_enabled: bool=True
):
    # Check feature rights
    if not auth_enabled:
        return
    claims = {}
    try:
        token = str(request.headers.get('Authorization', '')).split(' ').pop()
        claims = verify_token(token)
    except (firebase_auth.ExpiredIdTokenError,
            firebase_auth.RevokedIdTokenError,
            firebase_auth.InvalidIdTokenError) as e:
        if required_rights != RightsLevelEnum.NONE:
            raise BadRequestError('You don\'t have access to Adscale resources\n')
    except ValueError as e:
        raise BadRequestError(str(e))

    _check_feature_right_access(
        claims,
        required_rights,
        service_user_right
    )



def _check_feature_right_access(
    claims: Dict,
    required_rights: int,
    service_user_right: str,
):
    rights = _get_level_access_for_a_feature_from_claims(claims, service_user_right)
    if rights < required_rights:
        raise BadRequestError("You don't have access to this resource")


def _get_level_access_for_a_feature_from_claims(
    claims: Dict,
    service_user_right: str
):
    return claims.get('features_rights', {}).get(service_user_right, RightsLevelEnum.NONE)


def get_user_email(token: str=None, auth_enabled=True) -> Union[str, None]:
    """
    retrieves user id from connexion header.
    may raise ValueError if Authorization token is invalid or if token did not have uid specified
    """
    if not auth_enabled:
        # To prevent errors in dev env
        return None
    if token is None:
        token = request.headers.get('Authorization', '').split(' ').pop()
        if not token:
            raise ValueError(f"Failed to retrieve token from http header from token {request.headers.get('Authorization', '')}")
    claims = firebase_auth.verify_id_token(token)
    try:
        mail_str = claims['email']
    except KeyError as e:
        raise ValueError('Failed to retrieve uid from token') from e
    if not isinstance(mail_str, str):
        raise ValueError(f'Uid key is mapped to {repr(mail_str)} (type: {type(mail_str)}) value in claims')
    return mail_str

def get_user_uid(token: Optional[str]=None) -> str:
    """
    Retrieve user firebase uid from connexion header.

    Arguments:
        token {AnyStr} -- Token provided by the connexion header

    Raises:
        ValueError -- If we failed to retrieve token

    Returns:
        [str] -- user uid
    """

    if token is None:
        token = request.headers.get('Authorization', '').split(' ').pop()
        if token == "":
            return "No uid provided"
    claims = firebase_auth.verify_id_token(token)

    return claims['uid']
