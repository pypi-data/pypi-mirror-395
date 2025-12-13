# Scorb API
[![PyPI Latest Release](https://img.shields.io/pypi/v/scorb-api.svg)](https://pypi.org/project/scorb-api/)

Use scorb functionalities in your python application.
## Instalation
```sh
pip install scorb-api
```

# Configuration
## Environment variables
To use scorb-api, you need to set two environment variables:
```dotenv
# ---DOTENV EXAMPLE---
SCORB_USERNAME_API= # Username to authenticate
SCORB_PASSWORD_API= # Password to authenticate
SCORB_BASE_URL=https://scorb.com.br/ # Base path of your api instance
```

# Usage Example
You can use scorb-api in order to read registers on all system tables.

## List registers
You can use get methods to list registers of system table. See the following example:
```python
from scorb_api import ScorbApiClient

# Instantiate ScorbApiClient client object
client = ScorbApiClient(company="your-company", app_name="your-app-name")

# Get the endpoint
cenario_endpoint = client.globais().cenario()

calculo_alcance_enpoint = client.entidades_de_cenario().calculo_alcance(
    cenario_code="cenario_code"
)

custom_entity_enpoint = client.entidades_customizadas().entidade_customizada(
    cenario_code="cenario_code", custom="custom_endpoint_name"
)

custom_table_endpoint = client.tabelas_customizadas().tabela_customizada(
    cenario_code="cenario_code", custom="custom_endpoint_name"
)

# Read will return a list of objects from API.
cenarios_data = cenario_endpoint.read()
calculo_alcance_data = calculo_alcance_enpoint.read()
custom_entity_data = custom_entity_enpoint.read()
custom_table_data = custom_table_endpoint.read()
```
