"""Глобальная конфигурация для API сервисов проверки IP и геолокации."""

import random
from typing import List, Optional
from .api_services import IPService, IPGeoService


class ProxyConfig:
    """Глобальный объект конфигурации для API сервисов."""
    
    def __init__(self):
        """Инициализация конфигурации с дефолтными сервисами."""
        # Дефолтные сервисы из Enum
        self._ip_services: List[str] = IPService.get_all_urls()
        self._geo_services: List[str] = IPGeoService.get_all_urls()
    
    @property
    def ip_services(self) -> List[str]:
        """
        Возвращает список IP сервисов.
        
        Returns:
            Список URL IP сервисов
        """
        return self._ip_services.copy()
    
    @property
    def geo_services(self) -> List[str]:
        """
        Возвращает список Geo сервисов.
        
        Returns:
            Список URL Geo сервисов
        """
        return self._geo_services.copy()
    
    def add_ip_service(self, url: str) -> None:
        """
        Добавляет кастомный IP сервис.
        
        Args:
            url: URL сервиса для проверки IP
        """
        if url not in self._ip_services:
            self._ip_services.append(url)
    
    def add_geo_service(self, url: str) -> None:
        """
        Добавляет кастомный Geo сервис.
        
        Args:
            url: URL сервиса для проверки IP и геолокации
        """
        if url not in self._geo_services:
            self._geo_services.append(url)
    
    def add_ip_services(self, urls: List[str]) -> None:
        """
        Добавляет список кастомных IP сервисов.
        
        Args:
            urls: Список URL сервисов для проверки IP
        """
        for url in urls:
            self.add_ip_service(url)
    
    def add_geo_services(self, urls: List[str]) -> None:
        """
        Добавляет список кастомных Geo сервисов.
        
        Args:
            urls: Список URL сервисов для проверки IP и геолокации
        """
        for url in urls:
            self.add_geo_service(url)
    
    def set_ip_services(self, urls: List[str]) -> None:
        """
        Заменяет список IP сервисов.
        
        Args:
            urls: Новый список URL сервисов для проверки IP
        """
        self._ip_services = list(urls)
    
    def set_geo_services(self, urls: List[str]) -> None:
        """
        Заменяет список Geo сервисов.
        
        Args:
            urls: Новый список URL сервисов для проверки IP и геолокации
        """
        self._geo_services = list(urls)
    
    def get_random_ip_service(self) -> str:
        """
        Возвращает случайный IP сервис из списка.
        
        Returns:
            Случайный URL IP сервиса
        """
        if not self._ip_services:
            raise ValueError("Список IP сервисов пуст")
        return random.choice(self._ip_services)
    
    def get_random_geo_service(self) -> str:
        """
        Возвращает случайный Geo сервис из списка.
        
        Returns:
            Случайный URL Geo сервиса
        """
        if not self._geo_services:
            raise ValueError("Список Geo сервисов пуст")
        return random.choice(self._geo_services)
    
    def clear_ip_services(self) -> None:
        """Очищает список IP сервисов."""
        self._ip_services.clear()
    
    def clear_geo_services(self) -> None:
        """Очищает список Geo сервисов."""
        self._geo_services.clear()
    
    def reset_to_defaults(self) -> None:
        """Сбрасывает конфигурацию к дефолтным значениям."""
        self._ip_services = IPService.get_all_urls()
        self._geo_services = IPGeoService.get_all_urls()


# Глобальный объект конфигурации
proxy_config = ProxyConfig()

