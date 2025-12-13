"""Константы с URL API сервисов для проверки IP и геолокации."""

import random
from typing import List, Optional

# URL для проверки IP (только IP адрес)
IP_CHECK_URLS = [
    "https://api.ipify.org?format=json",
    "https://api64.ipify.org?format=json",
    "https://ipinfo.io/json",
    "https://api.myip.com",
    "https://ip.seeip.org/json",
]

# URL для проверки IP и геолокации
IP_GEO_CHECK_URLS = [
    "https://ipapi.co/json/",
    "https://ipinfo.io/json",
    "https://ipwho.is/",
]


def get_random_url(urls: Optional[List[str]] = None, default_urls: List[str] = None) -> str:
    """
    Возвращает случайный URL из списка.
    
    Args:
        urls: Опциональный список URL от пользователя
        default_urls: Список URL по умолчанию
        
    Returns:
        Случайный URL из переданного списка или списка по умолчанию
    """
    if urls:
        return random.choice(urls)
    if default_urls:
        return random.choice(default_urls)
    raise ValueError("Не указаны URL для запроса")

