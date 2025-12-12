import uuid
import time
import json
import ssl
import logging

try:
    import requests
except ImportError:
    requests = None

try:
    import aiohttp
    import asyncio
except ImportError:
    aiohttp = None
    asyncio = None


class GigaChatClient:
    def __init__(self, auth_key, scope='GIGACHAT_API_PERS', verify_ssl=True):
        if requests is None:
            raise ImportError("Для работы синхронного клиента установите requests: pip install requests")

        self.auth_key = auth_key
        self.scope = scope
        self.verify_ssl = verify_ssl
        self.access_token = None
        self.token_expires_at = 0
        self.auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"

    def _get_headers(self, auth=False):
        request_id = str(uuid.uuid4())
        headers = {
            'Accept': 'application/json',
            'RqUID': request_id
        }
        if auth:
            headers['Authorization'] = f'Basic {self.auth_key}'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        else:
            self._ensure_token()
            headers['Authorization'] = f'Bearer {self.access_token}'
            headers['Content-Type'] = 'application/json'
        return headers

    def _ensure_token(self):
        if self.access_token and time.time() * 1000 < self.token_expires_at:
            return

        headers = self._get_headers(auth=True)
        response = requests.post(
            self.auth_url,
            headers=headers,
            data={'scope': self.scope},
            verify=self.verify_ssl
        )
        if response.status_code != 200:
            raise Exception(f"Auth Error: {response.text}")

        data = response.json()
        self.access_token = data['access_token']
        self.token_expires_at = data['expires_at']

    def generate(self, prompt, model="GigaChat", temperature=0.7):
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "stream": False
        }
        response = requests.post(
            url, headers=self._get_headers(), json=payload, verify=self.verify_ssl
        )
        if response.status_code != 200:
            raise Exception(f"Generation Error: {response.text}")
        return response.json()['choices'][0]['message']['content']

    def generate_stream(self, prompt, model="GigaChat", temperature=0.7):
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "stream": True
        }
        response = requests.post(
            url, headers=self._get_headers(), json=payload, stream=True, verify=self.verify_ssl
        )
        if response.status_code != 200:
            raise Exception(f"Stream Error: {response.text}")

        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith("data: "):
                    data_str = decoded[6:]
                    if data_str == "[DONE]": break
                    try:
                        chunk = json.loads(data_str)
                        content = chunk['choices'][0]['delta'].get('content')
                        if content: yield content
                    except:
                        continue


class AsyncGigaChatClient:
    def __init__(self, auth_key, scope='GIGACHAT_API_PERS', verify_ssl=True):
        if aiohttp is None:
            raise ImportError("Для работы асинхронного клиента установите aiohttp: pip install aiohttp")
        self.auth_key = auth_key
        self.scope = scope
        self.verify_ssl = verify_ssl
        self.access_token = None
        self.token_expires_at = 0
        self.session = None
        self._auth_lock = asyncio.Lock() if asyncio else None
        self.auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"

    async def __aenter__(self):
        ssl_ctx = ssl.create_default_context()
        if not self.verify_ssl:
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE

        conn = aiohttp.TCPConnector(ssl=ssl_ctx)
        self.session = aiohttp.ClientSession(connector=conn)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session: await self.session.close()

    def _get_headers(self, auth=False):
        request_id = str(uuid.uuid4())
        headers = {'Accept': 'application/json', 'RqUID': request_id}
        if auth:
            headers['Authorization'] = f'Basic {self.auth_key}'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        else:
            headers['Authorization'] = f'Bearer {self.access_token}'
            headers['Content-Type'] = 'application/json'
        return headers

    async def _ensure_token(self):
        if self.access_token and time.time() * 1000 < self.token_expires_at: return
        async with self._auth_lock:
            if self.access_token and time.time() * 1000 < self.token_expires_at: return
            headers = self._get_headers(auth=True)
            async with self.session.post(self.auth_url, headers=headers, data={'scope': self.scope}) as resp:
                if resp.status != 200: raise Exception(await resp.text())
                data = await resp.json()
                self.access_token = data['access_token']
                self.token_expires_at = data['expires_at']

    async def generate(self, prompt, model="GigaChat", temperature=0.7):
        await self._ensure_token()
        payload = {"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False,
                   "temperature": temperature}
        async with self.session.post(f"{self.base_url}/chat/completions", headers=self._get_headers(),
                                     json=payload) as resp:
            if resp.status != 200: raise Exception(await resp.text())
            data = await resp.json()
            return data['choices'][0]['message']['content']

    async def generate_stream(self, prompt, model="GigaChat", temperature=0.7):
        await self._ensure_token()
        payload = {"model": model, "messages": [{"role": "user", "content": prompt}], "stream": True,
                   "temperature": temperature}
        async with self.session.post(f"{self.base_url}/chat/completions", headers=self._get_headers(),
                                     json=payload) as resp:
            if resp.status != 200: raise Exception(await resp.text())
            async for line in resp.content:
                decoded = line.decode('utf-8').strip()
                if decoded.startswith("data: "):
                    data_str = decoded[6:]
                    if data_str == "[DONE]": break
                    try:
                        chunk = json.loads(data_str)
                        content = chunk['choices'][0]['delta'].get('content')
                        if content: yield content
                    except:
                        continue