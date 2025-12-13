"""Enum для форматов прокси."""

from enum import Enum


class ProxyFormat(Enum):
    """Предопределенные форматы прокси."""
    
    # Простые форматы
    HOST_PORT = "{host}:{port}"
    PROTOCOL_HOST_PORT = "{protocol}://{host}:{port}"
    
    # С авторизацией
    HOST_PORT_AUTH = "{host}:{port}:{username}:{password}"
    PROTOCOL_HOST_PORT_AUTH = "{protocol}://{host}:{port}:{username}:{password}"
    PROTOCOL_USERNAME_PASSWORD_HOST_PORT = "{protocol}://{username}:{password}@{host}:{port}"
    
    # С rotation_url
    HOST_PORT_ROTATION = "{host}:{port}|{rotation_url}"
    PROTOCOL_HOST_PORT_ROTATION = "{protocol}://{host}:{port}|{rotation_url}"
    HOST_PORT_AUTH_ROTATION = "{host}:{port}:{username}:{password}|{rotation_url}"
    PROTOCOL_USERNAME_PASSWORD_HOST_PORT_ROTATION = "{protocol}://{username}:{password}@{host}:{port}|{rotation_url}"
    
    # Полный формат
    FULL = "{protocol}://{username}:{password}@{host}:{port}|{rotation_url}"
    
    def get_template(self) -> str:
        """
        Возвращает строку шаблона формата.
        
        Returns:
            Строка шаблона для парсинга
        """
        return self.value
    
    @classmethod
    def from_string(cls, format_string: str) -> "ProxyFormat":
        """
        Создает ProxyFormat из строки.
        
        Args:
            format_string: Строка формата
            
        Returns:
            ProxyFormat объект
            
        Raises:
            ValueError: Если формат не найден
        """
        for fmt in cls:
            if fmt.value == format_string:
                return fmt
        
        # Если не найден, создаем кастомный формат
        # Но для этого нужно использовать другой подход
        raise ValueError(f"Формат '{format_string}' не найден в предопределенных форматах")
    
    def __str__(self) -> str:
        """Строковое представление формата."""
        return self.value


class Format(Enum):
    """
    Enum для кастомного построения форматов прокси.
    
    Используется для построения собственных шаблонов формата через f-строки.
    
    Examples:
        >>> format_template = f"{Format.PROTOCOL}://{Format.USERNAME}:{Format.PASSWORD}@{Format.HOST}:{Format.PORT}|{Format.ROTATION_URL}"
        >>> parser.parse_file("proxies.txt", format_template)
    """
    
    HOST = "host"
    PORT = "port"
    PROTOCOL = "protocol"
    USERNAME = "username"
    PASSWORD = "password"
    ROTATION_URL = "rotation_url"
    
    def __format__(self, format_spec: str) -> str:
        """
        Позволяет использовать Format в f-строках напрямую.
        Автоматически добавляет фигурные скобки вокруг значения.
        
        Args:
            format_spec: Спецификация формата (не используется)
            
        Returns:
            Значение enum с фигурными скобками (например, "{host}")
            
        Examples:
            >>> f"{Format.HOST}"  # Возвращает "{host}"
            >>> f"{Format.PROTOCOL}://{Format.HOST}:{Format.PORT}"  # Возвращает "{protocol}://{host}:{port}"
        """
        return f"{{{self.value}}}"
    
    def __str__(self) -> str:
        """Строковое представление формата с фигурными скобками."""
        return f"{{{self.value}}}"
