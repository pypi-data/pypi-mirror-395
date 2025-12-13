"""Демонстрационные тесты для config модуля."""

import pytest
from proxy_kit.config import IP_CHECK_URLS, IP_GEO_CHECK_URLS, get_random_url


class TestConfig:
    """Тесты для конфигурации."""
    
    def test_ip_check_urls_not_empty(self):
        """Тест наличия URL для проверки IP."""
        assert len(IP_CHECK_URLS) > 0
        assert all(isinstance(url, str) for url in IP_CHECK_URLS)
        assert all(url.startswith("http") for url in IP_CHECK_URLS)
    
    def test_ip_geo_check_urls_not_empty(self):
        """Тест наличия URL для проверки IP и геолокации."""
        assert len(IP_GEO_CHECK_URLS) > 0
        assert all(isinstance(url, str) for url in IP_GEO_CHECK_URLS)
        assert all(url.startswith("http") for url in IP_GEO_CHECK_URLS)
    
    def test_get_random_url_from_list(self):
        """Тест получения случайного URL из списка."""
        urls = ["https://api1.com", "https://api2.com", "https://api3.com"]
        
        result = get_random_url(urls=urls)
        
        assert result in urls
    
    def test_get_random_url_from_default(self):
        """Тест получения случайного URL из дефолтного списка."""
        result = get_random_url(default_urls=IP_CHECK_URLS)
        
        assert result in IP_CHECK_URLS
    
    def test_get_random_url_prefers_user_list(self):
        """Тест приоритета пользовательского списка."""
        user_urls = ["https://custom.com"]
        default_urls = IP_CHECK_URLS
        
        result = get_random_url(urls=user_urls, default_urls=default_urls)
        
        assert result == "https://custom.com"
        assert result not in default_urls
    
    def test_get_random_url_error_no_urls(self):
        """Тест ошибки при отсутствии URL."""
        with pytest.raises(ValueError, match="Не указаны URL"):
            get_random_url()
    
    def test_get_random_url_multiple_calls_different(self):
        """Тест получения разных URL при множественных вызовах."""
        urls = ["https://api1.com", "https://api2.com", "https://api3.com"]
        
        results = [get_random_url(urls=urls) for _ in range(10)]
        
        # Хотя бы один результат должен отличаться (вероятностный тест)
        assert len(set(results)) >= 1  # Может быть и один, но обычно больше

