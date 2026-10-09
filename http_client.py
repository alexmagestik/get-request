import requests
from typing import Optional, Dict, Any


def get(url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 10) -> Any:
    """
    Выполняет GET-запрос по указанному URL с базовой проверкой статуса.
    
    Args:
        url (str): URL для запроса
        params (dict, optional): Параметры запроса
        timeout (int, optional): Таймаут в секундах. По умолчанию 10.
    
    Returns:
        dict or str: Ответ сервера в формате JSON (если возможно) или текст
    """
    response = requests.get(url, params=params, timeout=timeout)
    
    # Базовая проверка статуса
    response.raise_for_status()
    
    # Пытаемся вернуть JSON, если возможно
    try:
        return response.json()
    except Exception:
        return response.text


def post(url: str, data: Optional[Dict[str, Any]] = None, 
         json_data: Optional[Dict[str, Any]] = None, 
         timeout: int = 10) -> Any:
    """
    Выполняет POST-запрос по указанному URL с базовой проверкой статуса.
    """
    response = requests.post(url, data=data, json=json_data, timeout=timeout)
    response.raise_for_status()
    try:
        return response.json()
    except Exception:
        return response.text
