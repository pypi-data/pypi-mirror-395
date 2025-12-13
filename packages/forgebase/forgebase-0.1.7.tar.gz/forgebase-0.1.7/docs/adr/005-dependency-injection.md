# ADR-005: Dependency Injection

## Status

**Aceita** (2025-11-03)

## Context

ForgeBase adota Clean Architecture ([ADR-001](001-clean-architecture-choice.md)) e Hexagonal Architecture ([ADR-002](002-hexagonal-ports-adapters.md)), o que significa que:

- **UseCases dependem de Ports, não de Adapters concretos**
- **Domain deve ser completamente independente de infraestrutura**
- **Adapters podem ser trocados sem modificar o core**

Para isso funcionar, precisamos de um mecanismo para **injetar dependências** em tempo de execução. O desafio é escolher como fazer isso de forma que:

- Mantenha a arquitetura limpa
- Seja testável
- Seja configurável
- Não adicione complexidade desnecessária
- Seja explícito (não mágico)

### Problema

```python
# ❌ Problema: UseCase cria suas próprias dependências
class CreateUserUseCase:
    def __init__(self):
        # Acoplamento direto
        self.repository = JSONRepository("/data/users.json")
        self.logger = StdoutLogger()

    def execute(self, input_dto):
        # Impossível testar sem filesystem real
        # Impossível trocar implementação
        ...
```

### Necessidades

1. **Inversão de Dependência**: UseCases dependem de abstrações (Ports)
2. **Configurabilidade**: Escolher implementações via config
3. **Testabilidade**: Injetar fakes em testes
4. **Explicitness**: Dependências visíveis na assinatura
5. **Lifecycle Management**: Criar/destruir dependências corretamente

### Forças em Jogo

**Necessidades:**
- Desacoplamento total entre layers
- Testes rápidos com fakes
- Flexibilidade de configuração
- Reutilização de componentes

**Riscos:**
- Complexidade de setup
- "Magic" que dificulta debugging
- Overhead de frameworks DI
- Curva de aprendizado

## Decision

**Adotamos Dependency Injection Manual (Constructor Injection) com DI Container Opcional.**

### Princípio: Constructor Injection

**Todas as dependências são injetadas via construtor:**

```python
# ✅ Solução: Dependências injetadas
class CreateUserUseCase(UseCaseBase):
    def __init__(
        self,
        user_repository: UserRepositoryPort,  # Port, não adapter
        logger: LoggerPort,
        metrics: TrackMetrics
    ):
        self.user_repository = user_repository
        self.logger = logger
        self.metrics = metrics

    def execute(self, input_dto: CreateUserInput) -> CreateUserOutput:
        # Usa dependências injetadas
        self.logger.info("Creating user", email=input_dto.email)
        ...
```

**Benefícios:**
- ✅ **Explícito**: Dependências visíveis na assinatura
- ✅ **Testável**: Fácil injetar fakes
- ✅ **Type-safe**: Type hints claros
- ✅ **Zero magic**: Sem decorators ou metaclasses
- ✅ **IDE-friendly**: Autocomplete funciona

### Padrão de Injeção

#### 1. UseCases (Application Layer)

```python
class CreateUserUseCase(UseCaseBase):
    def __init__(
        self,
        user_repository: UserRepositoryPort,  # Required
        logger: Optional[LoggerPort] = None,  # Optional com default
        metrics: Optional[TrackMetrics] = None
    ):
        self.user_repository = user_repository
        self.logger = logger or NoOpLogger()
        self.metrics = metrics or NoOpMetrics()
```

**Convenções:**
- Dependências **obrigatórias** sem default
- Dependências **opcionais** com default NoOp
- Type hints sempre presentes
- Nomes descritivos (não genéricos como `repo`)

#### 2. Adapters

```python
class JSONUserRepository(UserRepositoryPort):
    def __init__(
        self,
        file_path: str,
        logger: Optional[LoggerPort] = None
    ):
        self.file_path = file_path
        self.logger = logger or NoOpLogger()
```

#### 3. Infrastructure

```python
class SQLRepository(RepositoryBase[T]):
    def __init__(
        self,
        connection_string: str,
        entity_type: Type[T],
        logger: Optional[LoggerPort] = None
    ):
        self.connection_string = connection_string
        self.entity_type = entity_type
        self.logger = logger or NoOpLogger()
```

### DI Container (Opcional)

Para aplicações complexas, fornecemos um **DI Container simples**:

```python
# src/forgebase/infrastructure/di_container.py
class DIContainer:
    """
    Simple dependency injection container.

    Registers factories and resolves dependencies automatically.
    """

    def __init__(self):
        self._factories = {}
        self._singletons = {}

    def register(
        self,
        interface: Type,
        factory: Callable,
        singleton: bool = False
    ):
        """Register a factory for an interface."""
        self._factories[interface] = (factory, singleton)

    def resolve(self, interface: Type) -> Any:
        """Resolve an instance of an interface."""
        if interface in self._singletons:
            return self._singletons[interface]

        if interface not in self._factories:
            raise ValueError(f"No factory registered for {interface}")

        factory, singleton = self._factories[interface]
        instance = factory(self)

        if singleton:
            self._singletons[interface] = instance

        return instance
```

**Uso:**

```python
# Setup (application startup)
container = DIContainer()

# Register adapters
container.register(
    LoggerPort,
    lambda c: StdoutLogger(),
    singleton=True
)

container.register(
    UserRepositoryPort,
    lambda c: JSONUserRepository(
        file_path="/data/users.json",
        logger=c.resolve(LoggerPort)
    ),
    singleton=True
)

container.register(
    TrackMetrics,
    lambda c: PrometheusMetrics(endpoint="http://localhost:9090"),
    singleton=True
)

# Register UseCases
container.register(
    CreateUserUseCase,
    lambda c: CreateUserUseCase(
        user_repository=c.resolve(UserRepositoryPort),
        logger=c.resolve(LoggerPort),
        metrics=c.resolve(TrackMetrics)
    )
)

# Resolve UseCase (automatically resolves dependencies)
usecase = container.resolve(CreateUserUseCase)
result = usecase.execute(input_dto)
```

### Configuration-Based DI

Integração com ConfigLoader:

```yaml
# config.yaml
dependencies:
  logger:
    type: stdout
    level: info

  repository:
    type: json
    path: /data/users.json

  metrics:
    type: prometheus
    endpoint: http://localhost:9090

usecases:
  create_user:
    repository: user_repository
    logger: logger
    metrics: metrics
```

```python
# Loader de config para DI
class DIConfigLoader:
    def load_from_config(self, config_path: str) -> DIContainer:
        config = load_yaml(config_path)
        container = DIContainer()

        # Register dependencies from config
        for name, dep_config in config['dependencies'].items():
            factory = self._create_factory(dep_config)
            interface = self._get_interface(name)
            container.register(interface, factory, singleton=True)

        return container
```

### Testing with DI

```python
class TestCreateUserUseCase(unittest.TestCase):
    def setUp(self):
        # Manual injection com fakes (sem DI container)
        self.fake_repo = FakeRepository()
        self.fake_logger = FakeLogger()
        self.fake_metrics = FakeMetricsCollector()

        self.usecase = CreateUserUseCase(
            user_repository=self.fake_repo,
            logger=self.fake_logger,
            metrics=self.fake_metrics
        )

    def test_creates_user(self):
        result = self.usecase.execute(CreateUserInput(...))

        # Validações
        self.assertEqual(self.fake_repo.count(), 1)
        self.assertTrue(self.fake_logger.was_called('info'))
        self.assertTrue(self.fake_metrics.has_metric('create_user.count'))
```

**Sem DI container em testes:**
- Setup mais simples
- Controle total
- Sem surpresas

### Lifecycle Management

```python
class DIContainer:
    def __enter__(self):
        """Context manager para lifecycle."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup de singletons."""
        for instance in self._singletons.values():
            if hasattr(instance, 'close'):
                instance.close()

# Uso
with DIContainer() as container:
    # Register & resolve
    usecase = container.resolve(CreateUserUseCase)
    usecase.execute(input_dto)
    # Automatic cleanup on exit
```

### core_init.py Integration

```python
# src/forgebase/core_init.py
class ForgeBaseCore:
    def __init__(self, config_path: Optional[str] = None):
        self.config = ConfigLoader.load(config_path)
        self.container = DIContainer()
        self._setup_dependencies()

    def _setup_dependencies(self):
        """Setup DI container from config."""
        # Logger
        logger_config = self.config.get('logger', {})
        self.container.register(
            LoggerPort,
            lambda c: self._create_logger(logger_config),
            singleton=True
        )

        # Metrics
        metrics_config = self.config.get('metrics', {})
        self.container.register(
            TrackMetrics,
            lambda c: self._create_metrics(metrics_config),
            singleton=True
        )

        # Repository
        repo_config = self.config.get('repository', {})
        self.container.register(
            UserRepositoryPort,
            lambda c: self._create_repository(repo_config),
            singleton=True
        )

        # UseCases
        self._register_usecases()

    def get_usecase(self, usecase_class: Type[UseCaseBase]) -> UseCaseBase:
        """Get UseCase with dependencies injected."""
        return self.container.resolve(usecase_class)
```

## Consequences

### Positivas

✅ **Testabilidade Máxima**
```python
# Injetar fakes é trivial
usecase = CreateUserUseCase(
    user_repository=FakeRepository(),
    logger=FakeLogger()
)
```

✅ **Flexibilidade de Configuração**
```yaml
# Trocar implementações sem código
repository:
  type: sql  # antes era "json"
```

✅ **Explicitness**
```python
# Dependências visíveis na assinatura
def __init__(self, user_repository: UserRepositoryPort, logger: LoggerPort):
    ...
```

✅ **Type Safety**
- Type hints garantem contratos
- IDE autocomplete funciona
- Mypy detecta erros

✅ **Zero Magic**
- Sem decorators @inject
- Sem metaclasses
- Debugging simples

✅ **Reusabilidade**
```python
# Mesmo UseCase, múltiplos contextos
prod_usecase = CreateUserUseCase(sql_repo, prod_logger)
test_usecase = CreateUserUseCase(fake_repo, fake_logger)
```

### Negativas

⚠️ **Boilerplate de Wiring**
```python
# Precisa wirear manualmente
usecase = CreateUserUseCase(
    user_repository=container.resolve(UserRepositoryPort),
    logger=container.resolve(LoggerPort),
    metrics=container.resolve(TrackMetrics)
)
```

**Mitigation**: DI Container automatiza wiring

⚠️ **Setup Inicial Verboso**
- Muitos `container.register()` calls
- Config YAML pode ficar extensa

**Mitigation**: Defaults sensatos, auto-discovery

⚠️ **Constructor Bloat**
```python
# Muitas dependências = construtor grande
def __init__(self, dep1, dep2, dep3, dep4, dep5):
    ...
```

**Mitigation**: Se >5 dependências, refatorar UseCase

### Mitigações Implementadas

1. **Defaults NoOp**
   ```python
   def __init__(self, logger: Optional[LoggerPort] = None):
       self.logger = logger or NoOpLogger()
   ```

2. **Container Simplificado**
   - Não é framework complexo (Guice, Spring)
   - ~200 LOC total
   - Fácil entender e debugar

3. **Config-Driven**
   - YAML define wiring
   - Código apenas implementa
   - Switching sem rebuild

4. **Generators**
   ```bash
   forgebase generate usecase CreateUser --with-di
   # Gera UseCase com DI correto
   ```

## Alternatives Considered

### 1. Service Locator

```python
class CreateUserUseCase:
    def execute(self, input_dto):
        repo = ServiceLocator.get(UserRepositoryPort)
        logger = ServiceLocator.get(LoggerPort)
        ...
```

**Rejeitado porque:**
- Dependências ocultas
- Dificulta testes
- Estado global
- Não type-safe

### 2. Frameworks DI Pesados (Injector, Dependency-Injector)

**Rejeitado porque:**
- Overhead desnecessário
- Magic demais (decorators, metaclasses)
- Curva de aprendizado
- ForgeBase quer ser simples

### 3. Function-based DI

```python
def create_user(
    input_dto: CreateUserInput,
    repository: UserRepositoryPort = Depends(get_repository)
):
    ...
```

**Rejeitado porque:**
- Específico de frameworks web (FastAPI)
- Não se aplica bem a UseCases
- Mistura concerns

### 4. Property Injection

```python
class CreateUserUseCase:
    @inject
    def set_repository(self, repo: UserRepositoryPort):
        self.repository = repo
```

**Rejeitado porque:**
- Menos explícito que constructor
- Permite objeto em estado inválido
- Mais verboso

### 5. Monkey Patching para Testes

```python
# Em testes
CreateUserUseCase.repository = FakeRepository()
```

**Rejeitado porque:**
- Estado global
- Race conditions
- Não isolado entre testes
- Horrível

## Implementation Guidelines

### Para Desenvolvedores de UseCases

**Sempre use constructor injection:**
```python
class MyUseCase(UseCaseBase):
    def __init__(
        self,
        required_port: SomePort,
        optional_port: Optional[OtherPort] = None
    ):
        self.required_port = required_port
        self.optional_port = optional_port or NoOpPort()
```

**Regras:**
1. Dependências obrigatórias primeiro
2. Dependências opcionais com defaults
3. Type hints sempre
4. Nomes descritivos

### Para Integração

**Use DI Container para apps:**
```python
# main.py
container = DIContainer()
# ... register dependencies ...
usecase = container.resolve(CreateUserUseCase)
```

**Use manual injection para testes:**
```python
# test_*.py
usecase = CreateUserUseCase(
    repository=FakeRepository(),
    logger=FakeLogger()
)
```

## References

- **Dependency Injection Principles, Practices, and Patterns** by Steven van Deursen & Mark Seemann
- **Clean Architecture** by Robert C. Martin (Capítulo sobre DI)
- **Inversion of Control Containers and the Dependency Injection pattern** by Martin Fowler

## Related ADRs

- [ADR-001: Clean Architecture Choice](001-clean-architecture-choice.md)
- [ADR-002: Hexagonal Ports & Adapters](002-hexagonal-ports-adapters.md)

---

**Author:** ForgeBase Development Team
**Date:** 2025-11-03
**Version:** 1.0
