# ForgeBase

**ForgeBase** é o núcleo técnico do Forge Framework — a infraestrutura cognitiva onde o raciocínio do ForgeProcess se transforma em código observável, reflexivo e modular.

---

## 🤖 For AI Coding Agents

**First time using ForgeBase?** Access complete API documentation programmatically:

```python
from forgebase.dev import get_agent_quickstart

# Get the full AI Agent Quick Start guide (embedded in package)
guide = get_agent_quickstart()
print(guide)  # Full markdown with examples and API reference
```

**Available APIs for AI Agents:**

```python
from forgebase.dev.api import (
    QualityChecker,      # Code quality checks (ruff, mypy)
    ScaffoldGenerator,   # Generate boilerplate code
    ComponentDiscovery,  # Discover entities, usecases, ports
    TestRunner          # Run tests programmatically
)

# Example: Quality check before commit
checker = QualityChecker()
results = checker.run_all()

for tool, result in results.items():
    if not result.passed:
        for error in result.errors:
            # Each error has: file, line, column, code, message
            print(f"Fix {error['file']}:{error['line']} - {error['code']}")
```

**Why this matters:**
- ✅ Works offline (docs embedded in package)
- ✅ Structured, machine-readable results (not CLI text parsing)
- ✅ Auto-discovery of components and architecture
- ✅ Integrated quality checking and code generation

📚 **Complete guide:** See [docs/agentes-ia/](docs/agentes-ia/) for full documentation with error codes, data structures, and workflow examples.

---

## ⚡ Quick Start

### Installation

```bash
# Install from GitHub
pip install git+https://github.com/symlabs-ai/forgebase.git

# Or clone for development
git clone https://github.com/symlabs-ai/forgebase.git
cd forgebase
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### For AI Agents (Programmatic Access)

```python
# Documentation is embedded in the package - works offline!
from forgebase.dev import get_agent_quickstart

guide = get_agent_quickstart()  # Full API documentation
# Parse and use to discover available APIs
```

### For Developers (CLI)

```bash
# Run quality checks
python devtool.py quality

# Generate boilerplate
python devtool.py scaffold usecase CreateOrder

# Run tests
python devtool.py test
```

---

## 🏗️ Estrutura do Repositório

```
forgebase/
├── docs/                 # Documentação completa (reorganizada)
│   ├── usuarios/         # Guias para desenvolvedores humanos
│   ├── agentes-ia/       # Documentação para AI agents
│   ├── referencia/       # Referência técnica e arquitetura
│   └── adr/              # Architecture Decision Records
├── examples/             # Exemplos de uso do framework
├── scripts/              # Scripts de desenvolvimento (scaffolding, discovery)
├── src/                  # Código-fonte do framework ForgeBase
│   └── forgebase/
│       ├── domain/           # Camada de Domínio
│       ├── application/      # Camada de Aplicação
│       ├── infrastructure/   # Camada de Infraestrutura
│       ├── integration/      # Adaptadores e integrações
│       └── observability/    # Sistema de observabilidade
├── tests/                # Testes (unit, integration, property-based, contract)
├── devtool.py           # CLI unificada para desenvolvimento
├── pyproject.toml       # Configuração do projeto (PEP 621)
├── setup.py             # Shim para backward compatibility
├── CHANGELOG.md         # Histórico de mudanças
├── CONTRIBUTING.md      # Guia de contribuição
├── VERSION.MD           # Versão atual do projeto
└── README.md            # Este arquivo
```

### 📂 Detalhamento das Pastas

#### `docs/`
Documentação completa do projeto, organizada por público-alvo:
- **usuarios/** — Guias para desenvolvedores (início rápido, receitas, testes)
- **agentes-ia/** — Documentação para AI agents (APIs, descoberta, ecossistema)
- **referencia/** — Referência técnica (ForgeProcess, arquitetura, backlog)
- **adr/** — Architecture Decision Records

#### `examples/`
Exemplos práticos de uso do framework:
- **user_management/** — Sistema completo de gerenciamento de usuários
  - Demonstra Clean Architecture na prática
  - Inclui domínio (User, Email), aplicação (CreateUserUseCase) e infraestrutura (JSONUserRepository)

#### `scripts/`
Ferramentas de desenvolvimento:
- **scaffold.py** — Gerador de boilerplate (UseCases, Ports, Adapters)
- **discover.py** — Descoberta e catalogação de componentes
- **mypy.ini** — Configuração de type checking

#### `src/forgebase/`
Código-fonte seguindo Clean + Hexagonal Architecture:

**`domain/`** — Camada de Domínio (núcleo do negócio)
- `entity_base.py` — Classe base para entidades com identidade imutável
- `value_object_base.py` — Classe base para value objects imutáveis
- `exceptions.py` — Exceções de negócio (BusinessRuleViolation, ValidationError)

**`application/`** — Camada de Aplicação (orquestração)
- `usecase_base.py` — Classe base genérica para casos de uso
- `port_base.py` — Classe base para portas (abstrações de I/O)
- `dto_base.py` — Classe base para DTOs (Data Transfer Objects)

**`infrastructure/`** — Camada de Infraestrutura (implementações)
- `config/` — Gerenciamento de configurações (YAML, environment)
- `repository/` — Implementações do padrão Repository
  - `repository_base.py` — Interface abstrata do Repository Pattern
  - `json_repository.py` — Repository com armazenamento em JSON (dev/testing)
  - `sql_repository.py` — Repository com SQLAlchemy (produção)

**`integration/`** — Adaptadores externos
- Adaptadores para sistemas externos, APIs, etc.

**`observability/`** — Sistema de observabilidade nativo
- Decoradores e utilitários para métricas, logging e tracing

#### `tests/`
Suíte de testes completa:
- **unit/** — Testes unitários isolados
- **integration/** — Testes de integração entre componentes
- **property_based/** — Testes baseados em propriedades (Hypothesis)
- **contract_tests/** — Testes de contratos entre camadas

#### `devtool.py`
CLI unificada para desenvolvimento:
```bash
python devtool.py scaffold      # Gerar boilerplate
python devtool.py discover      # Catalogar componentes
python devtool.py test          # Executar testes
python devtool.py lint          # Linters (Ruff, Mypy)
python devtool.py check-deps    # Validar dependências
python devtool.py check-arch    # Validar arquitetura
python devtool.py quality       # Suite completa de qualidade
```

### 📄 Arquivos de Configuração

#### `pyproject.toml`
Configuração moderna seguindo PEP 621:
- Metadados do projeto e dependências
- Configuração de ferramentas (pytest, mypy, ruff, coverage, deptry)
- Fonte única de verdade para todo o projeto

#### `.import-linter`
Validação de boundaries da Clean Architecture:
- Garante que camadas não violem dependências
- Domain não pode importar Application/Infrastructure
- Application não pode importar Infrastructure

#### `VERSION.MD`
Rastreamento da versão atual do projeto

#### `CHANGELOG.md`
Histórico detalhado de mudanças por versão

---

## 🧠 Filosofia

> "Forjar é transformar pensamento em estrutura."

ForgeBase não é apenas um framework técnico — é uma **arquitetura cognitiva** que:
- **Pensa**: Cada componente carrega intenção e propósito
- **Mede**: Observabilidade nativa em todos os níveis
- **Explica**: Capacidade de auto-reflexão e documentação viva

### Princípios Fundamentais

1. **Reflexividade** — O código entende e explica seu próprio funcionamento
2. **Autonomia** — Módulos independentes com contratos bem definidos
3. **Coerência Cognitiva** — Padrões consistentes em toda a arquitetura

---

## 🚀 Status do Projeto

**Versão Atual:** v0.1.7 (Production-Ready)

### ✅ Completo (FASE 1 - Foundation)

**Domain Layer**
- ✅ EntityBase com ID imutável (property-based)
- ✅ ValueObjectBase com igualdade estrutural
- ✅ Exceções de negócio (BusinessRuleViolation, ValidationError)

**Application Layer**
- ✅ UseCaseBase genérico (Generic[TInput, TOutput])
- ✅ PortBase para abstrações de I/O
- ✅ DTOBase para transferência de dados

**Infrastructure Layer**
- ✅ RepositoryBase (Repository Pattern do DDD)
- ✅ JSONRepository (thread-safe, development/testing)
- ✅ SQLRepository (SQLAlchemy, production-ready)
- ✅ ConfigLoader (YAML + environment variables)

**Developer Tooling**
- ✅ devtool.py (CLI unificada)
- ✅ Scaffolding (geração de boilerplate)
- ✅ Discovery (catalogação de componentes)
- ✅ Modern dependency management (pyproject.toml)
- ✅ Import standardization (100% absolute imports)
- ✅ Cross-platform support

**Quality Assurance**
- ✅ 84+ testes passing (unit + integration + property-based + contract)
- ✅ Mypy strict type checking
- ✅ Ruff linting + pre-commit hooks
- ✅ Import-linter (architecture boundary validation)
- ✅ Deptry (dependency hygiene)

### 🚧 Em Desenvolvimento (FASE 2)

**Observability**
- 🚧 Métricas nativas
- 🚧 Decoradores de observabilidade
- 🚧 Sistema de logging estruturado

**Integration Layer**
- 🚧 Adaptadores para sistemas externos
- 🚧 API adapters (REST, GraphQL)

### 📋 Backlog

Consulte o [CHANGELOG.md](/CHANGELOG.md) para histórico detalhado de mudanças.

Consulte o [docs/referencia/backlog.md](/docs/referencia/backlog.md) para o roadmap completo com 54 componentes organizados em 8 fases.

---

## 📖 Documentação

Para entender a arquitetura completa, consulte:

### Para Desenvolvedores
- [ForgeBase Rules](/docs/usuarios/forgebase-rules.md) — **Guia completo de regras e práticas**
- [Início Rápido](/docs/usuarios/inicio-rapido.md) — Instalação e primeiros passos
- [Receitas](/docs/usuarios/receitas.md) — Exemplos práticos de uso
- [Guia de Testes](/docs/usuarios/guia-de-testes.md) — Como executar e escrever testes
- [CLI First](/docs/usuarios/cli-first.md) — Filosofia de desenvolvimento CLI First
- [Ambiente e Scripts](/docs/usuarios/ambiente_e_scripts.md) — Setup de ambiente e ferramentas
- [Extensão](/docs/usuarios/extending-forgebase.md) — Como estender ForgeBase

### Para AI Agents
- [Início Rápido](/docs/agentes-ia/inicio-rapido.md) — Quick start para agentes de IA
- [Guia Completo](/docs/agentes-ia/guia-completo.md) — Referência completa de APIs
- [Descoberta](/docs/agentes-ia/descoberta.md) — Sistema de descoberta de APIs
- [Ecossistema](/docs/agentes-ia/ecossistema.md) — Integração com ferramentas

### Referência Técnica
- [ForgeProcess](/docs/referencia/forge-process.md) — Ciclo cognitivo de desenvolvimento
- [Arquitetura](/docs/referencia/arquitetura.md) — Modularização do núcleo
- [Backlog](/docs/referencia/backlog.md) — Roadmap (8 fases, 54 componentes)
- [Guia de Documentação](/docs/referencia/documentation_guide.md) — Padrões de docstrings

---
## 🛠️ AVISOS IMPORTANTES
- Nunca grave nada na raíz sem solitacao explicita do usuario
- Nunca de push no repositorio remoto sem solitacao explicita do usuario
- Nunca crie tags ou aumente versao do forgebase sem solitacao explicita do usuario
- A fonte da verdade sobre a versao atual, bem como historico sintetico pode ser encontrada em VERSION.md

## 🛠️ Tecnologias

- **Python 3.11+**
- **Clean Architecture** + **Hexagonal Architecture**
- **Observabilidade Nativa** (Logging, Métricas, Tracing)
- **Test-Driven Development**

---
