import os

import httpx
from dotenv import load_dotenv


class NuvemFiscal:
    """
    NuvemFiscal

    """
    def __init__(self):
        load_dotenv()
        self.CLIENT_ID = os.getenv('CLIENT_ID', None)
        self.CLIENT_SECRET = os.getenv('CLIENT_SECRET', None)

        self.url_base = 'https://api.nuvemfiscal.com.br'
        self.url_token = 'https://auth.nuvemfiscal.com.br/oauth/token'

    def get_access_token(self, scope=None):
        headers = {
            'user-agent': 'nuvemfiscal/0.0.1',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        credentials = {
            'grant_type': 'client_credentials',
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'scope': scope,
        }
        resp = httpx.post(
            self.url_token,
            headers=headers,
            data=credentials
        )
        return resp.json()['access_token']

    def consulta_cnpj(self, cnpj=None):
        access_token = self.get_access_token(scope='cnpj')
        authorization = f'Bearer {access_token}'
        headers_access = {
            'Authorization': authorization,
        }

        resp = httpx.get(
            f'{self.url_base}/cnpj/{cnpj}',
            headers=headers_access
        )
        return resp.json()

    def consulta_cep(self, cep=None):
        access_token = self.get_access_token(scope='cep')
        authorization = f'Bearer {access_token}'
        headers_access = {
            'Authorization': authorization,
        }

        resp = httpx.get(
            f'{self.url_base}/cep/{cep}',
            headers=headers_access
        )
        return resp.json()
