# Integração — Amazon Selling Partner API (SP-API)

_Última atualização: 2026-05-12_

## Veredicto de Arquitetura

Não existe MCP oficial da Amazon para Claude. A integração correta é via **SP-API** com a biblioteca Python `python-amazon-sp-api`.

---

## O que é a SP-API

REST API da Amazon que dá acesso programático a: pedidos, estoque, anúncios, preços, relatórios e métricas de vendas. Substitui a antiga MWS (descontinuada).

**Documentação oficial:** https://developer-docs.amazon.com/sp-api

---

## Autenticação — Login with Amazon (LWA)

| Item | Detalhe |
|---|---|
| Protocolo | OAuth 2.0 + AWS Signature V4 |
| Token de acesso | Expira em **1 hora** |
| Renovação | Via `refresh_token` (automática pela biblioteca) |
| Endpoint LWA | `https://api.amazon.com/auth/o2/token` |

### Credenciais necessárias
```
AMAZON_CLIENT_ID=
AMAZON_CLIENT_SECRET=
AMAZON_REFRESH_TOKEN=
AMAZON_AWS_ACCESS_KEY=
AMAZON_AWS_SECRET_KEY=
AMAZON_AWS_ROLE_ARN=
AMAZON_MARKETPLACE_ID=A2Q3Y263D00KWC  # Brasil
```

---

## Biblioteca Python Recomendada

**`python-amazon-sp-api`** — wrapper completo com renovação automática de token.

- GitHub: https://github.com/saleweaver/python-amazon-sp-api
- PyPI: https://pypi.org/project/python-amazon-sp-api/
- Docs: https://python-amazon-sp-api.readthedocs.io/

```bash
pip install python-amazon-sp-api
```

### Exemplo básico
```python
from sp_api.api import Products
from sp_api.base import Marketplaces

products = Products(marketplace=Marketplaces.BR)
result = products.get_competitive_pricing_for_asin(asin="B09XYZ")
```

---

## APIs Relevantes para o Negócio

| API | Uso |
|---|---|
| `Products` | Preços competitivos por ASIN |
| `Catalog` | Detalhes de produto, categorias |
| `Listings` | Criar e gerenciar anúncios |
| `Orders` | Consultar pedidos recebidos |
| `Reports` | Relatórios de vendas e inventário |
| `FBAInventory` | Estoque no fulfillment da Amazon |

---

## Pré-requisitos para Ativar

1. Ter conta de vendedor na Amazon Brasil (Seller Central)
2. Registrar aplicação em: https://developer-docs.amazon.com/sp-api/docs/registering-your-application
3. Obter aprovação para os roles necessários (Catalog, Listings, Orders)
4. Gerar `CLIENT_ID`, `CLIENT_SECRET` e `REFRESH_TOKEN`
5. Criar usuário IAM na AWS com permissões SP-API
6. Salvar todas as credenciais no `.env`

---

## Plano de Implementação

### Fase 1 — Pesquisa de mercado (pré-conta)
Mesmo sem conta Amazon, é possível consultar preços públicos via scraping ou APIs de terceiros (ex: Keepa, Jungle Scout). Avaliar custo-benefício antes de abrir conta.

### Fase 2 — Conta criada
Criar `tools/amazon_api.py` com autenticação LWA e endpoints de Products + Listings.

---

## Fontes
- [SP-API Documentação Oficial](https://developer-docs.amazon.com/sp-api)
- [python-amazon-sp-api — GitHub](https://github.com/saleweaver/python-amazon-sp-api)
- [python-amazon-sp-api — PyPI](https://pypi.org/project/python-amazon-sp-api/)
- [Tutorial Python SDK — Amazon](https://developer-docs.amazon.com/sp-api/docs/tutorial-automate-your-sp-api-calls-using-python-sdk)
