"""Proxy DTO класс с методами проверки IP и геолокации."""

import httpx
import asyncio
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Callable, Awaitable, Dict, Any, Union

from .info import ProxyInfo
from .config import proxy_config

# Настройка логгера
logger = logging.getLogger(__name__)


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
        timeout: float = 10.0,
        verify: bool = True
    ) -> bool:
        """
        Проверяет IP адрес через прокси.
        
        Использует случайный сервис из глобальной конфигурации proxy_config.
        
        Args:
            timeout: Таймаут запроса в секундах
            verify: Проверять SSL сертификаты (по умолчанию True). 
                   Установите False для Burp и других прокси с самоподписанными сертификатами
            
        Returns:
            True если проверка успешна, False в противном случае
            
        Raises:
            httpx.HTTPError: При ошибках HTTP запроса
            httpx.TimeoutException: При превышении таймаута
            Exception: При других ошибках
        """
        check_url = proxy_config.get_random_ip_service()
        logger.debug(f"Проверка IP через прокси {self.proxy_url} используя сервис {check_url}")
        
        try:
            async with httpx.AsyncClient(proxy=self.__get_proxy_url(), timeout=timeout, verify=verify) as client:
                response = await client.get(check_url)
                response.raise_for_status()
                
                # IP-only сервисы возвращают простой текст или JSON
                content_type = response.headers.get("content-type", "").lower()
                if "application/json" in content_type:
                    data = response.json()
                else:
                    # Простой текстовый ответ (IP адрес)
                    ip_text = response.text.strip()
                    data = {"ip": ip_text}
                
                # Обновляем info
                self.info.update_from_dict(data)
                logger.info(f"Успешная проверка IP через прокси {self.proxy_url}: {self.info.ip}")
                return True
                
        except httpx.TimeoutException as e:
            logger.error(f"Таймаут при проверке IP через прокси {self.proxy_url} (сервис: {check_url}): {e}")
            raise
        except httpx.HTTPError as e:
            logger.error(f"HTTP ошибка при проверке IP через прокси {self.proxy_url} (сервис: {check_url}): {e}")
            raise
        except Exception as e:
            logger.error(f"Ошибка при проверке IP через прокси {self.proxy_url} (сервис: {check_url}): {e}", exc_info=True)
            raise
    
    async def check_ip_geo(
        self,
        timeout: float = 10.0,
        verify: bool = True
    ) -> bool:
        """
        Проверяет IP адрес и геолокацию через прокси.
        
        Использует случайный сервис из глобальной конфигурации proxy_config.
        
        Args:
            timeout: Таймаут запроса в секундах
            verify: Проверять SSL сертификаты (по умолчанию True). 
                   Установите False для Burp и других прокси с самоподписанными сертификатами
            
        Returns:
            True если проверка успешна, False в противном случае
            
        Raises:
            httpx.HTTPError: При ошибках HTTP запроса
            httpx.TimeoutException: При превышении таймаута
            Exception: При других ошибках
        """
        check_url = proxy_config.get_random_geo_service()
        logger.debug(f"Проверка IP и геолокации через прокси {self.proxy_url} используя сервис {check_url}")
        
        try:
            async with httpx.AsyncClient(proxy=self.__get_proxy_url(), timeout=timeout, verify=verify) as client:
                response = await client.get(check_url)
                response.raise_for_status()
                data = response.json()
                
                # Обновляем info
                self.info.update_from_dict(data)
                logger.info(f"Успешная проверка IP и геолокации через прокси {self.proxy_url}: IP={self.info.ip}, Country={self.info.country}")
                return True
                
        except httpx.TimeoutException as e:
            logger.error(f"Таймаут при проверке IP и геолокации через прокси {self.proxy_url} (сервис: {check_url}): {e}")
            raise
        except httpx.HTTPError as e:
            logger.error(f"HTTP ошибка при проверке IP и геолокации через прокси {self.proxy_url} (сервис: {check_url}): {e}")
            raise
        except Exception as e:
            logger.error(f"Ошибка при проверке IP и геолокации через прокси {self.proxy_url} (сервис: {check_url}): {e}", exc_info=True)
            raise
    
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
        try:
            check_success = await self.check_ip()
            if not check_success:
                error_msg = "Не удалось получить начальный IP адрес"
                logger.error(f"Ошибка ротации прокси {self.proxy_url}: {error_msg}")
                raise ValueError(error_msg)
        except Exception as e:
            logger.error(f"Ошибка при получении начального IP для прокси {self.proxy_url}: {e}")
            raise
        
        initial_ip = self.info.ip
        if not initial_ip:
            error_msg = "Не удалось получить начальный IP адрес"
            logger.error(f"Ошибка ротации прокси {self.proxy_url}: {error_msg}")
            raise ValueError(error_msg)
        
        logger.info(f"Начальный IP для прокси {self.proxy_url}: {initial_ip}")
        
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
            logger.debug(f"Попытка ротации {attempt + 1}/{max_retries} для прокси {self.proxy_url}")
            
            try:
                # Вызываем функцию ротации с передачей данных через **kwargs
                rotation_success = await func(**proxy_data)
                
                if not rotation_success:
                    logger.warning(f"Ротация не удалась для прокси {self.proxy_url}, попытка {attempt + 1}/{max_retries}")
                    continue
                
                logger.debug(f"Функция ротации вернула успех для прокси {self.proxy_url}, ожидание {delay} секунд")
                
                # Ждем указанную задержку
                await asyncio.sleep(delay)
                
                # Проверяем IP снова
                try:
                    check_success = await self.check_ip()
                    if not check_success:
                        logger.warning(f"Не удалось проверить IP после ротации для прокси {self.proxy_url}, попытка {attempt + 1}/{max_retries}")
                        continue
                except Exception as e:
                    logger.error(f"Ошибка при проверке IP после ротации для прокси {self.proxy_url}, попытка {attempt + 1}/{max_retries}: {e}")
                    continue
                
                new_ip = self.info.ip
                
                if new_ip and new_ip != initial_ip:
                    # IP изменился - ротация успешна
                    logger.info(f"Ротация успешна для прокси {self.proxy_url}: IP изменился с {initial_ip} на {new_ip}")
                    return True
                else:
                    logger.warning(f"IP не изменился для прокси {self.proxy_url} после ротации (было: {initial_ip}, стало: {new_ip}), попытка {attempt + 1}/{max_retries}")
                    
            except Exception as e:
                logger.error(f"Ошибка при выполнении ротации для прокси {self.proxy_url}, попытка {attempt + 1}/{max_retries}: {e}", exc_info=True)
                # Продолжаем попытки
                continue
        
        # Все попытки исчерпаны или IP не изменился
        logger.warning(f"Ротация не удалась для прокси {self.proxy_url} после {max_retries} попыток")
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

