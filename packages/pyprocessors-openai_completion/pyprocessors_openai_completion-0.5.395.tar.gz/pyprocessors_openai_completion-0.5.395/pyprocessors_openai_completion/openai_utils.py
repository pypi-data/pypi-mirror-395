import os
from logging import Logger

import requests
from openai import OpenAI
from openai.lib.azure import AzureOpenAI
from pymultirole_plugins.util import comma_separated_to_list
from strenum import StrEnum
import time
from openai._base_client import SyncHttpxClientWrapper


class OAuthToken:
    access_token: str = None
    token_expiry: str = None


logger = Logger("pymultirole")
DEFAULT_CHAT_GPT_MODEL = "gpt-4o-mini"
OPENAI_MAX_RETRIES = int(os.getenv("OPENAI_MAX_RETRIES", 2))


def check_litellm_defined():
    LITELLM_OPENAI_API_KEY = os.getenv("LITELLM_OPENAI_API_KEY", None)
    if LITELLM_OPENAI_API_KEY:
        os.environ["OPENAI_API_KEY"] = LITELLM_OPENAI_API_KEY
    LITELLM_OPENAI_API_BASE = os.getenv("LITELLM_OPENAI_API_BASE", None)
    if LITELLM_OPENAI_API_BASE:
        os.environ["OPENAI_API_BASE"] = LITELLM_OPENAI_API_BASE


def get_api_key(prefix, oauth_token):
    if not prefix.startswith("APOLLO"):
        api_key = os.getenv(prefix + "OPENAI_API_KEY")
    elif oauth_token.access_token is None or time.time() + 100 > oauth_token.token_expiry:
        client_id = os.getenv("APOLLO_CLIENT_ID")
        client_secret = os.getenv("APOLLO_CLIENT_SECRET")
        token_url = os.getenv("APOLLO_OAUTH")
        if not client_id or not client_secret or not token_url:
            raise ValueError("Environment variables for OAuth are not set properly.")
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        verify = not prefix.startswith("APOLLO")
        response = requests.post(token_url, data=token_data, verify=verify)
        response.raise_for_status()
        json_response = response.json()
        oauth_token.access_token = json_response['access_token']
        oauth_token.token_expiry = time.time() + json_response.get('expires_in', 3600)
        api_key = oauth_token.access_token
    else:
        api_key = oauth_token.access_token
    return api_key


# Now use default retry with backoff of openai api
def openai_chat_completion(prefix, oauth_token, base_url, **kwargs):
    client = set_openai(prefix, oauth_token, base_url)
    response = client.chat.completions.create(**kwargs)
    return response


def openai_list_models(prefix, oauth_token, base_url, **kwargs):
    def sort_by_created(x):
        if 'created' in x:
            return x['created']
        elif 'created_at' in x:
            return x['created_at']
        elif 'deprecated' in x:
            return x['deprecated'] or 9999999999
        else:
            return x.id

    models = []
    client = set_openai(prefix, oauth_token, base_url, max_retries=10)
    if prefix.startswith("DEEPINFRA"):
        deepinfra_url = client.base_url
        deepinfra_models = {}
        public_models_list_url = f"{deepinfra_url.scheme}://{deepinfra_url.host}/models/list"
        response = requests.get(public_models_list_url,
                                headers={'Accept': "application/json", 'Authorization': f"Bearer {client.api_key}"})
        if response.ok:
            resp = response.json()
            mods = sorted(resp, key=sort_by_created, reverse=True)
            mods = list(
                {m['model_name'] for m in mods if m['type'] == 'text-generation'})
            deepinfra_models.update({m: m for m in mods})

        private_models_list_url = f"{deepinfra_url.scheme}://{deepinfra_url.host}/models/private/list"
        response = requests.get(private_models_list_url,
                                headers={'Accept': "application/json", 'Authorization': f"Bearer {client.api_key}"})
        if response.ok:
            resp = response.json()
            mods = sorted(resp, key=sort_by_created, reverse=True)
            mods = list(
                {m['model_name'] for m in mods if m['type'] == 'text-generation'})
            deepinfra_models.update({m: m for m in mods})

        deployed_models_list_url = f"{deepinfra_url.scheme}://{deepinfra_url.host}/deploy/list/"
        response = requests.get(deployed_models_list_url,
                                headers={'Accept': "application/json", 'Authorization': f"Bearer {client.api_key}"})
        if response.ok:
            resp = response.json()
            mods = sorted(resp, key=sort_by_created, reverse=True)
            mods = list(
                {m['model_name'] for m in mods if m['task'] == 'text-generation' and m['status'] == 'running'})
            deepinfra_models.update({m: m for m in mods})
        models = list(deepinfra_models.keys())
    elif prefix.startswith("AZURE"):
        models = comma_separated_to_list(os.getenv(prefix + "OPENAI_DEPLOYMENT_ID", None))
    elif prefix.startswith("APOLLO"):
        apollo_url = client.base_url
        public_models_list_url = f"{apollo_url}models"
        response = requests.get(public_models_list_url, verify=False,
                                headers={'Accept': "application/json", 'Authorization': f"Bearer {client.api_key}"})
        if response.ok:
            resp = response.json()
            mods = sorted(resp["data"], key=sort_by_created, reverse=True)
            models = list(
                {m['id'] for m in mods})
    else:
        response = client.models.list(**kwargs)
        models = sorted(response.data, key=sort_by_created, reverse=True)
        models = [m.id for m in models]
    return models


def set_openai(prefix, oauth_token, base_url, max_retries=OPENAI_MAX_RETRIES):
    api_key = get_api_key(prefix, oauth_token)
    if prefix.startswith("AZURE"):
        client = AzureOpenAI(
            # This is the default and can be omitted
            api_key=api_key,
            azure_endpoint=base_url,
            api_version=os.getenv(prefix + "OPENAI_API_VERSION", None),
            # azure_deployment=os.getenv(prefix + "OPENAI_DEPLOYMENT_ID", None)
        )
    else:
        # hack to support verify=None for Apollo
        if prefix.startswith("APOLLO"):
            assert base_url is not None
            http_client = SyncHttpxClientWrapper(
                base_url="https://api.openai.com/v1" if base_url is None else base_url,
                verify=False,
            )
        else:
            http_client = None
        client = OpenAI(
            # This is the default and can be omitted
            api_key=api_key,
            base_url=base_url,
            http_client=http_client,
            max_retries=max_retries
        )
    return client


def gpt_filter(m: str):
    return m.startswith('gpt') and not m.startswith('gpt-3.5-turbo-instruct') and 'vision' not in m


def all_filter(m: str):
    return True


def apollo_filter(m: str):
    return 'embed' not in m and 'vision' not in m and 'mock' not in m and 'tts' not in m and 'mock' not in m


NO_DEPLOYED_MODELS = 'no deployed models - check API key'


# @lru_cache(maxsize=None)
def create_openai_model_enum(name, prefix="", base_url=None, key=all_filter):
    chat_gpt_models = []
    default_chat_gpt_model = None
    try:
        chat_gpt_models = [m for m in openai_list_models(prefix, OAuthToken(), base_url) if key(m)]
        if chat_gpt_models:
            default_chat_gpt_model = DEFAULT_CHAT_GPT_MODEL if DEFAULT_CHAT_GPT_MODEL in chat_gpt_models else \
                chat_gpt_models[0]
    except BaseException:
        logger.warning("Can't list models from endpoint", exc_info=True)

    if len(chat_gpt_models) == 0:
        chat_gpt_models = [NO_DEPLOYED_MODELS]
    models = [("".join([c if c.isalnum() else "_" for c in m]), m) for m in chat_gpt_models]
    model_enum = StrEnum(name, dict(models))
    default_chat_gpt_model = model_enum(default_chat_gpt_model) if default_chat_gpt_model is not None else None
    return model_enum, default_chat_gpt_model
