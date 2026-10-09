import os
from typing import Dict, Any
from dotenv import load_dotenv
import requests

load_dotenv()


def get_country_info(country_name: str) -> Dict[str, Any]:
    api_key = os.getenv('RC_API_KEY')
    url = "https://api.restcountries.com/countries/v5"
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    params = {"q": country_name}
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    try:
        return response.json()
    except Exception:
        return {"data": response.text}
