# Proxy Tool Kit

Библиотека для работы с прокси: проверка IP, геолокации и парсинг прокси из файлов.

## Установка

```bash
pip install proxy-tool-kit
```

### Установка для разработки

```bash
git clone <repository-url>
cd proxy-tool-kit

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установить зависимости
pip install httpx

# Или установить пакет в режиме разработки (включает все зависимости)
pip install -e ".[dev]"
```

### Запуск тестов

```bash
pytest
```

### Примеры использования

В папке `examples/` находятся демонстрационные примеры:

- `basic_usage.py` - базовое использование
- `check_ip_geo.py` - проверка IP и геолокации
- `parse_proxies.py` - парсинг прокси из файла
- `full_example.py` - полный пример работы

#### Запуск примеров:

**Вариант 1: Используя виртуальное окружение (рекомендуется)**

```bash
# Активировать виртуальное окружение
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Запустить пример
python examples/basic_usage.py
python examples/parse_proxies.py
python examples/check_ip_geo.py
python examples/full_example.py
```

**Вариант 2: Используя скрипт-помощник**

```bash
./run_example.sh basic_usage
./run_example.sh parse_proxies
./run_example.sh check_ip_geo
./run_example.sh full_example
```

**Вариант 3: Установить пакет в режиме разработки**

```bash
pip install -e ".[dev]"
python examples/basic_usage.py
```

## Основные возможности

- **Proxy DTO** - класс для работы с прокси с методами проверки IP и геолокации
- **ProxyParser** - парсинг прокси из файлов с поддержкой различных форматов
- **Циклическая очередь** - автоматическая ротация прокси при использовании
- **Асинхронные запросы** - проверка прокси через различные API сервисы
- **Поддержка протоколов** - HTTP, HTTPS (SOCKS5 требует дополнительных библиотек)

## Использование

### Создание прокси

```python
from fox_proxy_kit import Proxy

# Прокси без авторизации
proxy = Proxy(protocol="http", host="127.0.0.1", port=8080)

# Прокси с авторизацией
proxy = Proxy(
    protocol="socks5",
    host="127.0.0.1",
    port=1080,
    username="user",
    password="pass"
)
```

### Проверка IP

```python
import asyncio
from fox_proxy_kit import Proxy

async def main():
    proxy = Proxy(protocol="http", host="127.0.0.1", port=8080)
    
    # Проверка IP через случайный API сервис
    info = await proxy.check_ip()
    print(f"IP: {info.ip}")
    
    # Проверка через конкретный URL
    info = await proxy.check_ip(url="https://api.ipify.org?format=json")
    
    # Проверка через список URL (случайный выбор)
    info = await proxy.check_ip(urls=[
        "https://api.ipify.org?format=json",
        "https://api64.ipify.org?format=json"
    ])

asyncio.run(main())
```

### Проверка IP и геолокации

```python
import asyncio
from fox_proxy_kit import Proxy

async def main():
    proxy = Proxy(protocol="http", host="127.0.0.1", port=8080)
    
    # Проверка IP и геолокации
    info = await proxy.check_ip_geo()
    print(f"IP: {info.ip}")
    print(f"Country: {info.country}")
    print(f"City: {info.city}")
    print(f"Geo: {info.geo}")

asyncio.run(main())
```

### Парсинг прокси из файла

```python
from fox_proxy_kit import ProxyParser, ProxyFormat

parser = ProxyParser()

# Использование ProxyFormat enum (рекомендуется)
parser.parse_file("proxies.txt", ProxyFormat.HOST_PORT, default_protocol="http")
parser.parse_file("proxies.txt", ProxyFormat.PROTOCOL_HOST_PORT)
parser.parse_file("proxies.txt", ProxyFormat.PROTOCOL_USERNAME_PASSWORD_HOST_PORT)
parser.parse_file("proxies.txt", ProxyFormat.PROTOCOL_USERNAME_PASSWORD_HOST_PORT_ROTATION)

# Или со строкой (как раньше)
parser.parse_file("proxies.txt", "{host}:{port}", default_protocol="http")
parser.parse_file("proxies.txt", "{protocol}://{host}:{port}")
parser.parse_file("proxies.txt", "{protocol}://{username}:{password}@{host}:{port}|{rotation_url}")

# Получение прокси (циклическая очередь)
proxy = parser.get_proxy()  # rotate=True по умолчанию

# Получение без ротации
proxy = parser.get_proxy(rotate=False)
```

#### Доступные форматы ProxyFormat:

- `ProxyFormat.HOST_PORT` - `{host}:{port}`
- `ProxyFormat.PROTOCOL_HOST_PORT` - `{protocol}://{host}:{port}`
- `ProxyFormat.HOST_PORT_AUTH` - `{host}:{port}:{username}:{password}`
- `ProxyFormat.PROTOCOL_HOST_PORT_AUTH` - `{protocol}://{host}:{port}:{username}:{password}`
- `ProxyFormat.PROTOCOL_USERNAME_PASSWORD_HOST_PORT` - `{protocol}://{username}:{password}@{host}:{port}`
- `ProxyFormat.HOST_PORT_ROTATION` - `{host}:{port}|{rotation_url}`
- `ProxyFormat.PROTOCOL_HOST_PORT_ROTATION` - `{protocol}://{host}:{port}|{rotation_url}`
- `ProxyFormat.HOST_PORT_AUTH_ROTATION` - `{host}:{port}:{username}:{password}|{rotation_url}`
- `ProxyFormat.PROTOCOL_USERNAME_PASSWORD_HOST_PORT_ROTATION` - `{protocol}://{username}:{password}@{host}:{port}|{rotation_url}`
- `ProxyFormat.FULL` - `{protocol}://{username}:{password}@{host}:{port}|{rotation_url}`

#### Кастомное построение форматов с Format:

Для создания собственных форматов используйте `Format` enum:

```python
from fox_proxy_kit import ProxyParser, Format

parser = ProxyParser()

# Строим кастомный формат через f-строку
custom_format = f"{Format.PROTOCOL}://{Format.USERNAME}:{Format.PASSWORD}@{Format.HOST}:{Format.PORT}|{Format.ROTATION_URL}"

# Используем для парсинга
proxies = parser.parse_file("proxies.txt", custom_format)

# Доступные элементы Format:
# - Format.HOST = "{host}"
# - Format.PORT = "{port}"
# - Format.PROTOCOL = "{protocol}"
# - Format.USERNAME = "{username}"
# - Format.PASSWORD = "{password}"
# - Format.ROTATION_URL = "{rotation_url}"
```

### Пример файла proxies.txt

```
# HTTP прокси (формат: {host}:{port})
127.0.0.1:8080
192.168.1.1:3128

# С протоколом (формат: {protocol}://{host}:{port})
http://127.0.0.1:8080
socks5://192.168.1.1:1080

# С авторизацией (формат: {protocol}://{username}:{password}@{host}:{port})
http://user:pass@proxy.example.com:8080

# С rotation_url через | (формат: {protocol}://{username}:{password}@{host}:{port}|{rotation_url})
http://user:pass@127.0.0.1:8080|https://api.example.com/rotate
https://admin:secret@192.168.1.1:3128|https://api.example.com/rotate2
```

### Ротация прокси

```python
import asyncio
import httpx
from fox_proxy_kit import Proxy

async def rotation_function(**kwargs) -> bool:
    """
    Функция для ротации прокси через rotation_url.
    
    ВАЖНО: Функция ОБЯЗАТЕЛЬНО должна принимать **kwargs!
    
    Функция получает данные прокси через **kwargs:
    - protocol: протокол прокси
    - host: хост прокси
    - port: порт прокси
    - username: имя пользователя (может быть None)
    - password: пароль (может быть None)
    - rotation_url: URL для ротации (может быть None)
    - proxy_url: полный URL прокси
    """
    rotation_url = kwargs.get("rotation_url")
    proxy_url = kwargs.get("proxy_url")
    
    if not rotation_url:
        return False
    
    try:
        async with httpx.AsyncClient(proxy=proxy_url, verify=False) as client:
            response = await client.get(rotation_url)
            return response.status_code == 200
    except:
        return False

async def main():
    # Вариант 1: Функция передана при создании объекта
    proxy = Proxy(
        protocol="http",
        host="127.0.0.1",
        port=8080,
        rotation_url="https://api.example.com/rotate",
        rotation_func=rotation_function  # Функция получит данные через **kwargs
    )
    
    # Выполняем ротацию
    result = await proxy.rotation(delay=2.0, max_retries=3)
    if result:
        print("IP успешно изменен!")
    
    # Вариант 2: Функция передана в метод rotation
    proxy2 = Proxy(
        protocol="http",
        host="127.0.0.1",
        port=8080,
        rotation_url="https://api.example.com/rotate"
    )
    
    result = await proxy2.rotation(rotation_func=rotation_function, delay=2.0, max_retries=3)

asyncio.run(main())
```

### Полный пример

```python
import asyncio
from fox_proxy_kit import ProxyParser, ProxyFormat

async def main():
    parser = ProxyParser()
    
    # Парсим прокси из файла
    parser.parse_file("proxies.txt", "{host}:{port}", default_protocol="http")
    
    # Проверяем каждый прокси
    for _ in range(len(parser)):
        proxy = parser.get_proxy()  # Циклическая очередь
        
        try:
            info = await proxy.check_ip_geo()
            print(f"Proxy: {proxy.proxy_url}")
            print(f"IP: {info.ip}, Country: {info.country}, City: {info.city}")
        except Exception as e:
            print(f"Ошибка при проверке {proxy.proxy_url}: {e}")

asyncio.run(main())
```

## API Reference

### Proxy

Класс для работы с прокси.

#### Атрибуты

- `protocol` - протокол (http, https, socks5)
- `host` - хост прокси
- `port` - порт прокси
- `username` - имя пользователя (опционально)
- `password` - пароль (опционально)
- `rotation_url` - URL для ротации прокси (опционально)
- `rotation_func` - асинхронная функция для ротации (опционально)
- `proxy_url` - полный URL прокси
- `info` - объект ProxyInfo с результатами проверки

#### Методы

- `async check_ip(url=None, urls=None, timeout=10.0)` - проверка IP
- `async check_ip_geo(url=None, urls=None, timeout=10.0)` - проверка IP и геолокации
- `async rotation(rotation_func=None, delay=2.0, max_retries=3)` - ротация прокси с проверкой изменения IP

### ProxyParser

Класс для парсинга и управления прокси.

#### Методы

- `parse_file(file_path, format_template, default_protocol=None)` - парсинг файла
  - `format_template` может быть строкой или `ProxyFormat` enum
- `get_proxy(rotate=True)` - получение прокси из списка
- `add_proxy(proxy)` - добавление прокси
- `clear()` - очистка списка

### ProxyFormat

Enum с предопределенными форматами прокси.

#### Доступные форматы:

- `HOST_PORT` - `{host}:{port}`
- `PROTOCOL_HOST_PORT` - `{protocol}://{host}:{port}`
- `HOST_PORT_AUTH` - `{host}:{port}:{username}:{password}`
- `PROTOCOL_HOST_PORT_AUTH` - `{protocol}://{host}:{port}:{username}:{password}`
- `PROTOCOL_USERNAME_PASSWORD_HOST_PORT` - `{protocol}://{username}:{password}@{host}:{port}`
- `HOST_PORT_ROTATION` - `{host}:{port}|{rotation_url}`
- `PROTOCOL_HOST_PORT_ROTATION` - `{protocol}://{host}:{port}|{rotation_url}`
- `HOST_PORT_AUTH_ROTATION` - `{host}:{port}:{username}:{password}|{rotation_url}`
- `PROTOCOL_USERNAME_PASSWORD_HOST_PORT_ROTATION` - `{protocol}://{username}:{password}@{host}:{port}|{rotation_url}`
- `FULL` - `{protocol}://{username}:{password}@{host}:{port}|{rotation_url}`

### ProxyInfo

DTO класс с информацией о прокси.

#### Атрибуты

- `ip` - IP адрес
- `geo` - геолокация (lat,lon)
- `city` - город
- `country` - страна
- `country_code` - код страны
- `region` - регион
- `timezone` - часовой пояс
- `isp` - провайдер
- `raw_data` - полные данные от API

## Примечания

### Поддержка SOCKS5

Для работы с SOCKS5 прокси требуется дополнительная библиотека `httpx-socks`:

```bash
pip install httpx-socks
```

После установки httpx автоматически будет использовать SOCKS5 прокси через httpx-socks.

### API сервисы

Библиотека использует бесплатные API сервисы для проверки IP и геолокации. Для избежания лимитов рекомендуется передавать свои URL или списки URL в методы `check_ip` и `check_ip_geo`.

## Лицензия

MIT
