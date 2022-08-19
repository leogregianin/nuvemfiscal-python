# nuvemfiscal
SDK para Python para NuvemFiscal https://nuvemfiscal.com.br

## Configuração

 * Crie o arquivo `.env` com base no arquivo `.env.example`
 * Altere as credenciais de acesso CLIENT_ID e CLIENT_SECRET fornecidas pela NuvemFiscal

## Instalação

 * Instale o Python 3.7 ou superior
 * Instale o gerenciador de pacotes Poetry
    * `pip install poetry`
 * Instale as dependências do projeto:
    * `poetry install`

## Utilização

 * Buscar informações de CNPJ:
```python
from nuvemfiscal import NuvemFiscal

api = NuvemFiscal()
resp = api.consulta_cnpj('numero do cnpj')
print(resp)
```

 * Buscar informações de CEP:
```python
from nuvemfiscal import NuvemFiscal

api = NuvemFiscal()
resp = api.consulta_cep('numero do cep')
print(resp)
```

## Documentação

 * https://dev.nuvemfiscal.com.br/docs
