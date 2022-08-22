import os
import time
import tempfile

import httpx
from dotenv import load_dotenv

from nuvemfiscal.utils import onlynumber
from nuvemfiscal.exceptions import EnvException


class NuvemFiscal:
    """
    NuvemFiscal API

    """
    def __init__(self):
        load_dotenv()
        self.CLIENT_ID = os.getenv('CLIENT_ID', None)
        self.CLIENT_SECRET = os.getenv('CLIENT_SECRET', None)

        if not self.CLIENT_ID or not self.CLIENT_SECRET:
            raise EnvException('CLIENT_ID and/or CLIENT_SECRET not found')

        self.url_base = 'https://api.nuvemfiscal.com.br'
        self.url_token = 'https://auth.nuvemfiscal.com.br/oauth/token'

    def get_access_token(self, scope=None):
        """
        Busca o access token para iteração com os recursos da API.

        Após o token ser obtido, ele é armazenado em um arquivo temporário
        chamado nuvemfiscal.token para que o mesmo seja mantido em cache.

        O token expira em 24 horas conforme regra da API.

        """
        token = None
        MAX_AGE = 60 * 60 * 24  # 24 hours
        TOKEN_PATH = os.path.join(
            tempfile.gettempdir(),
            'nuvemfiscal.token',
        )

        if os.path.isfile(TOKEN_PATH):
            token_age = time.time() - os.path.getmtime(TOKEN_PATH)

            if token_age < MAX_AGE:
                with open(TOKEN_PATH, 'r') as infile:
                    token = infile.read()

                return token

        if not token:
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

            if resp.status_code != 200:
                raise EnvException('Invalid credentials')

            token = resp.json()['access_token']

            with open(TOKEN_PATH, 'w+') as outfile:
                outfile.write(token)

            return token

    def consulta_cnpj(self, cnpj=None):
        access_token = self.get_access_token(scope='cnpj')
        authorization = f'Bearer {access_token}'
        headers_access = {
            'Authorization': authorization,
        }

        resp = httpx.get(
            f'{self.url_base}/cnpj/{onlynumber(cnpj)}',
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
            f'{self.url_base}/cep/{onlynumber(cep)}',
            headers=headers_access
        )

        return resp.json()
