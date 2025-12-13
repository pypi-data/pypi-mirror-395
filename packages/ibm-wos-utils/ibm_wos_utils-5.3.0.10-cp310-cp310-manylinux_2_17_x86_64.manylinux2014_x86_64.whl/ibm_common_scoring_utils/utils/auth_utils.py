
# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# © Copyright IBM Corp. 2022, 2024  All Rights Reserved.
# US Government Users Restricted Rights -Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import os
import json
import jwt
import base64

from http import HTTPStatus
from requests.auth import HTTPBasicAuth

from ibm_common_scoring_utils.utils.rest_util import RestUtil
from ibm_common_scoring_utils.utils.scoring_utils_logger import ScoringUtilsLogger
from ibm_common_scoring_utils.utils.constants import AuthProvider
from ibm_common_scoring_utils.utils.lru_cache import LRUCache

logger = ScoringUtilsLogger(__name__)

token_cache = LRUCache(1000)


def get_iam_token(apikey, iam_provider=AuthProvider.CLOUD.value, auth_url=None):
    # Try to get the token from lru cache
    try:
        token = token_cache.get(base64.b64encode(apikey.encode('ascii')))
        if token is not None:
            jwt.decode(token, options={
                       "verify_signature": False, "verify_exp": True})
            return token
    except jwt.ExpiredSignatureError:
        logger.log_warning(
            "Cached token has expired. New token will be generated")
        pass
    try:
        # Invoke token generation method based on the auth provider
        if iam_provider in [AuthProvider.CLOUD.value, AuthProvider.CLOUD_REMOTE.value]:  # Cloud
            if auth_url is None:
                auth_url = "https://iam.cloud.ibm.com" # Consider Production by default
            token = _get_classic_token(apikey, auth_url)

        elif iam_provider in [AuthProvider.MCSP.value, AuthProvider.MCSP_REMOTE.value]:  # MCSP
            if auth_url is None:
                auth_url = "https://account-iam.platform.saas.ibm.com" # Consider Production by default
            token = _get_mcsp_token(apikey, auth_url)

        else:
            raise Exception(f"Invalid IAM Provider / WML Location : {str(ex)}")
        # Cache and return the new token
        token_cache[base64.b64encode(apikey.encode('ascii'))] = token
        return token

    except Exception as ex:
        raise Exception(f"Error while generating IAM token. Reason: {str(ex)}")


def get_cp4d_jwt_token(host: str, username: str, apikey: str = None):
    # Try to get the token from lru cache
    try:
        token = token_cache.get(base64.b64encode(apikey.encode('ascii')))
        if token is not None:
            jwt.decode(token, options={
                       "verify_signature": False, "verify_exp": True})
            return token
    except jwt.ExpiredSignatureError:
        logger.log_warning(
            "Cached token has expired. New token will be generated")
        pass

    # Generate a new token as the token is either not cached before or expired
    auth_url = f"{host}/icp4d-api/v1/authorize"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "username": username,
        "api_key": apikey
    }
    try:
        response = RestUtil.request(additional_retry_status_codes=[HTTPStatus.TOO_MANY_REQUESTS.value], method_list=[
                                    "POST"]).post(url=auth_url, data=json.dumps(data), headers=headers, verify=False)
        response_json = json.loads(response.text)
    except Exception as ex:
        msg = f"Error while generation cp4d jwt token.Reason:{str(ex)}"
        raise Exception(msg)

    token = response_json.get("token")

    # Cache the token
    token_cache[base64.b64encode(apikey.encode('ascii'))] = token

    return token


def get_cp4d_impersonated_token(host: str, uid: str, zen_service_broker_secret: str, username: str = None):
    # Try to get the token from lru cache
    try:
        token = token_cache.get(base64.b64encode(uid.encode('ascii')))
        if token is not None:
            jwt.decode(token, options={
                       "verify_signature": False, "verify_exp": True})
            return token
    except jwt.ExpiredSignatureError:
        logger.log_warning(
            "Cached token has expired. New token will be generated")
        pass

    # Generate a new token as the token is either not cached before or expired
    uname = username if username else f"WOS_{uid}"
    auth_url = "{}/zen-data/internal/v1/service_token?uid={}&username={}&expiration_time=60".format(
        host, uid, uname)
    headers = {
        "secret": zen_service_broker_secret,
        "Accept": "application/json"
    }
    try:
        response = RestUtil.request(additional_retry_status_codes=[
                                    HTTPStatus.TOO_MANY_REQUESTS.value]).get(url=auth_url, headers=headers, verify=False)
        response_json = json.loads(response.text)
    except Exception as ex:
        msg = f"Error while generation cp4d impersonated token.Reason:{str(ex)}"
        raise Exception(msg)

    token = response_json.get("token")

    # Cache the token based on uid
    token_cache[base64.b64encode(uid.encode('ascii'))] = token

    return token

# WI 51904  Method to create token based on the auth provider (Used for custom provider)
def generate_iam_token_with_authprovider(apikey,auth_provider, auth_url=None):
    # Try to get the token from lru cache
    try:
        token = token_cache.get(base64.b64encode(apikey.encode('ascii')))
        if token is not None:
            jwt.decode(token, options={
                       "verify_signature": False, "verify_exp": True})
            return token
    except jwt.ExpiredSignatureError:
        logger.log_warning(
            "Cached token has expired. New token will be generated")
        pass

    try:
        # Invoke token generation method based on the auth provider
        if auth_provider in [AuthProvider.CLOUD.value, AuthProvider.CLOUD_REMOTE.value]:  # Cloud
            if auth_url is None:
               auth_url = "https://iam.cloud.ibm.com" # Consider Production by default
            token = _get_classic_token(apikey, auth_url)
        elif auth_provider in [AuthProvider.MCSP.value, AuthProvider.MCSP_REMOTE.value]:  # MCSP
            if auth_url is None:
                auth_url = "https://account-iam.platform.saas.ibm.com" # Consider Production by default
            token = _get_mcsp_token(apikey, auth_url)
        else:
            raise ValueError("Auth provider is required but was not provided or is null.")

        # Cache and return the new token
        token_cache[base64.b64encode(apikey.encode('ascii'))] = token
        return token

    except Exception as ex:
        raise Exception(f"Error while generating IAM token. Auth provider: {auth_provider}, Auth URL: {auth_url}, Reason: {str(ex)}")

def _get_classic_token(apikey, auth_url):
    """Get token using Classic IAM provider."""
    url = f"{auth_url}/oidc/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": apikey
    }

    response = RestUtil.request(
        additional_retry_status_codes=[HTTPStatus.TOO_MANY_REQUESTS.value],
        method_list=["POST"]
    ).post(url, data=data, headers=headers, auth=HTTPBasicAuth("bx", "bx"))

    if not response.ok:
        raise Exception(
            f"IAM token generation failed with status code: {response.status_code}. "
            f"Reason: {response.reason}"
        )

    return response.json()["access_token"]


def _get_mcsp_token(apikey, auth_url):
    url = f"{auth_url}/api/2.0/apikeys/token"
    """Get token using MCSP IAM provider."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {"apikey": apikey}

    response = RestUtil.request(
        additional_retry_status_codes=[HTTPStatus.BAD_GATEWAY.value,
                                       HTTPStatus.SERVICE_UNAVAILABLE.value, HTTPStatus.GATEWAY_TIMEOUT.value],
        method_list=["POST"]
    ).post(
        url, headers=headers, json=payload, verify=False
    )

    if not response.ok:
        raise Exception(
            f"IAM token generation failed with status code: {response.status_code}. "
            f"Reason: {response.reason}"
        )

    return response.json()["token"]
