"""Enum классы для API сервисов проверки IP и геолокации."""

from enum import Enum
from typing import List


class IPService(Enum):
    """API сервисы для проверки только IP адреса (быстрые)."""
    
    IPIFY = "https://api.ipify.org"
    IFCONFIG = "https://ifconfig.me/ip"
    AMAZONAWS = "https://checkip.amazonaws.com"
    ICAHAZIP = "https://icanhazip.com"
    
    @classmethod
    def get_all_urls(cls) -> List[str]:
        """
        Возвращает список всех URL сервисов.
        
        Returns:
            Список URL всех сервисов
        """
        return [service.value for service in cls]
    
    def __str__(self) -> str:
        """Строковое представление сервиса."""
        return self.value


class IPGeoService(Enum):
    """API сервисы для проверки IP адреса и геолокации."""
    
    IPAPI_CO = "https://ipapi.co/json/"
    IP_API_COM = "https://ip-api.com/json/"
    IPINFO = "https://ipinfo.io/json"
    FREEGEOIP = "https://freegeoip.app/json/"
    IPGEOLOCATION = "https://api.ipgeolocation.io/ipgeo?apiKey=free"
    
    @classmethod
    def get_all_urls(cls) -> List[str]:
        """
        Возвращает список всех URL сервисов.
        
        Returns:
            Список URL всех сервисов
        """
        return [service.value for service in cls]
    
    def __str__(self) -> str:
        """Строковое представление сервиса."""
        return self.value

