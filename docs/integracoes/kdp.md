# Integração — Amazon KDP (publicação de ebooks)

_Última atualização: 2026-05-25_

## Veredicto de Arquitetura

**KDP não tem API pública de upload.** A KDP Reports API existe mas é só leitura (royalties). Para publicar livros, browser automation é a única via legítima.

Stack escolhida: **Patchright** (fork do Playwright com Chromium patcheado anti-detect) + perfil persistente (`user_data_dir`).

---

## Por que Patchright (e não Camoufox ou Playwright puro)

A Amazon usa detecção em múltiplas camadas:

| Camada | Detecção | Quem evade |
|---|---|---|
| JS-level (`navigator.webdriver`, plugins) | Sim | Patchright (built-in), playwright-stealth |
| Canvas/WebGL fingerprint | Sim | Patchright (built-in), Camoufox |
| TLS handshake (JA3/JA4) | Sim | Camoufox + Patchright (parcial) |
| Distribuição estatística de fingerprints | Sim | Camoufox (gerador BrowserForge) |

**Histórico das tentativas:**
1. ❌ **SeleniumBase + Playwright CDP** (original) — detectado pela Amazon, várias bugs de URL/seletor
2. ❌ **Camoufox** (Firefox C++ fork) — abandonou builds Windows desde mar/2025. Última versão Windows (v135 beta 24) tem bug de manifest SxS que impede inicialização. **Inviável em Windows.**
3. ✅ **Patchright** — drop-in replacement do Playwright com stealth built-in, sem binário customizado. Funciona em Windows.

Patchright cobre as duas primeiras camadas perfeitamente. TLS-level é parcial mas suficiente pro KDP (que não é tão paranoico quanto Cloudflare-protected sites).

---

## Arquitetura do fluxo

```
┌──────────────────────────────┐         ┌──────────────────────────────┐
│ kdp_session_bootstrap.py     │         │ kdp_upload.py                │
│ (roda 1x, manual)            │         │ (roda toda vez que publica)  │
├──────────────────────────────┤         ├──────────────────────────────┤
│ Abre Patchright visível      │         │ Reabre o mesmo perfil Chrome │
│ Você loga + resolve CAPTCHA  │   →     │ Entra direto no Bookshelf    │
│ Auto-detecta Bookshelf URL   │         │ Preenche metadados, upload   │
│ Perfil salvo em ~/.kdp/      │         │ Publica                      │
└──────────────────────────────┘         └──────────────────────────────┘
```

### Perfil persistente
- Caminho: `~/.kdp/chrome_profile/` (fora do repo, gitignored por padrão)
- Conteúdo: perfil Chrome completo (cookies, localStorage, IndexedDB, settings)
- Validade: ~30 dias (Amazon força reauth)
- Renovação automática: perfil é re-salvo continuamente pelo Chromium
- Fallback: se expirou, script aborta e pede pra rodar bootstrap de novo

---

## Instalação

```bash
pip install -U patchright python-dotenv
python -m patchright install chromium    # baixa Chromium patcheado (~180 MB)
```

Armazenamento: `~/AppData/Local/ms-playwright/chromium-XXXX/` (Windows).

---

## Uso

### Primeira vez (ou sessão expirada)
```bash
python tools/kdp_session_bootstrap.py
```
1. Chrome abre na tela de login do KDP
2. Você loga normalmente, resolve CAPTCHA se aparecer
3. **Quando chegar no Bookshelf, o script detecta sozinho e fecha**
4. Perfil salvo em `~/.kdp/chrome_profile/`

### Toda vez que for publicar
```bash
python tools/kdp_upload.py
```
- Edita o dict `BOOK` no topo de `kdp_upload.py` antes de rodar
- Browser abre visível, você acompanha cada etapa
- Script pausa em 3 pontos críticos pra revisão (Enter pra prosseguir)
- Screenshots de cada etapa salvos em `.tmp/kdp_*.png`

---

## Mapa do fluxo de publicação no KDP

Captura dos seletores DOM importantes (a Amazon mexe nisso de tempos em tempos — se o script quebrar, atualizar aqui).

### URLs principais
| Função | URL |
|---|---|
| Login | `https://www.amazon.com/ap/signin?openid.return_to=https://kdp.amazon.com/bookshelf&openid.assoc_handle=amzn_dtp&pageId=kdp-ap&openid.ns=http://specs.openid.net/auth/2.0` |
| Bookshelf | `https://kdp.amazon.com/en_US/bookshelf` |
| Novo ebook | `https://kdp.amazon.com/en_US/title-setup/kindle/new/details` |

### Etapa 1 — Book Details
| Campo | Seletor |
|---|---|
| Idioma | `select[id*='language']` |
| Título | `input[id*='book-title']:not([id*='subtitle'])` |
| Subtítulo | `input[id*='subtitle']` |
| Autor (nome) | `input[id*='first-name'], input[name*='firstName']` |
| Autor (sobrenome) | `input[id*='last-name'], input[name*='lastName']` |
| Descrição | `textarea[id*='description'], div[contenteditable='true'][id*='description']` |
| Copyright owner | `input[value='COPYRIGHT_OWNER']` |
| Keywords (7 campos) | `input[id*='keyword']` (use `.nth(0..6)`) |
| Avançar | `button:has-text('Save and Continue')` |

### Etapa 2 — Content
| Arquivo | Seletor |
|---|---|
| Manuscrito | `input[type='file']` (primeiro) |
| Capa | `input[type='file']` (segundo) |

Aguardar 10–60s para processamento após upload. Se aparecer erro vermelho, arquivo foi rejeitado.

### Etapa 3 — Pricing
| Campo | Seletor |
|---|---|
| KDP Select | `input[id*='kdp-select']` |
| Royalty 70% | `input[value='0.70'], label:has-text('70%')` |
| Preço US | `input[id*='price'][id*='us'], input[id*='listPrice']` |
| Publicar | `button:has-text('Publish Your Kindle eBook'), button:has-text('Publish')` |

---

## Troubleshooting

| Sintoma | Causa provável | Fix |
|---|---|---|
| `Perfil Chrome KDP não existe` | Bootstrap não rodou | `python tools/kdp_session_bootstrap.py` |
| Browser abre e cai no `/ap/signin` | Sessão expirou (~30 dias) | Rodar bootstrap de novo |
| Campo não preenche (`✗ title: TimeoutError`) | Amazon mudou seletor DOM | Atualizar seletor + atualizar tabela acima |
| Upload trava em "processing" | PDF/PNG não passou validação KDP | Conferir specs em `docs/ebooks/kdp_format_specs.md` |
| CAPTCHA aparece durante upload (raro) | Amazon flagou comportamento | Resolver manualmente, dar Enter, continuar |

---

## Custos e segurança

- **Patchright + Chromium:** open source, gratuito
- **CAPTCHA solver:** não implementado (perfil persistente evita CAPTCHAs recorrentes). Se virar problema, integrar `2captcha-mcp` ou `CapSolver` como fallback
- **Credenciais:** `AMAZON_EMAIL` e `AMAZON_PASSWORD` no `.env` (apenas fallback se quiser automatizar relogin no futuro — atualmente não usado, login é manual no bootstrap)

---

## Notas históricas

- **2026-05-25:** Camoufox tentado e descartado em Windows (bug de manifest no v135-beta.24, builds Windows abandonados pelo maintainer desde mar/2025). Migrado para Patchright.
- **2026-05-24:** Tentativa original com SeleniumBase + Playwright CDP — bugs de URL e seletor.
