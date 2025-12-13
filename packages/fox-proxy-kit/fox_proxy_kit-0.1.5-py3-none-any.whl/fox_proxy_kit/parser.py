"""Класс для парсинга прокси из файлов и управления списком прокси."""
from dataclasses import dataclass
import re
import logging
from typing import List, Optional, Union, Callable, Awaitable
from pathlib import Path

from .proxy import Proxy
from .format import ProxyFormat

# Логгер для модуля (логи появляются только если пользователь настроил logging)
logger = logging.getLogger(__name__)

@dataclass
class ProxyParser:
    """Класс для парсинга и управления прокси."""
    
    def __init__(self):
        """Инициализация парсера."""
        self.proxies: List[Proxy] = []
    
    def parse_file(
        self,
        file_path: str,
        format_template: Union[str, ProxyFormat],
        default_protocol: Optional[str] = None
    ) -> List[Proxy]:
        """
        Парсит файл с прокси по указанному формату.
        
        Args:
            file_path: Путь к файлу с прокси
            format_template: Шаблон формата (строка или ProxyFormat enum), например:
                - ProxyFormat.HOST_PORT
                - ProxyFormat.PROTOCOL_HOST_PORT_AUTH
                - "{protocol}://{host}:{port}"
                - "{host}:{port}:{username}:{password}"
                - "{host}:{port}"
                - "{protocol}://{host}:{port}:{username}:{password}"
                - "{host}:{port}|{rotation_url}" - с URL для ротации
                - "{protocol}://{username}:{password}@{host}:{port}|{rotation_url}"
            default_protocol: Протокол по умолчанию, если не указан в формате
            
        Returns:
            Список объектов Proxy
            
        Examples:
            >>> parser = ProxyParser()
            >>> parser.parse_file("proxies.txt", ProxyFormat.HOST_PORT, default_protocol="http")
            >>> parser.parse_file("proxies.txt", "{host}:{port}", default_protocol="http")
            >>> parser.parse_file("proxies.txt", ProxyFormat.PROTOCOL_USERNAME_PASSWORD_HOST_PORT_ROTATION)
        """
        # Если передан ProxyFormat, получаем строку шаблона
        if isinstance(format_template, ProxyFormat):
            format_template = format_template.get_template()
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл {file_path} не найден")
        
        proxies = []
        
        # Определяем, какие поля есть в шаблоне
        template_fields = re.findall(r'\{(\w+)\}', format_template)
        
        # Проверяем наличие протокола в шаблоне
        has_protocol = "protocol" in template_fields
        if not has_protocol and not default_protocol:
            raise ValueError("Протокол не указан в шаблоне и не задан default_protocol")
        
        # Создаем регулярное выражение для парсинга строк
        # Экранируем специальные символы, кроме {}
        regex_pattern = re.escape(format_template)
        regex_pattern = regex_pattern.replace(r'\{', '{').replace(r'\}', '}')
        
        # Заменяем поля на группы захвата
        for field in template_fields:
            if field == "protocol":
                regex_pattern = regex_pattern.replace(f"{{{field}}}", r"([a-zA-Z0-9]+)")
            elif field == "port":
                regex_pattern = regex_pattern.replace(f"{{{field}}}", r"(\d+)")
            elif field == "host":
                # Хост может содержать точки, дефисы, но не двоеточия, @ и |
                regex_pattern = regex_pattern.replace(f"{{{field}}}", r"([^:@|]+)")
            elif field == "rotation_url":
                # URL может содержать любые символы, включая двоеточия и слеши
                # Разделитель | используется для отделения rotation_url
                regex_pattern = regex_pattern.replace(f"{{{field}}}", r"(.+)")
            else:
                # Для username и password - любые символы кроме двоеточия, @ и |
                regex_pattern = regex_pattern.replace(f"{{{field}}}", r"([^:@|]+)")
        
        regex = re.compile(regex_pattern)
        
        with open(path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                match = regex.match(line)
                if not match:
                    continue
                
                # Создаем словарь значений из групп захвата
                values = {}
                for i, field in enumerate(template_fields):
                    values[field] = match.group(i + 1)
                
                # Если протокол не в шаблоне, используем дефолтный
                protocol = values.get("protocol") or default_protocol
                
                # Создаем объект Proxy
                proxy = Proxy(
                    protocol=protocol,
                    host=values.get("host", ""),
                    port=int(values.get("port", 0)),
                    username=values.get("username"),
                    password=values.get("password"),
                    rotation_url=values.get("rotation_url")
                )
                
                proxies.append(proxy)
        
        self.proxies.extend(proxies)
        return proxies
    
    def get_proxy(self, rotate: bool = True) -> Optional[Proxy]:
        """
        Получает прокси из списка.
        
        Args:
            rotate: Если True, перемещает прокси в конец списка (циклическая очередь)
                   Если False, просто возвращает прокси без перемещения
                   
        Returns:
            Объект Proxy или None, если список пуст
        """
        if not self.proxies:
            return None
        
        if rotate:
            proxy = self.proxies.pop(0)
            self.proxies.append(proxy)
            return proxy
        else:
            return self.proxies[0]
    
    def add_proxy(self, proxy: Proxy) -> None:
        """
        Добавляет прокси в список.
        
        Args:
            proxy: Объект Proxy для добавления
        """
        self.proxies.append(proxy)
    
    def set_rotation_func(self, rotation_func: Callable[..., Awaitable[bool]]) -> None:
        """
        Устанавливает функцию ротации для всех прокси в списке.
        
        Args:
            rotation_func: Асинхронная функция для ротации прокси.
                          Функция ДОЛЖНА принимать **kwargs с данными прокси:
                          protocol, host, port, username, password, rotation_url, proxy_url.
                          Должна возвращать bool (True если ротация успешна).
                          
        Examples:
            >>> async def my_rotation_func(**kwargs) -> bool:
            ...     rotation_url = kwargs.get("rotation_url")
            ...     # Ваша логика ротации
            ...     return True
            >>> 
            >>> parser = ProxyParser()
            >>> parser.parse_file("proxies.txt", ProxyFormat.HOST_PORT)
            >>> parser.set_rotation_func(my_rotation_func)
        """
        for proxy in self.proxies:
            proxy.rotation_func = rotation_func
    
    def clear(self) -> None:
        """Очищает список прокси."""
        self.proxies.clear()
    
    def __len__(self) -> int:
        """Возвращает количество прокси в списке."""
        return len(self.proxies)

