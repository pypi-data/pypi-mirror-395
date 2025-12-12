import json
import pathlib
from typing import Dict, List, Union

import requests
from loguru import logger as LOGGER


class ApiTokenHelper():
    """
    Manage dt_tools* 3rd Party API interface tokens.

    """
    _DT_TOOLS_TOKENS_LOCATION=pathlib.Path('~').expanduser().absolute() / ".dt_tools" / "api_tokens.json"
    
    API_IP_INFO = 'ipinfo.io'
    API_WEATHER_INFO = 'weatherapi.com'
    API_GEOLOCATION_INFO = 'geocode.maps.co'
    
    _API_DICT = {
        "ipinfo.io": {
            "desc": "IP Address information API",
            "package": "dt-net",
            "module": "dt_tools.net.ip_helper",
            "token_url": "https://ipinfo.io/missingauth",
            "validate_url": "https://ipinfo.io/8.8.8.8?token={token}",
            "limits": "50,000/month, ~1,600/day"
        },
        "weatherapi.com": {
            "desc": "Weather API (current, forecasts, alerts)",
            "package": "dt-misc",
            "module": "dt_tools.misc.weather",
            "token_url": "https://www.weatherapi.com/signup.aspx",
            "validate_url": "http://api.weatherapi.com/v1/ip.json?key={token}&q=auto:ip",
            "limits": "1,000,000/month, ~32,000/day"
        },
        "geocode.maps.co": {
            "desc": "GeoLocation API (Lat, Lon, Address, ...)",
            "package": "dt-misc",
            "module": "dt_tools.misc.geoloc",
            "token_url": "https://geocode.maps.co/join/",
            "validate_url": "https://geocode.maps.co/reverse?lat=0&lon=0&api_key={token}",
            "limits": "5,000/day, throttle 1 per sec"
        }
    }
    
    @classmethod
    def _get_tokens_dictionary(cls) -> Dict[str, dict]:
        cls._DT_TOOLS_TOKENS_LOCATION.parent.mkdir(parents=True, exist_ok=True)
        token_dict = {}
        if cls._DT_TOOLS_TOKENS_LOCATION.exists():
            token_dict = json.loads(cls._DT_TOOLS_TOKENS_LOCATION.read_text())
        return token_dict
    
    @classmethod
    def get_api_token(cls, service_id: str) -> str:
        """
        Get token for API service_id

        Args:
            service_id (str): Service identifier (see get_api_services())

        Raises:
            NameError: If the service name is not valid.

        Returns:
            str: API token for target service or None if not in token cache.
        """
        if cls._API_DICT.get(service_id, None) is None:
            raise NameError(f'Not a valid service: {service_id}')
        
        t_dict = cls._get_tokens_dictionary()
        token = t_dict.get(service_id, None)
        return token

    @classmethod
    def save_api_token(cls, service_id: str, token: str) -> bool:
        """
        Save the API Token for the service.

        Args:
            service_id (str): Target service id.
            token (str): Token string.

        Returns:
            bool: True if saved, False if there was an error.
        """
        saved = True
        t_dict = cls._get_tokens_dictionary()
        t_dict[service_id] = token
        token_str = json.dumps(t_dict)
        try:
            cls._DT_TOOLS_TOKENS_LOCATION.write_text(token_str)
        except Exception as ex:
            LOGGER.error(f'Unable to save token for {service_id} - {repr(ex)}')
            saved = False

        return saved
    
    @classmethod
    def get_api_service_ids(cls) -> List[str]:
        """
        Return a list of the API service ids.

        Returns:
            List[str]: List of API service ids.
        """
        t_dict = cls._get_tokens_dictionary()
        return list(t_dict.keys())

    @classmethod
    def get_api_service_definition(cls, service_id: str) -> Union[Dict, None]:
        """
        Return a dictionary of the API Service.

        Args:
            api_key (str): Service ID of requested service.

        Returns:

            Union[Dict, None]: Service definition as a dict if found, else None.

            Format:: 
            
                <service_id1>: {
                    "desc": "Service description",
                    "package": "dt-xxxxx",
                    "module": "dt_tools.xxx.xxxx",
                    "token_url": "https://xxxxxx",
                    "validate_url": "https://xxxxxx/yyyyy",
                    "limits": "Limit description",
                    "enabled": True
                }

        """
        return cls._API_DICT.get(service_id, None)
    
    @classmethod
    def can_validate(cls, service: str) -> bool:
        """
        Ensure service setup is valid.

        Args:
            service_id (str): Target service_id.

        Returns:
            bool: True if service is setup False if invalid name or missing token.
        """
        t_service:dict = cls._API_DICT.get(service, {})
        valid_service = t_service.get('validate_url', None) is not None
        if valid_service:
            LOGGER.debug(f'{service} is a valid service name')
            valid_service = cls.get_api_token(service) is not None
            if valid_service:
                LOGGER.debug(f'{service} has a token.')
            else:
                LOGGER.debug(f'{service} does NOT have a token.')
        else:
            LOGGER.debug(f'{service} is NOT a valid service name')

        return valid_service

    @classmethod
    def validate_token(cls, service_id: str) -> bool:
        """
        Validate service token.

        Args:
            service_id (str): Target service_id.

        Returns:
            bool: True if token validates successfully, False if invalid token.
        """
        valid_token = False
        if not cls.can_validate(service_id):
            LOGGER.debug(f'{service_id} is not valid.')
        else:
            entry = cls.get_api_service_definition(service_id)
            try:
                token = cls.get_api_token(service_id)
                url = entry['validate_url'].replace('{token}', token)
                resp = requests.get(url)
                LOGGER.debug(f'Validate: {url}  returns: {resp.status_code}')
                if resp.status_code == 200:
                    valid_token = True
            except Exception as ex:
                LOGGER.debug(f'Validate: {url}  Exception: {repr(ex)}')

        return valid_token
    