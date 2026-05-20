# Integração — Mercado Livre API

_Última atualização: 2026-05-12_

---

## Decisão de Arquitetura

| Opção | Status | Uso |
|---|---|---|
| MCP `newerton/mcp-mercado-livre` | **Quebrado** — ML serve anti-bot challenge sem JS | Descartado |
| API REST Oficial | **Funcional** — requer token de app | Usar para pesquisa e gestão |
| Chrome MCP | Último recurso | Só se API falhar |

**Causa raiz do MCP:** o scraper busca `lista.mercadolivre.com.br` que retorna página de micro-landing (5KB, anti-bot) ao invés do HTML de produtos. Seletores CSS nunca encontram items.

---

## Aplicativo Criado — BRAIN Mercado Livre

| Campo | Valor |
|---|---|
| Nome | BRAIN Mercado Livre |
| Client ID | 2188140758440937 |
| Redirect URI | https://www.google.com |
| Fluxos OAuth | Authorization Code, Client Credentials, Refresh Token |
| Negócio | Mercado Livre |

**Permissões configuradas (2026-05-12):**

| Permissão | Nível |
|---|---|
| Usuários | Leitura e escrita |
| Comunicações pré e pós-vendas | Leitura |
| Publicação e sincronização | Leitura e escrita |
| Publicidade de um produto | Sem acesso |
| Faturamento de uma venda | Leitura e escrita |
| Métricas do negócio | Leitura |
| Promoções, cupons e descontos | Leitura e escrita |
| Venda e envios de um produto | Leitura |

**Nota:** Permissões mais amplas do que o necessário no momento. Recomenda-se reduzir "escrita" e remover faturamento/comunicações quando for editar o app. Expandir conforme funcionalidades forem implementadas.

**Limitação conhecida:** `/sites/MLB/search` retorna 403 — bloqueado pelo ML para apps não certificadas. Endpoints funcionais: `/users/me`, `/users/{id}/items/search`.

---

## Criar Aplicação (Obter Credenciais)

**Link direto:** https://developers.mercadolivre.com.br/pt_br/crie-uma-aplicacao-no-mercado-livre

**Passos:**
1. Login com conta ML em https://developers.mercadolivre.com.br
2. Ir em "Minhas Aplicações" → "Criar nova aplicação"
3. Preencher nome, descrição, Redirect URI (pode ser `https://localhost` para testes)
4. Selecionar scopes: `read`, `write`, `offline_access`
5. Salvar → receber `APP_ID` (= CLIENT_ID) e `SECRET_KEY` (= CLIENT_SECRET)

**Salvar no `.env`:**
```
ML_CLIENT_ID=<APP_ID>
ML_CLIENT_SECRET=<SECRET_KEY>
ML_ACCESS_TOKEN=
ML_REFRESH_TOKEN=
```

---

## Autenticação OAuth 2.0

### Endpoint de Token
```
POST https://api.mercadolibre.com/oauth/token
```

### Obter Access Token (Authorization Code Flow)

**1. Redirecionar usuário para autorização:**
```
https://auth.mercadolivre.com.br/authorization
  ?response_type=code
  &client_id={CLIENT_ID}
  &redirect_uri={REDIRECT_URI}
```

**2. Trocar code por token:**
```http
POST https://api.mercadolibre.com/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&client_id={CLIENT_ID}
&client_secret={CLIENT_SECRET}
&code={AUTHORIZATION_CODE}
&redirect_uri={REDIRECT_URI}
```

**Resposta:**
```json
{
  "access_token": "APP_USR-...",
  "token_type": "bearer",
  "expires_in": 10800,
  "refresh_token": "TG-...",
  "scope": "offline_access read write",
  "user_id": 123456789
}
```

### Renovar Token (Refresh)
```http
POST https://api.mercadolibre.com/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&client_id={CLIENT_ID}
&client_secret={CLIENT_SECRET}
&refresh_token={REFRESH_TOKEN}
```

> **Importante:** o refresh retorna um NOVO refresh_token — sempre salvar o mais recente.

### Validade dos Tokens
| Token | Validade |
|---|---|
| `access_token` | 6 horas (10.800 segundos) |
| `refresh_token` | 6 meses |

### Segurança
- Parâmetros SEMPRE no body da requisição, nunca como query params
- Usar `Authorization: Bearer {access_token}` no header de todas as chamadas

---

## Scopes

| Scope | Permissão |
|---|---|
| `read` | GET — buscar produtos, pedidos, dados da conta |
| `write` | PUT/POST/DELETE — criar e editar anúncios |
| `offline_access` | Renovar token sem usuário online (essencial para automação) |

---

## Endpoints Principais

### Busca Pública de Produtos
```
GET https://api.mercadolibre.com/sites/MLB/search?q={query}&limit=50
Authorization: Bearer {access_token}
```

> **Nota:** O endpoint `/sites/MLB/search` requer token mesmo para dados públicos. Retorna 403 sem autenticação.

**Parâmetros úteis:**
| Parâmetro | Descrição |
|---|---|
| `q` | Termo de busca |
| `limit` | Itens por página (máx. 100, default 50) |
| `offset` | Paginação |
| `sort` | `price_asc`, `price_desc`, `relevance` |
| `category` | ID da categoria ML |

**Campos retornados por item:**
- `id`, `title`, `price`, `currency_id`
- `sold_quantity`, `available_quantity`
- `seller.id`, `seller.nickname`, `seller.seller_reputation`
- `shipping.free_shipping`, `shipping.logistic_type`
- `permalink` (link do anúncio)

### Detalhe de Item
```
GET https://api.mercadolibre.com/items/{item_id}
Authorization: Bearer {access_token}
```

### Meus Anúncios
```
GET https://api.mercadolibre.com/users/{user_id}/items/search
Authorization: Bearer {access_token}
```

### Categorias
```
GET https://api.mercadolibre.com/sites/MLB/categories
GET https://api.mercadolibre.com/categories/{category_id}
```

---

## Rate Limits

| Nível | Limite |
|---|---|
| Padrão | 18.000 requests/hora |
| Erro por excesso | `429 local_rate_limited` — aguardar alguns segundos |

---

## Plano de Implementação

### Fase 1 — Pesquisa de Mercado (agora)
Implementar `tools/ml_search.py`:
- Autenticar com CLIENT_ID + CLIENT_SECRET
- Buscar top resultados de qualquer query
- Retornar: nome, preço, vendidos, frete grátis, link

### Fase 2 — Gestão de Anúncios (quando escalar)
Implementar `tools/ml_listings.py`:
- Listar meus anúncios ativos
- Atualizar preço via PUT
- Monitorar estoque

---

## Fontes
- [Criar Aplicação](https://developers.mercadolivre.com.br/pt_br/crie-uma-aplicacao-no-mercado-livre)
- [Autenticação e Autorização](https://developers.mercadolivre.com.br/en_us/authentication-and-authorization)
- [Items & Buscas](https://developers.mercadolivre.com.br/pt_br/itens-e-buscas)
- [Gerenciar Aplicações](https://developers.mercadolivre.com.br/en_us/manage-your-applications)
- [Application Manager](https://developers.mercadolivre.com.br/en_us/application-manager)
