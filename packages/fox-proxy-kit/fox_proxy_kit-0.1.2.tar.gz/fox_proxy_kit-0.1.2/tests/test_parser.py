"""Демонстрационные тесты для ProxyParser класса."""

import pytest
import tempfile
import os
from pathlib import Path
from proxy_kit import ProxyParser, Proxy


class TestProxyParser:
    """Тесты для ProxyParser класса."""
    
    def test_parser_initialization(self):
        """Тест инициализации парсера."""
        parser = ProxyParser()
        
        assert parser.proxies == []
        assert len(parser) == 0
    
    def test_parse_file_simple_format(self):
        """Тест парсинга файла с простым форматом host:port."""
        parser = ProxyParser()
        
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("127.0.0.1:8080\n")
            f.write("192.168.1.1:3128\n")
            f.write("# Комментарий\n")
            f.write("10.0.0.1:8080\n")
            temp_file = f.name
        
        try:
            proxies = parser.parse_file(
                temp_file,
                format_template="{host}:{port}",
                default_protocol="http"
            )
            
            assert len(proxies) == 3
            assert len(parser) == 3
            
            # Проверяем первый прокси
            assert proxies[0].host == "127.0.0.1"
            assert proxies[0].port == 8080
            assert proxies[0].protocol == "http"
            
            # Проверяем второй прокси
            assert proxies[1].host == "192.168.1.1"
            assert proxies[1].port == 3128
            
            # Проверяем третий прокси
            assert proxies[2].host == "10.0.0.1"
            assert proxies[2].port == 8080
            
        finally:
            os.unlink(temp_file)
    
    def test_parse_file_with_protocol(self):
        """Тест парсинга файла с протоколом в формате."""
        parser = ProxyParser()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("http://127.0.0.1:8080\n")
            f.write("socks5://192.168.1.1:1080\n")
            temp_file = f.name
        
        try:
            proxies = parser.parse_file(
                temp_file,
                format_template="{protocol}://{host}:{port}"
            )
            
            assert len(proxies) == 2
            assert proxies[0].protocol == "http"
            assert proxies[1].protocol == "socks5"
            
        finally:
            os.unlink(temp_file)
    
    def test_parse_file_with_auth(self):
        """Тест парсинга файла с авторизацией."""
        parser = ProxyParser()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("127.0.0.1:8080:user1:pass1\n")
            f.write("192.168.1.1:3128:user2:pass2\n")
            temp_file = f.name
        
        try:
            proxies = parser.parse_file(
                temp_file,
                format_template="{host}:{port}:{username}:{password}",
                default_protocol="http"
            )
            
            assert len(proxies) == 2
            assert proxies[0].username == "user1"
            assert proxies[0].password == "pass1"
            assert proxies[1].username == "user2"
            assert proxies[1].password == "pass2"
            
        finally:
            os.unlink(temp_file)
    
    def test_parse_file_full_format(self):
        """Тест парсинга файла с полным форматом."""
        parser = ProxyParser()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("http://127.0.0.1:8080:user:pass\n")
            f.write("socks5://192.168.1.1:1080:admin:secret\n")
            temp_file = f.name
        
        try:
            proxies = parser.parse_file(
                temp_file,
                format_template="{protocol}://{host}:{port}:{username}:{password}"
            )
            
            assert len(proxies) == 2
            assert proxies[0].protocol == "http"
            assert proxies[0].host == "127.0.0.1"
            assert proxies[0].port == 8080
            assert proxies[0].username == "user"
            assert proxies[0].password == "pass"
            
        finally:
            os.unlink(temp_file)
    
    def test_parse_file_nonexistent(self):
        """Тест обработки несуществующего файла."""
        parser = ProxyParser()
        
        with pytest.raises(FileNotFoundError):
            parser.parse_file(
                "nonexistent_file.txt",
                format_template="{host}:{port}",
                default_protocol="http"
            )
    
    def test_parse_file_missing_protocol(self):
        """Тест ошибки при отсутствии протокола."""
        parser = ProxyParser()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("127.0.0.1:8080\n")
            temp_file = f.name
        
        try:
            with pytest.raises(ValueError, match="Протокол не указан"):
                parser.parse_file(
                    temp_file,
                    format_template="{host}:{port}"
                    # default_protocol не указан
                )
        finally:
            os.unlink(temp_file)
    
    def test_get_proxy_rotate(self):
        """Тест получения прокси с ротацией."""
        parser = ProxyParser()
        
        # Добавляем прокси вручную
        proxy1 = Proxy(protocol="http", host="127.0.0.1", port=8080)
        proxy2 = Proxy(protocol="http", host="127.0.0.2", port=8080)
        proxy3 = Proxy(protocol="http", host="127.0.0.3", port=8080)
        
        parser.add_proxy(proxy1)
        parser.add_proxy(proxy2)
        parser.add_proxy(proxy3)
        
        assert len(parser) == 3
        
        # Получаем прокси с ротацией
        first = parser.get_proxy(rotate=True)
        assert first == proxy1
        assert len(parser) == 3  # Количество не изменилось
        assert parser.proxies[0] == proxy2  # Первый элемент изменился
        assert parser.proxies[-1] == proxy1  # Последний элемент - это первый прокси
        
        # Получаем еще раз
        second = parser.get_proxy(rotate=True)
        assert second == proxy2
        assert parser.proxies[-1] == proxy2
    
    def test_get_proxy_no_rotate(self):
        """Тест получения прокси без ротации."""
        parser = ProxyParser()
        
        proxy1 = Proxy(protocol="http", host="127.0.0.1", port=8080)
        proxy2 = Proxy(protocol="http", host="127.0.0.2", port=8080)
        
        parser.add_proxy(proxy1)
        parser.add_proxy(proxy2)
        
        # Получаем без ротации
        first = parser.get_proxy(rotate=False)
        assert first == proxy1
        
        # Получаем еще раз - должен быть тот же прокси
        second = parser.get_proxy(rotate=False)
        assert second == proxy1
        assert parser.proxies[0] == proxy1  # Порядок не изменился
    
    def test_get_proxy_empty_list(self):
        """Тест получения прокси из пустого списка."""
        parser = ProxyParser()
        
        assert parser.get_proxy() is None
        assert parser.get_proxy(rotate=False) is None
    
    def test_add_proxy(self):
        """Тест добавления прокси."""
        parser = ProxyParser()
        
        proxy = Proxy(protocol="http", host="127.0.0.1", port=8080)
        parser.add_proxy(proxy)
        
        assert len(parser) == 1
        assert parser.proxies[0] == proxy
    
    def test_clear(self):
        """Тест очистки списка прокси."""
        parser = ProxyParser()
        
        parser.add_proxy(Proxy(protocol="http", host="127.0.0.1", port=8080))
        parser.add_proxy(Proxy(protocol="http", host="127.0.0.2", port=8080))
        
        assert len(parser) == 2
        
        parser.clear()
        
        assert len(parser) == 0
        assert parser.proxies == []
    
    def test_len(self):
        """Тест метода __len__."""
        parser = ProxyParser()
        
        assert len(parser) == 0
        
        parser.add_proxy(Proxy(protocol="http", host="127.0.0.1", port=8080))
        assert len(parser) == 1
        
        parser.add_proxy(Proxy(protocol="http", host="127.0.0.2", port=8080))
        assert len(parser) == 2
    
    def test_parse_file_with_rotation_url(self):
        """Тест парсинга файла с rotation_url."""
        parser = ProxyParser()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("127.0.0.1:8080:https://api.example.com/rotate\n")
            f.write("192.168.1.1:3128:https://api.example.com/rotate2\n")
            temp_file = f.name
        
        try:
            proxies = parser.parse_file(
                temp_file,
                format_template="{host}:{port}:{rotation_url}",
                default_protocol="http"
            )
            
            assert len(proxies) == 2
            assert proxies[0].rotation_url == "https://api.example.com/rotate"
            assert proxies[1].rotation_url == "https://api.example.com/rotate2"
            
        finally:
            os.unlink(temp_file)

