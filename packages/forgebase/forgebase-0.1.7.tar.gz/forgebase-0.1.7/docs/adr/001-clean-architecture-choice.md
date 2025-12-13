# ADR-001: Clean Architecture Choice

## Status

**Aceita** (2025-11-03)

## Context

ForgeBase foi concebido como o núcleo técnico do Forge Framework, responsável por executar lógica de negócio definida pelo ForgeProcess. Precisávamos de uma arquitetura que:

- Isolasse a lógica de domínio de detalhes técnicos (UI, banco de dados, frameworks)
- Permitisse testabilidade máxima sem dependências externas
- Facilitasse manutenção e evolução ao longo do tempo
- Garantisse que decisões de negócio não fossem contaminadas por concerns técnicos
- Permitisse trocar implementações de infraestrutura sem afetar o core

### Forças em Jogo

**Positivas:**
- Necessidade de separação clara de responsabilidades
- Requisito de testabilidade independente de infraestrutura
- Expectativa de mudanças frequentes em adapters (CLI, HTTP, AI)
- Desejo de que o domínio seja "puro" e expressivo

**Negativas:**
- Potencial overhead de criar muitas camadas
- Curva de aprendizado para novos desenvolvedores
- Necessidade de disciplina para manter boundaries

## Decision

**Adotamos Clean Architecture como padrão arquitetural do ForgeBase.**

A implementação segue 4 camadas concêntricas:

```
┌─────────────────────────────────────────────┐
│           Adapters (External)               │  ← CLI, HTTP, AI
│  ┌───────────────────────────────────────┐  │
│  │     Application (Use Cases)           │  │  ← Orquestração
│  │  ┌─────────────────────────────────┐  │  │
│  │  │      Domain (Entities, VOs)     │  │  │  ← Regras de negócio
│  │  └─────────────────────────────────┘  │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### Regras de Dependência

1. **Domain** não depende de nada (zero imports externos ao domínio)
2. **Application** depende apenas de Domain
3. **Adapters** podem depender de Application e Domain
4. **Infrastructure** implementa contratos definidos por Application/Domain

### Implementação no ForgeBase

```python
# Domain Layer (src/forgebase/domain/)
- EntityBase: Entidades com identidade
- ValueObjectBase: Objetos de valor imutáveis
- Exceptions: ValidationError, BusinessRuleViolation
- Validators: Regras reutilizáveis

# Application Layer (src/forgebase/application/)
- UseCaseBase: Orquestração de lógica
- PortBase: Contratos de comunicação
- DTOBase: Data Transfer Objects

# Infrastructure Layer (src/forgebase/infrastructure/)
- RepositoryBase: Persistência
- ConfigLoader: Configurações
- LoggerPort: Logging

# Adapters Layer (src/forgebase/adapters/)
- CLIAdapter: Interface de linha de comando
- HTTPAdapter: API REST
```

### Enforcement

Usamos testes para garantir boundaries:
- Testes de importação validam zero dependências circulares
- Code review verifica violations
- Linting rules detectam imports proibidos

## Consequences

### Positivas

✅ **Testabilidade Máxima**
- Domain testável sem mocks (lógica pura)
- Application testável com fakes simples
- Adapters testáveis com ports mockados

✅ **Flexibilidade de Infraestrutura**
- Trocar de JSON para SQL sem afetar UseCases
- Adicionar novo adapter (gRPC, GraphQL) sem modificar core
- Migrar de CLI para HTTP sem reescrever lógica

✅ **Separação Clara de Concerns**
- Regras de negócio expressas em linguagem ubíqua
- Detalhes técnicos isolados em adapters
- Orquestração explícita em UseCases

✅ **Manutenibilidade**
- Mudanças localizadas em uma camada
- Evolução independente de cada layer
- Código mais fácil de entender e navegar

### Negativas

⚠️ **Overhead Inicial**
- Mais arquivos e abstrações
- Setup inicial mais complexo
- Necessidade de entender o padrão

⚠️ **Disciplina Necessária**
- Desenvolvedores precisam respeitar boundaries
- Tentação de "atalhos" violando camadas
- Code review crítico para manter padrão

⚠️ **Boilerplate**
- DTOs para entrada/saída
- Ports para cada dependência externa
- Mapeamento entre camadas

### Mitigações

Para minimizar as consequências negativas:

1. **Documentação Clara**: ADRs, guias, exemplos
2. **Code Generators**: Scaffolding automático de UseCases
3. **Linting**: Detecção automática de violations
4. **Exemplos**: Complete flow examples mostrando padrão
5. **Testing Utilities**: Fakes pré-construídos para acelerar testes

## Alternatives Considered

### 1. MVC/MTV (Model-View-Controller)

**Rejeitado porque:**
- Mistura concerns de apresentação com lógica de negócio
- Models frequentemente contaminados com detalhes de ORM
- Difícil testar controllers sem framework web
- Não expressa claramente regras de domínio

### 2. Layered Architecture Tradicional

**Rejeitado porque:**
- Permite dependências bidirecionais entre camadas
- Domain frequentemente acoplado a infraestrutura
- Difícil evitar "leaky abstractions"
- Não força isolamento do domínio

### 3. Microservices desde o início

**Rejeitado porque:**
- Overhead operacional desnecessário no início
- Complexidade de comunicação entre serviços
- Clean Architecture permite migrar para microservices depois
- ForgeBase é um framework, não uma aplicação distribuída

### 4. Flat Architecture (sem camadas)

**Rejeitado porque:**
- Tendência a criar "big ball of mud"
- Difícil manter separação de concerns
- Testes acoplados a infraestrutura
- Evolução caótica ao longo do tempo

## References

- **Clean Architecture** by Robert C. Martin (Uncle Bob)
- **Domain-Driven Design** by Eric Evans
- **Hexagonal Architecture** by Alistair Cockburn
- **ForgeBase PRD**: `/docs/guides/forgebase_PRD.md`
- **ForgeBase Guide**: `/docs/guides/forgebase_guide.md`

## Related ADRs

- [ADR-002: Hexagonal Ports & Adapters](002-hexagonal-ports-adapters.md) — Complementa com padrão Ports/Adapters
- [ADR-005: Dependency Injection](005-dependency-injection.md) — Implementação de DI respeitando Clean Architecture

---

**Author:** ForgeBase Development Team
**Date:** 2025-11-03
**Version:** 1.0
