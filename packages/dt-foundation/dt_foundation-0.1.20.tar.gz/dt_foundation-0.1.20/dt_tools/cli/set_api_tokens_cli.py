"""
This module creates the token file and stores token(s) used for interface with dt_tools 3rd party entities.

Specifically, tokens required for the follwing services:

    - ipinfo.io
    - weatherapi.com
    - geocode.maps.co

```
poetry run python -m dt_tools.cli.set_api_tokens_cli.py
```

"""
import argparse
import sys
from time import sleep
from typing import List

from loguru import logger as LOGGER

import dt_tools.logger.logging_helper as lh
from dt_tools.misc.api_helper import ApiTokenHelper as api_helper
from dt_tools.misc.helpers import ObjectHelper as oh
from dt_tools.os.project_helper import ProjectHelper


def get_input(text: str, valid_responses: List=None) -> str:
    resp = input(text)
    if valid_responses is not None:
        while resp not in valid_responses:
            resp = input(text)
    return resp

def list_apis():
    LOGGER.info('API Services available')
    LOGGER.info('-----------------------------------------')
    log_level = ''
    idx = 0
    for key, val in api_helper._API_DICT.items():
        entry = oh.dict_to_obj(val)
        has_token = api_helper.get_api_token(key) is not None
        valid = ""
        if has_token:
            valid_token = api_helper.validate_token(key)
            log_level = 'SUCCESS' if valid_token else 'ERROR'
            valid = "(Valid token)" if valid_token else "(Invalid token)"
        else:
            log_level = 'WARNING'
        LOGGER.log(log_level, f'{idx:1} {key} - {entry.desc}')
        LOGGER.log(log_level, f'  Has Token    : {has_token} {valid}')
        LOGGER.info(f'  Sign-up  URL : {entry.token_url}')
        LOGGER.info(f'  Validate URL : {entry.validate_url}')
        LOGGER.info(f'  Limits       : {entry.limits}')
        LOGGER.info(f'  dt_module    : {entry.module}')
        LOGGER.info('')
        idx += 1

def select_api() -> str:
    num_services = len(api_helper._API_DICT)
    choices = []
    for i in range(num_services):
        choices.append(str(i))
    choices.append('99')

    resp = int(get_input(f'What service to set API for? (0-{num_services-1} or 99 to exit) > ', valid_responses=choices))
    key = None
    if resp != 99:
        key = list(api_helper._API_DICT.keys())[resp]

    return key

def manage_token(api_key: str) -> str:
    rc = 0
    entry = api_helper.get_api_service_definition(api_key)
    if entry is None:
        raise ValueError(f'Unknown API service: {api_key}')
    LOGGER.info('')
    LOGGER.info('-'*90)
    LOGGER.info('')
    LOGGER.info(f'Service  : {api_key} - {entry["desc"]}')
    LOGGER.info(f'Token URL: {entry["token_url"]}')
    LOGGER.info('')
    LOGGER.warning('NOTE:')
    LOGGER.info(f'  The token is stored locally in {api_helper._DT_TOOLS_TOKENS_LOCATION}.')
    LOGGER.info(f'         format: {{"{api_key}": "xxxxxxxxxxxxxx"}}')
    LOGGER.info('')

    old_token = api_helper.get_api_token(api_key) 
    if old_token is None:
        prompt = 'Continue (y/n) > '
    else:
        prompt = 'Token exists, overwrite? > '

    if get_input(prompt, ['y', 'n']) == 'y':
        token = get_input('Token > ')
        if len(token.strip()) == 0:
            LOGGER.warning('  Empty token, did not save.')
            rc = 2
        else:
            if api_helper.save_api_token(api_key, token):
                if api_helper.can_validate(api_key):
                    if api_helper.validate_token(api_key):
                        LOGGER.success('Token saved.')
                    else:
                        if old_token is None:
                            api_helper.save_api_token(api_key, None)
                            rc = 3
                        else:
                            api_helper.save_api_token(api_key, old_token)
                            rc = 4
                        LOGGER.warning(f'Token not valid, not saved. ({rc})')
        LOGGER.info('')
    
    return rc

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', action='store_true', default=False, help='List API information.')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose (debug) logging.')
    args = parser.parse_args()
    log_level = 'DEBUG' if args.verbose else 'INFO'
    lh.configure_logger(log_level=log_level, brightness=False)

    rc = 0
    version = ProjectHelper.determine_version('dt-foundation')
    LOGGER.info('')
    LOGGER.info('-'*95)
    LOGGER.info(f' dt_tools Token Manager (v{version})')
    LOGGER.info('-'*95)
    LOGGER.info('')
    LOGGER.info('To enable the dt_tools and packages for a specific service, a one-time process is necessary')
    LOGGER.info('to aquire a FREE API token.  Once aquired, this process will save it locally for future use.')
    LOGGER.info('')
    LOGGER.info('To get a token for a specific service, go the the sign-up URL (below) and follow the process')
    LOGGER.info('for creating an API token.  Provide the token here and it will be cached.')
    LOGGER.info('')
    LOGGER.info('If you already have a token, but forget what it is, you may log back into the service provider')
    LOGGER.info('and retrieve your token.')
    LOGGER.info('')
    LOGGER.info('-'*95)
    sleep(3)

    if args.list:
        list_apis()
    else:
        list_apis()
        api_key = select_api()
        if api_key is None:
            LOGGER.warning('  No API selected.')
            rc = 1
        else:
            rc = manage_token(api_key)

    return rc


if __name__ == "__main__":
    sys.exit(main())
    # manage_token()
