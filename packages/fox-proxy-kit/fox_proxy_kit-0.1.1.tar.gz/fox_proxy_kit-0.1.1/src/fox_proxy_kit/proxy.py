"""Proxy DTO класс с методами проверки IP и геолокации."""

import httpx
import asyncio
from typing import Optional, List, Callable, Awaitable, Dict, Any

from .info import ProxyInfo
from .config import IP_CHECK_URLS, IP_GEO_CHECK_URLS, get_random_url


class Proxy:
    """DTO класс для работы с прокси."""
    
    def __init__(
        self,
        protocol: str,
        host: str,
        port: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        rotation_url: Optional[str] = None,
        rotation_func: Optional[Callable[[], Awaitable[bool]]] = None
    ):
        """
        Инициализация прокси.
        
        Args:
            protocol: Протокол (http, https, socks5)
            host: Хост прокси
            port: Порт прокси
            username: Имя пользователя (опционально)
            password: Пароль (опционально)
            rotation_url: URL для ротации прокси (опционально)
            rotation_func: Асинхронная функция для ротации прокси (опционально).
                          Функция ДОЛЖНА принимать **kwargs с данными прокси.
                          Должна возвращать bool (True если ротация успешна)
        """
        self.protocol = protocol.lower()
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password
        self.rotation_url = rotation_url
        self.__rotation_func = rotation_func
        self.info = ProxyInfo()
        
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
        func = rotation_func or self.__rotation_func
        
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
        """Строковое представление прокси."""
        return f"Proxy(protocol={self.protocol}, host={self.host}, port={self.port})"

