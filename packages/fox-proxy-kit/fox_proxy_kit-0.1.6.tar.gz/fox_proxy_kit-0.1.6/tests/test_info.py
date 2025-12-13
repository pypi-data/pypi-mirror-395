"""Демонстрационные тесты для ProxyInfo класса."""

from proxy_kit import ProxyInfo


class TestProxyInfo:
    """Тесты для ProxyInfo класса."""
    
    def test_info_initialization(self):
        """Тест инициализации ProxyInfo."""
        info = ProxyInfo()
        
        assert info.ip is None
        assert info.geo is None
        assert info.city is None
        assert info.country is None
        assert info.country_code is None
        assert info.region is None
        assert info.region_code is None
        assert info.timezone is None
        assert info.isp is None
        assert info.org is None
        assert info.asn is None
        assert isinstance(info.raw_data, dict)
        assert len(info.raw_data) == 0
    
    def test_update_from_dict_ipify(self):
        """Тест обновления из данных ipify API."""
        info = ProxyInfo()
        
        data = {
            "ip": "192.168.1.1"
        }
        
        info.update_from_dict(data)
        
        assert info.ip == "192.168.1.1"
        assert info.raw_data == data
    
    def test_update_from_dict_ip_api(self):
        """Тест обновления из данных ip-api.com."""
        info = ProxyInfo()
        
        data = {
            "query": "192.168.1.1",
            "country": "United States",
            "countryCode": "US",
            "region": "CA",
            "regionName": "California",
            "city": "San Francisco",
            "lat": 37.7749,
            "lon": -122.4194,
            "timezone": "America/Los_Angeles",
            "isp": "Example ISP",
            "org": "Example Org",
            "as": "AS12345"
        }
        
        info.update_from_dict(data)
        
        assert info.ip == "192.168.1.1"
        assert info.country == "United States"
        assert info.country_code == "US"
        assert info.region == "CA"
        assert info.region_code == "CA"
        assert info.city == "San Francisco"
        assert info.geo == "37.7749,-122.4194"
        assert info.timezone == "America/Los_Angeles"
        assert info.isp == "Example ISP"
        assert info.org == "Example Org"
        assert info.asn == "AS12345"
    
    def test_update_from_dict_ipinfo(self):
        """Тест обновления из данных ipinfo.io."""
        info = ProxyInfo()
        
        data = {
            "ip": "192.168.1.1",
            "city": "New York",
            "region": "NY",
            "country": "US",
            "loc": "40.7128,-74.0060",
            "org": "AS12345 Example Org",
            "timezone": "America/New_York"
        }
        
        info.update_from_dict(data)
        
        assert info.ip == "192.168.1.1"
        assert info.city == "New York"
        assert info.region == "NY"
        assert info.country == "US"
        assert info.geo == "40.7128,-74.0060"
        assert info.org == "AS12345 Example Org"
        assert info.timezone == "America/New_York"
    
    def test_update_from_dict_ipapi_co(self):
        """Тест обновления из данных ipapi.co."""
        info = ProxyInfo()
        
        data = {
            "ip": "192.168.1.1",
            "city": "London",
            "region": "England",
            "region_code": "ENG",
            "country": "GB",
            "country_name": "United Kingdom",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "timezone": "Europe/London",
            "org": "Example ISP"
        }
        
        info.update_from_dict(data)
        
        assert info.ip == "192.168.1.1"
        assert info.city == "London"
        assert info.region == "England"
        assert info.region_code == "ENG"
        assert info.country_code == "GB"
        assert info.country == "United Kingdom"
        assert info.geo == "51.5074,-0.1278"
        assert info.timezone == "Europe/London"
        assert info.org == "Example ISP"
    
    def test_update_from_dict_multiple_calls(self):
        """Тест множественных обновлений."""
        info = ProxyInfo()
        
        # Первое обновление
        info.update_from_dict({"ip": "192.168.1.1", "city": "City1"})
        assert info.ip == "192.168.1.1"
        assert info.city == "City1"
        
        # Второе обновление
        info.update_from_dict({"ip": "192.168.1.2", "city": "City2", "country": "US"})
        assert info.ip == "192.168.1.2"
        assert info.city == "City2"
        assert info.country == "US"
        # Старые данные должны быть перезаписаны
        assert len(info.raw_data) == 3
    
    def test_update_from_dict_empty(self):
        """Тест обновления пустым словарем."""
        info = ProxyInfo()
        
        info.update_from_dict({})
        
        assert info.ip is None
        assert len(info.raw_data) == 0
    
    def test_update_from_dict_partial_data(self):
        """Тест обновления частичными данными."""
        info = ProxyInfo()
        
        data = {
            "ip": "192.168.1.1",
            "city": "Test City"
        }
        
        info.update_from_dict(data)
        
        assert info.ip == "192.168.1.1"
        assert info.city == "Test City"
        assert info.country is None
        assert info.geo is None

