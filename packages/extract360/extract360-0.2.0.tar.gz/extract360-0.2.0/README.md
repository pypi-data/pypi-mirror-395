# extract360 (Python)

Cliente oficial Python para a API do Extract360.

## Instalação

```bash
pip install extract360
```

## Uso

```py
from extract360 import Extract360Client

client = Extract360Client(
    api_key="YOUR_API_KEY",
    # base_url="https://api.extract360.dev/api",  # opcional
)

data = client.scrape_and_wait(
    input_url="https://example.com",
    output_format="markdown",
)

print("Status:", data["job"]["status"])
print("Conteudo:", data["result"])
```

## Requisitos
- Python 3.9+
- `requests` (instalado automaticamente)
