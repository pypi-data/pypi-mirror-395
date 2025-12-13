"""Демонстрационные тесты для Proxy класса."""

import pytest
import asyncio
from proxy_kit import Proxy, ProxyInfo


class TestProxy:
    """Тесты для Proxy класса."""
    
    def test_proxy_creation_without_auth(self):
        """Тест создания прокси без авторизации."""
        proxy = Proxy(protocol="http", host="127.0.0.1", port=8080)
        
        assert proxy.protocol == "http"
        assert proxy.host == "127.0.0.1"
        assert proxy.port == 8080
        assert proxy.username is None
        assert proxy.password is None
        assert proxy.proxy_url == "http://127.0.0.1:8080"
        assert isinstance(proxy.info, ProxyInfo)
    
    def test_proxy_creation_with_auth(self):
        """Тест создания прокси с авторизацией."""
        proxy = Proxy(
            protocol="socks5",
            host="proxy.example.com",
            port=1080,
            username="user",
            password="pass"
        )
        
        assert proxy.protocol == "socks5"
        assert proxy.host == "proxy.example.com"
        assert proxy.port == 1080
        assert proxy.username == "user"
        assert proxy.password == "pass"
        assert proxy.proxy_url == "socks5://user:pass@proxy.example.com:1080"
    
    def test_proxy_url_building(self):
        """Тест построения URL прокси."""
        # Без авторизации
        proxy1 = Proxy(protocol="http", host="127.0.0.1", port=8080)
        assert proxy1.proxy_url == "http://127.0.0.1:8080"
        
        # С авторизацией
        proxy2 = Proxy(
            protocol="https",
            host="proxy.com",
            port=3128,
            username="user",
            password="pass"
        )
        assert proxy2.proxy_url == "https://user:pass@proxy.com:3128"
    
    def test_proxy_repr(self):
        """Тест строкового представления прокси."""
        proxy = Proxy(protocol="http", host="127.0.0.1", port=8080)
        repr_str = repr(proxy)
        assert "Proxy" in repr_str
        assert "http" in repr_str
        assert "127.0.0.1" in repr_str
        assert "8080" in repr_str
    
    @pytest.mark.asyncio
    async def test_check_ip_structure(self):
        """Тест структуры метода check_ip (без реального запроса)."""
        proxy = Proxy(protocol="http", host="127.0.0.1", port=8080)
        
        # Проверяем, что метод существует и возвращает ProxyInfo
        assert hasattr(proxy, 'check_ip')
        assert callable(proxy.check_ip)
        
        # Проверяем, что info объект существует
        assert proxy.info is not None
        assert isinstance(proxy.info, ProxyInfo)
    
    @pytest.mark.asyncio
    async def test_check_ip_geo_structure(self):
        """Тест структуры метода check_ip_geo (без реального запроса)."""
        proxy = Proxy(protocol="http", host="127.0.0.1", port=8080)
        
        # Проверяем, что метод существует и возвращает ProxyInfo
        assert hasattr(proxy, 'check_ip_geo')
        assert callable(proxy.check_ip_geo)
        
        # Проверяем, что info объект существует
        assert proxy.info is not None
        assert isinstance(proxy.info, ProxyInfo)
    
    def test_proxy_info_initialization(self):
        """Тест инициализации ProxyInfo."""
        proxy = Proxy(protocol="http", host="127.0.0.1", port=8080)
        info = proxy.info
        
        assert info.ip is None
        assert info.geo is None
        assert info.city is None
        assert info.country is None
        assert isinstance(info.raw_data, dict)
        assert len(info.raw_data) == 0
    
    def test_proxy_with_rotation_url(self):
        """Тест создания прокси с rotation_url."""
        proxy = Proxy(
            protocol="http",
            host="127.0.0.1",
            port=8080,
            rotation_url="https://api.example.com/rotate"
        )
        
        assert proxy.rotation_url == "https://api.example.com/rotate"
    
    def test_proxy_with_rotation_func(self):
        """Тест создания прокси с rotation_func."""
        async def dummy_rotation():
            return True
        
        proxy = Proxy(
            protocol="http",
            host="127.0.0.1",
            port=8080,
            rotation_func=dummy_rotation
        )
        
        assert proxy.__rotation_func is not None
        assert callable(proxy.__rotation_func)
    
    @pytest.mark.asyncio
    async def test_rotation_without_func(self):
        """Тест ошибки при вызове rotation без функции."""
        proxy = Proxy(protocol="http", host="127.0.0.1", port=8080)
        
        with pytest.raises(ValueError, match="Функция ротации не указана"):
            await proxy.rotation()

