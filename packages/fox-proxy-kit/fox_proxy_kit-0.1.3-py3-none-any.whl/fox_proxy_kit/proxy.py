"""Proxy DTO класс с методами проверки IP и геолокации."""

import httpx
import asyncio
from dataclasses import dataclass, field
from typing import Optional, List, Callable, Awaitable, Dict, Any

from .info import ProxyInfo
from .config import IP_CHECK_URLS, IP_GEO_CHECK_URLS, get_random_url


@dataclass
class Proxy:
    """DTO класс для работы с прокси."""
    
    protocol: str
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    rotation_url: Optional[str] = None
    rotation_func: Optional[Callable[[], Awaitable[bool]]] = field(default=None, repr=False)
    info: ProxyInfo = field(default_factory=ProxyInfo)
    
    def __post_init__(self):
        """Инициализация после создания dataclass."""
        self.protocol = self.protocol.lower()
        self.port = int(self.port)
        # Формируем полный URL прокси
        self.proxy_url = self.__build_proxy_url()
    
    def __build_proxy_url(self) -> str:
        """Строит полный URL прокси."""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"
    
    def __get_proxy_url(self) -> str:
        """Возвращает URL прокси для httpx."""
        # httpx принимает proxy как строку URL
        return self.proxy_url
    
    async def check_ip(
        self,
        url: Optional[str] = None,
        urls: Optional[List[str]] = None,
        timeout: float = 10.0,
    ) -> ProxyInfo:
        """
        Проверяет IP адрес через прокси.
        
        Args:
            url: Опциональный URL для проверки (если не указан, используется случайный из дефолтных)
            urls: Опциональный список URL для случайного выбора
            timeout: Таймаут запроса в секундах
            verify: Проверять SSL сертификаты (по умолчанию True). Установите False для Burp и других прокси с самоподписанными сертификатами
            
        Returns:
            ProxyInfo объект с информацией о IP
        """
        check_url = get_random_url(urls, IP_CHECK_URLS) if not url else url
        
        try:
            async with httpx.AsyncClient(proxy=self.__get_proxy_url(), timeout=timeout, verify=False) as client:
                response = await client.get(check_url)
                response.raise_for_status()
                data = response.json()
                
                # Обновляем info
                self.info.update_from_dict(data)
                
        except Exception as e:
            # Сохраняем ошибку в raw_data
            self.info.raw_data["error"] = str(e)
            
        return self.info
    
    async def check_ip_geo(
        self,
        url: Optional[str] = None,
        urls: Optional[List[str]] = None,
        timeout: float = 10.0,
    ) -> ProxyInfo:
        """
        Проверяет IP адрес и геолокацию через прокси.
        
        Args:
            url: Опциональный URL для проверки (если не указан, используется случайный из дефолтных)
            urls: Опциональный список URL для случайного выбора
            timeout: Таймаут запроса в секундах
            verify: Проверять SSL сертификаты (по умолчанию True). Установите False для Burp и других прокси с самоподписанными сертификатами
            
        Returns:
            ProxyInfo объект с информацией о IP и геолокации
        """
        check_url = get_random_url(urls, IP_GEO_CHECK_URLS) if not url else url
        
        try:
            async with httpx.AsyncClient(proxy=self.__get_proxy_url(), timeout=timeout, verify=False) as client:
                response = await client.get(check_url)
                response.raise_for_status()
                data = response.json()
                
                # Обновляем info
                self.info.update_from_dict(data)
                
        except Exception as e:
            # Сохраняем ошибку в raw_data
            self.info.raw_data["error"] = str(e)
            
        return self.info
    
    async def rotation(
        self,
        rotation_func: Optional[Callable[[], Awaitable[bool]]] = None,
        delay: float = 2.0,
        max_retries: int = 3
    ) -> bool:
        """
        Выполняет ротацию прокси и проверяет изменение IP.
        
        Args:
            rotation_func: Асинхронная функция для ротации (опционально).
                          Если не передана, используется self.rotation_func.
                          Функция ДОЛЖНА принимать **kwargs с данными прокси:
                          protocol, host, port, username, password, rotation_url, proxy_url.
                          Должна возвращать bool (True если ротация успешна).
            delay: Задержка в секундах перед повторной проверкой IP после ротации
            max_retries: Максимальное количество попыток ротации
            
        Returns:
            True если IP изменился после ротации, False в противном случае
            
        Raises:
            ValueError: Если функция ротации не указана ни в объекте, ни в параметрах
        """
        # Определяем функцию ротации
        func = rotation_func or self.rotation_func
        
        if func is None:
            raise ValueError(
                "Функция ротации не указана. "
                "Передайте rotation_func в метод rotation() или при создании Proxy объекта."
            )
        
        # Проверяем текущий IP
        initial_info = await self.check_ip()
        initial_ip = initial_info.ip
        
        if not initial_ip:
            raise ValueError("Не удалось получить начальный IP адрес")
        
        # Подготавливаем данные для передачи в функцию ротации через **kwargs
        proxy_data = {
            "protocol": self.protocol,
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "rotation_url": self.rotation_url,
            "proxy_url": self.proxy_url
        }
        
        # Пытаемся выполнить ротацию
        for attempt in range(max_retries):
            # Вызываем функцию ротации с передачей данных через **kwargs
            # Функция должна принимать **kwargs
            rotation_success = await func(**proxy_data)
            
            if not rotation_success:
                # Если ротация не удалась, продолжаем попытки
                continue
            
            # Ждем указанную задержку
            await asyncio.sleep(delay)
            
            # Проверяем IP снова
            new_info = await self.check_ip()
            new_ip = new_info.ip
            
            if new_ip and new_ip != initial_ip:
                # IP изменился - ротация успешна
                return True
        
        # Все попытки исчерпаны или IP не изменился
        return False
    
    def __repr__(self) -> str:
        """Строковое представление прокси с заполненными полями."""
        parts = []
        
        # Обязательные поля
        parts.append(f"protocol={self.protocol!r}")
        parts.append(f"host={self.host!r}")
        parts.append(f"port={self.port}")
        
        # Опциональные поля (только заполненные)
        if self.username is not None:
            parts.append(f"username={self.username!r}")
        if self.password is not None:
            parts.append(f"password={self.password!r}")
        if self.rotation_url is not None:
            parts.append(f"rotation_url={self.rotation_url!r}")
        if self.proxy_url:
            parts.append(f"proxy_url={self.proxy_url!r}")
        
        # Информация из info (только заполненные поля)
        info_parts = []
        if self.info.ip:
            info_parts.append(f"ip={self.info.ip!r}")
        if self.info.country:
            info_parts.append(f"country={self.info.country!r}")
        if self.info.city:
            info_parts.append(f"city={self.info.city!r}")
        if self.info.geo:
            info_parts.append(f"geo={self.info.geo!r}")
        if self.info.region:
            info_parts.append(f"region={self.info.region!r}")
        if self.info.timezone:
            info_parts.append(f"timezone={self.info.timezone!r}")
        if self.info.isp:
            info_parts.append(f"isp={self.info.isp!r}")
        if self.info.org:
            info_parts.append(f"org={self.info.org!r}")
        if self.info.asn:
            info_parts.append(f"asn={self.info.asn!r}")
        
        if info_parts:
            parts.append(f"info=ProxyInfo({', '.join(info_parts)})")
        
        return f"Proxy({', '.join(parts)})"

