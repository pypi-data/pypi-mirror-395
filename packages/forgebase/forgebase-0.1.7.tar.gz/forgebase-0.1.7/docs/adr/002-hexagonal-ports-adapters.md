# ADR-002: Hexagonal Architecture (Ports & Adapters)

## Status

**Aceita** (2025-11-03)

## Context

Complementando a Clean Architecture ([ADR-001](001-clean-architecture-choice.md)), precisávamos de um padrão claro para definir **como** a aplicação se comunica com o mundo externo:

- Bancos de dados (persistência)
- APIs externas (HTTP, gRPC)
- Interfaces de usuário (CLI, Web)
- Sistemas de mensageria
- LLMs e serviços de IA

O desafio era criar um padrão que:
- Isolasse a lógica de aplicação de detalhes de implementação
- Permitisse trocar implementações sem modificar o core
- Facilitasse testes com mocks/fakes
- Mantivesse o domínio "puro" e independente
- Tornasse explícitos os pontos de integração

### Forças em Jogo

**Necessidades:**
- Múltiplos adapters para o mesmo port (ex: JSON, SQL, MongoDB para persistência)
- Testes sem dependências reais (fakes, mocks)
- Evolução independente de adapters
- Clareza sobre boundaries de integração

**Riscos:**
- Proliferação de interfaces desnecessárias
- Overhead de criar ports para tudo
- Confusão entre driving e driven ports

## Decision

**Adotamos Hexagonal Architecture (Ports & Adapters) como padrão de integração.**

### Conceitos Fundamentais

#### 1. Ports (Interfaces/Contratos)

**Ports são contratos abstratos** definidos pela aplicação que especificam **o que** precisa ser feito, sem se preocupar com **como**.

**Tipos de Ports:**

**Driving Ports (Primary)** — "Quem usa a aplicação"
- Interfaces que disparam a aplicação (entrada)
- Exemplos: UseCases, Command Handlers
- Definidos pela application layer
- Implementados por adapters externos

**Driven Ports (Secondary)** — "O que a aplicação usa"
- Interfaces que a aplicação chama (saída)
- Exemplos: RepositoryPort, LoggerPort, NotificationPort
- Definidos pela application layer
- Implementados pela infrastructure layer

#### 2. Adapters (Implementações Concretas)

**Adapters são implementações específicas** dos ports, traduzindo entre o domínio e tecnologias externas.

**Driving Adapters (Primary):**
```python
# CLIAdapter: Interpreta comandos CLI → chama UseCases
# HTTPAdapter: Recebe requests HTTP → chama UseCases
# AIAdapter: Processa instruções LLM → chama UseCases
```

**Driven Adapters (Secondary):**
```python
# JSONRepository: Implementa RepositoryPort → salva em JSON
# SQLRepository: Implementa RepositoryPort → salva em SQL
# StdoutLogger: Implementa LoggerPort → loga no stdout
```

### Arquitetura Hexagonal do ForgeBase

```
                    ┌─────────────────┐
     CLI ────────► │                 │
                    │   UseCaseBase   │ ◄────── HTTP
     AI  ────────► │  (Driving Port) │
                    │                 │
                    └────────┬────────┘
                             │
                             │ calls
                             ▼
                    ┌─────────────────┐
                    │                 │
                    │  Domain Logic   │
                    │                 │
                    └────────┬────────┘
                             │
                             │ uses
                             ▼
        ┌───────────────────────────────────┐
        │      Driven Ports                 │
        │  (RepositoryPort, LoggerPort)     │
        └───────────┬───────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    [JSON]      [SQL]      [Stdout]
   Adapter     Adapter     Adapter
```

### Implementação no ForgeBase

#### Driving Ports (Primary)

```python
# src/forgebase/application/usecase_base.py
class UseCaseBase(ABC):
    """
    Driving Port — entrada para a aplicação.
    Adapters chamam execute() para disparar lógica.
    """
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass
```

**Adapters que implementam:**
- `CLIAdapter` — traduz comandos CLI → `execute()`
- `HTTPAdapter` — traduz HTTP requests → `execute()`

#### Driven Ports (Secondary)

```python
# src/forgebase/application/port_base.py
class PortBase(ABC):
    """Base para todos os driven ports."""
    @abstractmethod
    def info(self) -> dict:
        pass

# src/forgebase/infrastructure/repository/repository_base.py
class RepositoryBase(PortBase, Generic[T]):
    """
    Driven Port — persistência.
    UseCases dependem desta interface, não de implementações.
    """
    @abstractmethod
    def save(self, entity: T) -> None:
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[T]:
        pass

# src/forgebase/infrastructure/logging/logger_port.py
class LoggerPort(PortBase):
    """
    Driven Port — logging.
    UseCases logam através desta interface.
    """
    @abstractmethod
    def info(self, message: str, **context) -> None:
        pass
```

**Adapters que implementam:**
- `JSONRepository(RepositoryBase)` — salva em JSON
- `SQLRepository(RepositoryBase)` — salva em SQL
- `StdoutLogger(LoggerPort)` — loga no stdout
- `FileLogger(LoggerPort)` — loga em arquivo

### Regras de Implementação

1. **Ports são definidos pela Application**, não por Adapters
2. **Adapters nunca são importados diretamente por UseCases**
3. **Dependency Injection injeta adapters concretos** ([ADR-005](005-dependency-injection.md))
4. **Um UseCase depende de Ports, nunca de Adapters**
5. **Múltiplos Adapters podem implementar o mesmo Port**

### Exemplo Completo

```python
# Application Layer — Define o Port
class UserRepositoryPort(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

# Use Case — Depende do Port
class CreateUserUseCase(UseCaseBase):
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository  # Port, não adapter

    def execute(self, input_dto: CreateUserInput) -> CreateUserOutput:
        user = User(name=input_dto.name, email=input_dto.email)
        self.user_repository.save(user)  # Chama o port
        return CreateUserOutput(user_id=user.id)

# Infrastructure — Implementa o Port
class JSONUserRepository(UserRepositoryPort):
    def save(self, user: User) -> None:
        # Implementação específica JSON
        pass

class SQLUserRepository(UserRepositoryPort):
    def save(self, user: User) -> None:
        # Implementação específica SQL
        pass

# Adapter — Driving (CLI)
class CLIAdapter:
    def run_command(self, command: str):
        # Parse command
        usecase = CreateUserUseCase(
            user_repository=injected_repository  # DI injeta adapter
        )
        usecase.execute(input_dto)
```

## Consequences

### Positivas

✅ **Testabilidade Máxima**
```python
# Testes usam FakeRepository, não SQL real
def test_create_user():
    fake_repo = FakeRepository()
    usecase = CreateUserUseCase(user_repository=fake_repo)
    usecase.execute(CreateUserInput(name="Test"))
    assert fake_repo.count() == 1
```

✅ **Troca de Implementação Sem Mudança no Core**
```python
# Trocar de JSON para SQL — zero mudanças no UseCase
# config.yaml
repository: sql  # antes era "json"
```

✅ **Múltiplas Implementações do Mesmo Port**
```python
# Mesmo port, múltiplos adapters
- JSONRepository(RepositoryPort)
- SQLRepository(RepositoryPort)
- MongoRepository(RepositoryPort)
- InMemoryRepository(RepositoryPort)
```

✅ **Clareza sobre Boundaries**
- Fácil ver "o que entra" (driving ports)
- Fácil ver "o que sai" (driven ports)
- Boundaries explícitos no código

✅ **Evolução Independente**
- Adapter pode evoluir sem afetar aplicação
- Novo adapter não requer mudança no core
- Deprecar adapter sem breaking changes

### Negativas

⚠️ **Overhead de Abstrações**
- Um port para cada dependência externa
- Código de "plumbing" (DI, wiring)
- Mais arquivos para navegar

⚠️ **Confusão Inicial**
- Diferença entre port e adapter não é óbvia
- Tentação de "pular" o port e usar adapter diretamente
- Curva de aprendizado

⚠️ **Over-Engineering em Casos Simples**
- Para dependências estáveis (ex: Python stdlib), port pode ser overhead
- Nem tudo precisa de abstração

### Mitigações

1. **Convenção de Nomes Clara**
   - Ports: `*Port` (ex: `RepositoryPort`, `LoggerPort`)
   - Adapters: `*Adapter` (ex: `CLIAdapter`, `HTTPAdapter`)
   - Implementações: `*Repository`, `*Logger` (ex: `JSONRepository`)

2. **Documentação com Exemplos**
   - Complete flow example mostrando port + adapter
   - Cookbook com receitas comuns
   - ADRs explicando "porquê"

3. **Tooling**
   - Scaffold automático de port + adapter
   - Linting para validar boundaries
   - Code generators

4. **Regra de Pragmatismo**
   - "Se a dependência é estável e controlada por nós, port pode ser opcional"
   - "Se a dependência é externa ou pode mudar, port é obrigatório"

## Alternatives Considered

### 1. Acoplamento Direto (sem Ports)

```python
# UseCase importa adapter diretamente
from infrastructure.json_repository import JSONRepository

class CreateUserUseCase:
    def __init__(self):
        self.repo = JSONRepository()  # Acoplamento direto
```

**Rejeitado porque:**
- Impossível trocar implementação sem modificar UseCase
- Testes requerem JSON real (lento, frágil)
- Violação de Clean Architecture
- Domínio acoplado a infraestrutura

### 2. Service Locator Pattern

```python
# UseCase pede dependência a um locator global
class CreateUserUseCase:
    def execute(self, input_dto):
        repo = ServiceLocator.get('repository')  # Global
```

**Rejeitado porque:**
- Dependências ocultas (não explícitas na assinatura)
- Dificulta testes (estado global)
- Acoplamento implícito
- Dificulta rastreamento de dependências

### 3. Concrete Dependencies Everywhere

```python
# Cada UseCase cria suas próprias dependências
class CreateUserUseCase:
    def execute(self, input_dto):
        repo = JSONRepository(path="/data/users.json")  # Hardcoded
```

**Rejeitado porque:**
- Zero flexibilidade
- Testes impossíveis sem sistema de arquivos real
- Configuração hardcoded
- Violação de Single Responsibility

### 4. Ports apenas para "coisas grandes"

**Rejeitado porque:**
- Inconsistência arquitetural
- Linha tênue entre "grande" e "pequeno"
- Tende a degradar com o tempo
- Melhor ter regra clara: "toda dependência externa = port"

## References

- **Hexagonal Architecture** (Ports & Adapters) by Alistair Cockburn
- **Clean Architecture** by Robert C. Martin (Capítulo sobre boundaries)
- **Growing Object-Oriented Software, Guided by Tests** by Freeman & Pryce
- ForgeBase complete_flow.py — Exemplo prático de ports & adapters

## Related ADRs

- [ADR-001: Clean Architecture Choice](001-clean-architecture-choice.md)
- [ADR-005: Dependency Injection](005-dependency-injection.md)

---

**Author:** ForgeBase Development Team
**Date:** 2025-11-03
**Version:** 1.0
