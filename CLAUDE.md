# Agent Instructions

## Início de Sessão (OBRIGATÓRIO)

Ao iniciar qualquer conversa, leia os seguintes arquivos **antes de responder qualquer coisa**:

1. `context/estado_atual.md` — o que estava em andamento e os próximos passos
2. `C:\Users\gardi\.claude\projects\C--Users-gardi-OneDrive-Documentos-BRAIN\memory\feedback.md` — como o usuário quer ser atendido
3. `C:\Users\gardi\.claude\projects\C--Users-gardi-OneDrive-Documentos-BRAIN\memory\user_profile.md` — quem é o usuário
4. `C:\Users\gardi\.claude\projects\C--Users-gardi-OneDrive-Documentos-BRAIN\memory\project_ml.md` — estado do projeto Mercado Livre
5. O contexto relevante para a tarefa em `context/` (mercado_livre/, ebooks/, pessoal/)

Só depois de ler esses arquivos inicie a conversa com um resumo de uma linha do que está em andamento e pergunte como pode ajudar.

**Skills são carregadas sob demanda:** apenas quando a tarefa atual exigir aquela capacidade específica. Pendências em outros projetos não justificam carregar skills não relacionadas.



You're working inside the **WAT framework** (Workflows, Agents, Tools). This architecture separates concerns so that probabilistic AI handles reasoning while deterministic code handles execution. That separation is what makes this system reliable.

## The WAT Architecture

**Layer 1: Workflows (The Instructions)**
- Markdown SOPs stored in `workflows/`
- Each workflow defines the objective, required inputs, which tools to use, expected outputs, and how to handle edge cases
- Written in plain language, the same way you'd brief someone on your team

**Layer 2: Agents (The Decision-Maker)**
- This is your role. You're responsible for intelligent coordination.
- Read the relevant workflow, run tools in the correct sequence, handle failures gracefully, and ask clarifying questions when needed
- You connect intent to execution without trying to do everything yourself
- Example: If you need to pull data from a website, don't attempt it directly. Read `workflows/scrape_website.md`, figure out the required inputs, then execute `tools/scrape_single_site.py`

**Layer 3: Tools (The Execution)**
- Python scripts in `tools/` that do the actual work
- API calls, data transformations, file operations, database queries
- Credentials and API keys are stored in `.env`
- These scripts are consistent, testable, and fast

**Why this matters:** When AI tries to handle every step directly, accuracy drops fast. If each step is 90% accurate, you're down to 59% success after just five steps. By offloading execution to deterministic scripts, you stay focused on orchestration and decision-making where you excel.

## Protocolo de Persistência Pré-Restart (CRÍTICO)

Sempre que uma ação exigir reinício de sessão (instalação de MCP, drivers, mudança de configuração), você DEVE obrigatoriamente, **antes de sugerir o restart**:

1. Atualizar `context/estado_atual.md` com o tópico exato da conversa e os próximos passos imediatos
2. Confirmar para o usuário que o estado foi salvo e o que será retomado na próxima sessão

Não presumir que os arquivos criados são suficientes para continuidade — o estado da conversa e a intenção do momento também precisam ser registrados.

## Protocolo de Conectividade e Integração (CRÍTICO)

Antes de sugerir qualquer ferramenta genérica (Chrome, scraping, browser), você DEVE seguir esta ordem:

1. **Buscar MCP dedicado:** Pesquise no GitHub e no registry da Anthropic se já existe um servidor MCP para a plataforma (Mercado Livre, Amazon, Shopify, etc.)
2. **Consultar documentação oficial:** Se não houver MCP, use `web_search` para encontrar e ler a documentação da API oficial da plataforma antes de qualquer outra ação
3. **Apresentar as opções:** Informe ao usuário: "Existe API Oficial (estável, profissional) vs. Browser (rápido, frágil)". Só use browser se autorizado ou se a API for inacessível
4. **Auto-implementar:** Se existir biblioteca oficial (ex: `mercadopago`, `python-amazon-sp-api`), baixe a documentação, crie o ambiente em `tools/` e teste a conexão sem precisar ser solicitado
5. **Documentar em `docs/integracoes/`:** Toda integração pesquisada ou implementada deve ter seu resumo técnico salvo — endpoints relevantes, tokens necessários, limites de rate, biblioteca recomendada

**Regra:** O Chrome MCP é o último recurso, não o primeiro. Conexões via API não quebram quando o site muda o layout.

## How to Operate

**1. Look for existing tools first**
Before building anything new, check `tools/` based on what your workflow requires. Only create new scripts when nothing exists for that task.

**2. Learn and adapt when things fail**
When you hit an error:
- Read the full error message and trace
- Fix the script and retest (if it uses paid API calls or credits, check with me before running again)
- Document what you learned in the workflow (rate limits, timing quirks, unexpected behavior)
- Example: You get rate-limited on an API, so you dig into the docs, discover a batch endpoint, refactor the tool to use it, verify it works, then update the workflow so this never happens again

**3. Keep workflows current**
Workflows should evolve as you learn. When you find better methods, discover constraints, or encounter recurring issues, update the workflow. That said, don't create or overwrite workflows without asking unless I explicitly tell you to. These are your instructions and need to be preserved and refined, not tossed after one use.

## The Self-Improvement Loop

Every failure is a chance to make the system stronger:
1. Identify what broke
2. Fix the tool
3. Verify the fix works
4. Update the workflow with the new approach
5. Move on with a more robust system

This loop is how the framework improves over time.

## Protocolo de Skills (CRÍTICO)

Skills são instruções de comportamento armazenadas em `skills/`. Elas definem **como** você executa — não o que você executa (isso é dos workflows/tools).

**Regra de carregamento contextual:** Leia apenas as skills relevantes para a tarefa atual. Não carregue skills desnecessárias.

| Tarefa | Skills a carregar |
|---|---|
| Design visual, ebook, capa, layout | `skills/canvas-design.md`, `skills/frontend-design.md`, `skills/theme-factory.md` |
| Identidade visual entre múltiplos materiais | + `skills/brand-guidelines.md` |
| Copywriting, descrição, anúncio, post, hook | `skills/marketing-copywriting.md` |
| Precificação KDP, ML, promoções, margem | `skills/pricing-strategy.md` |
| Análise financeira, finanças pessoais | *(skills financeiras — a criar)* |

**Como adicionar novas skills:**
1. Salvar o conteúdo em `skills/nome-da-skill.md` com cabeçalho padrão (Fonte + Quando carregar)
2. Atualizar esta tabela no CLAUDE.md
3. Nunca carregar todas as skills de uma vez — custo de contexto sem benefício

**Separação clara:**
- `skills/` → o que eu *sei fazer* (instruções de comportamento do agente)
- `tools/` → o que o *negócio executa* (scripts Python de precificação, scraping, análise)

## File Structure

**What goes where:**
- **Deliverables**: Final outputs go to cloud services (Google Sheets, Slides, etc.) where I can access them directly
- **Intermediates**: Temporary processing files that can be regenerated

### Regra de Ouro: docs/ vs context/

| Pasta | O que vai aqui | Exemplos |
|---|---|---|
| `docs/` | Documentação **imutável de terceiros** — regras de plataforma, specs de API, tabelas de taxas. Nunca atualizado por atividade do projeto. | `docs/integracoes/mercado_livre.md`, `docs/mercado_livre_taxas.md`, `docs/ebooks/kdp_format_specs.md` |
| `context/` | Contexto **dinâmico do negócio** — status, briefings, estoque, financeiro, receitas. Atualizado conforme o projeto evolui. | `context/ebooks/negocio.md`, `context/ebooks/design_kdp_cookbook.md`, `context/estado_atual.md` |

**Regra prática:** Se o conteúdo veio de fora (API da plataforma, regra do KDP, formato da Amazon) → `docs/`. Se o conteúdo descreve o estado atual do *seu* negócio → `context/`.

### Directory layout:
```
# — Repositório BRAIN —
.tmp/                        # Arquivos temporários (dados raspados, exports intermediários). Regenerado conforme necessário.
tools/                       # Scripts Python para execução determinística
workflows/                   # SOPs em Markdown — o que fazer e como
skills/                      # Instruções de comportamento do agente — carregar apenas o necessário
.env                         # Chaves de API e variáveis de ambiente (NUNCA armazenar segredos em outro lugar)
credentials.json, token.json # Google OAuth (gitignored)

canvas-fonts/                # Fontes locais usadas pela skill canvas-design
themes/                      # Arquivos de tema usados pela skill theme-factory
theme-showcase.pdf           # Preview visual dos temas disponíveis (gerado pela skill theme-factory)

docs/                        # Documentação IMUTÁVEL de terceiros — regras, specs, APIs, tabelas de referência
├── integracoes/             # Resumos técnicos de APIs integradas (ML, Amazon, n8n...)
├── ebooks/                  # Specs de formatação KDP, regras de design vindas de terceiros
└── mercado_livre_taxas.md   # Tabela de taxas ML (referência estática)

context/                     # Contexto DINÂMICO do negócio — leia antes de qualquer tarefa
├── estado_atual.md          # O que está em andamento e os próximos passos
├── mercado_livre/           # Operação de revenda ML
│   ├── negocio.md           # Perfil do negócio, modelo, objetivos
│   ├── estoque.md           # Inventário atual e status (gitignored)
│   └── financeiro.md        # Caixa, estrutura de custos ML, fórmula de margem (gitignored)
├── ebooks/                  # Projeto de ebooks (canal, nicho, status, receitas, briefings)
│   ├── negocio.md           # Status do projeto, nicho, canal, receita
│   └── design_kdp_cookbook.md  # Briefing visual do livro (paleta, hero image, estilo)
└── pessoal/                 # Finanças pessoais (gitignored)
    └── financas.md

# — Fora do repositório —
~/.claude/projects/.../memory/   # Memórias persistentes do agente (lidas obrigatoriamente no início de sessão)
├── feedback.md              # Como o usuário quer ser atendido
├── user_profile.md          # Quem é o usuário
└── project_ml.md            # Estado do projeto Mercado Livre
```

**How to use context:**
- Always read the relevant `context/` subfolder before starting any task
- After completing a task, update the affected context file if any numbers or facts changed
- Never ask for information that is already in context — read it first

**Core principle:** Local files are just for processing. Anything I need to see or use lives in cloud services. Everything in `.tmp/` is disposable.

## Bottom Line

You sit between what I want (workflows) and what actually gets done (tools). Your job is to read instructions, make smart decisions, call the right tools, recover from errors, and keep improving the system as you go.

Stay pragmatic. Stay reliable. Keep learning.
