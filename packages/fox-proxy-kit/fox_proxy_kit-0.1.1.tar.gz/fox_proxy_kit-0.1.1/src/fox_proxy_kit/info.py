"""DTO класс для хранения информации о прокси."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class ProxyInfo:
    """DTO класс для хранения информации о прокси после проверки."""
    
    ip: Optional[str] = None
    geo: Optional[str] = None  # Геолокация в формате "lat,lon"
    city: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    region: Optional[str] = None
    region_code: Optional[str] = None
    timezone: Optional[str] = None
    isp: Optional[str] = None
    org: Optional[str] = None
    asn: Optional[str] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)  # Полные данные от API
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """
        Обновляет поля из словаря с данными от API.
        
        Args:
            data: Словарь с данными от API сервиса
        """
        self.raw_data = data
        
        # Стандартизация полей из различных API
        self.ip = data.get("ip") or data.get("query") or data.get("origin")
        
        # Геолокация
        lat = data.get("latitude") or data.get("lat")
        lon = data.get("longitude") or data.get("lng") or data.get("lon")
        if lat is not None and lon is not None:
            self.geo = f"{lat},{lon}"
        
        # Локация
        self.city = data.get("city")
        self.country = data.get("country") or data.get("country_name")
        self.country_code = data.get("country_code") or data.get("countryCode")
        self.region = data.get("region") or data.get("regionName")
        self.region_code = data.get("region_code") or data.get("regionCode")
        self.timezone = data.get("timezone") or data.get("time_zone")
        
        # Провайдер
        self.isp = data.get("isp")
        self.org = data.get("org") or data.get("organization")
        self.asn = data.get("asn") or data.get("as")

