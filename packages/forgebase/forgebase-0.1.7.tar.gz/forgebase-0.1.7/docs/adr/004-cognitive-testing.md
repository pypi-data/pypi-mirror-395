# ADR-004: Cognitive Testing

## Status

**Aceita** (2025-11-03)

## Context

ForgeBase não é apenas um framework técnico, é um framework **cognitivo** — código que pensa, mede e explica. Testes tradicionais validam **comportamento** ("o código faz o que deveria fazer?"), mas não validam **intenção** ("o código faz o que PRETENDÍAMOS que fizesse?").

### Limitações de Testes Tradicionais

**Testes Unitários Convencionais:**
```python
def test_create_user():
    user = create_user("Alice", "alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
```

**O que validam:**
- ✅ Sintaxe correta
- ✅ Tipo correto
- ✅ Valor esperado

**O que NÃO validam:**
- ❌ Intenção original foi cumprida?
- ❌ Coerência com especificação (YAML/ForgeProcess)?
- ❌ Instrumentação está funcionando?
- ❌ Side effects indesejados?
- ❌ Performance aceitável?

### Necessidades do ForgeBase

Como framework cognitivo, precisamos validar:

1. **Coerência Cognitiva**: Intent vs Execution
2. **Observabilidade**: Métricas estão sendo coletadas?
3. **Pureza**: Funções sem side effects indesejados?
4. **Performance**: Execução dentro de limites aceitáveis?
5. **Rastreabilidade**: Correlation IDs propagando?
6. **Feedback Loops**: Learning data sendo gerado?

### Forças em Jogo

**Necessidades:**
- Validar não apenas "funciona", mas "funciona como PRETENDIDO"
- Detectar drift entre especificação e implementação
- Garantir observabilidade está ativa
- Validar integração ForgeProcess ↔ ForgeBase

**Riscos:**
- Testes mais complexos de escrever
- Overhead de validação adicional
- Curva de aprendizado para novos desenvolvedores
- Potencial para over-testing

## Decision

**Adotamos "Cognitive Testing" como filosofia de teste: validar intenção, não apenas comportamento.**

### Conceito: ForgeTestCase

Criamos `ForgeTestCase`, uma extensão de `unittest.TestCase` com **assertions cognitivas**:

```python
class ForgeTestCase(unittest.TestCase):
    """
    Base class para testes cognitivos.

    Adiciona validações de:
    - Intenção vs execução
    - Métricas coletadas
    - Pureza funcional
    - Performance
    """

    def assert_intent_matches(self, expected: str, actual: str, threshold: float = 0.8)
    def assert_metrics_collected(self, metrics: dict)
    def assert_no_side_effects(self, fn: Callable)
    def assert_performance_within(self, fn: Callable, max_duration_ms: float)
```

### Assertions Cognitivas

#### 1. assert_intent_matches

**Propósito**: Validar que a execução real corresponde à intenção original.

```python
class TestCreateUser(ForgeTestCase):
    def test_creates_user_with_intent(self):
        # Captura intenção
        intent = "Create a new user with valid email address"

        # Execução
        result = usecase.execute(CreateUserInput(
            name="Alice",
            email="alice@example.com"
        ))

        # Validação cognitiva
        actual = f"Created user {result.user_id} with email {result.email}"

        self.assert_intent_matches(
            expected=intent,
            actual=actual,
            threshold=0.8  # 80% similarity mínima
        )
```

**Implementação:**
- Usa similarity analysis (difflib.SequenceMatcher)
- Threshold configurável
- Mensagem descritiva em caso de falha

#### 2. assert_metrics_collected

**Propósito**: Garantir que métricas estão sendo coletadas.

```python
class TestCreateUser(ForgeTestCase):
    def test_collects_metrics(self):
        fake_metrics = FakeMetricsCollector()
        usecase = CreateUserUseCase(
            user_repository=fake_repo,
            metrics_collector=fake_metrics
        )

        usecase.execute(input_dto)

        # Valida que métricas esperadas foram coletadas
        self.assert_metrics_collected({
            'create_user.duration': lambda v: v > 0,
            'create_user.count': lambda v: v == 1,
            'create_user.success': lambda v: v == True
        })
```

**Implementação:**
- Verifica presença de métricas
- Valida valores com predicates
- Falha descritiva mostrando métricas ausentes

#### 3. assert_no_side_effects

**Propósito**: Validar pureza funcional (ausência de side effects).

```python
class TestEmailValueObject(ForgeTestCase):
    def test_validation_has_no_side_effects(self):
        email = Email("alice@example.com")

        # Validar que múltiplas chamadas não mudam estado
        self.assert_no_side_effects(
            lambda: email.validate()
        )

        # Email deve ser imutável após criação
        with self.assertRaises(AttributeError):
            email.address = "bob@example.com"
```

**Implementação:**
- Executa função múltiplas vezes
- Verifica estado antes e depois
- Detecta mutações indesejadas

#### 4. assert_performance_within

**Propósito**: Garantir performance aceitável.

```python
class TestCreateUser(ForgeTestCase):
    def test_executes_within_acceptable_time(self):
        # Deve executar em menos de 50ms
        self.assert_performance_within(
            lambda: usecase.execute(input_dto),
            max_duration_ms=50.0
        )
```

**Implementação:**
- Mede tempo de execução
- Falha se exceder threshold
- Mostra duração real vs esperada

### Estrutura de um Teste Cognitivo

```python
class TestCreateUserUseCase(ForgeTestCase):
    def setUp(self):
        """Setup com fakes e contexto."""
        self.fake_repo = FakeRepository()
        self.fake_metrics = FakeMetricsCollector()
        self.fake_logger = FakeLogger()

        self.usecase = CreateUserUseCase(
            user_repository=self.fake_repo,
            metrics_collector=self.fake_metrics,
            logger=self.fake_logger
        )

    def test_creates_user_cognitive_validation(self):
        """
        Teste cognitivo completo:
        - Valida comportamento
        - Valida intenção
        - Valida métricas
        - Valida performance
        """
        # 1. Captura intenção
        intent = "Create user with name Alice and email alice@example.com"

        # 2. Execução
        result = self.usecase.execute(CreateUserInput(
            name="Alice",
            email="alice@example.com"
        ))

        # 3. Validações tradicionais
        self.assertEqual(result.name, "Alice")
        self.assertEqual(result.email, "alice@example.com")
        self.assertTrue(result.user_id)

        # 4. Validações cognitivas

        # 4a. Coerência de intenção
        self.assert_intent_matches(
            expected=intent,
            actual=f"Created user {result.name} with email {result.email}"
        )

        # 4b. Métricas coletadas
        self.assert_metrics_collected({
            'create_user.duration': lambda v: v > 0,
            'create_user.count': lambda v: v == 1
        })

        # 4c. Logs estruturados
        logs = self.fake_logger.get_logs(level='info')
        self.assertTrue(any('user_created' in log['message'] for log in logs))
        self.assertTrue(any('user_id' in log['context'] for log in logs))

        # 4d. Performance
        self.assert_performance_within(
            lambda: self.usecase.execute(input_dto),
            max_duration_ms=100.0
        )

        # 4e. Side effects (repository state)
        self.assertEqual(self.fake_repo.count(), 1)
        self.assertTrue(self.fake_repo.exists(result.user_id))
```

### Test Doubles Cognitivos

ForgeBase fornece fakes especializados para testes cognitivos:

#### FakeLogger
```python
class FakeLogger(LoggerPort):
    """Logger in-memory para testes."""

    def get_logs(self, level: str = None) -> List[dict]:
        """Retorna logs coletados."""

    def assert_logged(self, message: str, level: str = 'info'):
        """Assert que mensagem foi logada."""

    def assert_context_present(self, **context):
        """Assert que contexto está presente em algum log."""
```

#### FakeMetricsCollector
```python
class FakeMetricsCollector:
    """Coletor de métricas in-memory."""

    def get_metric(self, name: str) -> Optional[Metric]:
        """Retorna métrica coletada."""

    def assert_metric_collected(self, name: str, predicate: Callable):
        """Assert sobre valor de métrica."""

    def get_all_metrics(self) -> dict:
        """Retorna todas métricas coletadas."""
```

#### FakeRepository
```python
class FakeRepository(RepositoryBase[T]):
    """Repository in-memory para testes."""

    def count(self) -> int:
        """Quantidade de entidades."""

    def contains(self, id: str) -> bool:
        """Se contém entidade."""

    def get_all(self) -> List[T]:
        """Todas entidades."""
```

### Testes de Coerência YAML ↔ Code

Para validar sincronização ForgeProcess:

```python
class TestYAMLCodeCoherence(ForgeTestCase):
    def test_usecase_matches_yaml_spec(self):
        """Valida que código implementa spec YAML."""
        # Carrega spec YAML
        sync = YAMLSync()
        spec = sync.parse_yaml("specs/create_user.yaml")

        # Detecta drift
        drift = sync.detect_drift(CreateUserUseCase, spec)

        # Deve ter zero drift
        self.assertEqual(len(drift), 0,
            f"Drift detected between YAML and code: {drift}")

    def test_generated_code_matches_manual_implementation(self):
        """Valida que código gerado seria idêntico ao manual."""
        spec = sync.parse_yaml("specs/create_user.yaml")
        generated = sync.generate_code(spec)

        # Parse ambos e compare AST
        # (implementação simplificada)
        self.assertCodeStructureMatches(generated, CreateUserUseCase)
```

### Testes de Intent Tracking

```python
class TestIntentTracking(ForgeTestCase):
    def test_tracks_intent_coherence(self):
        """Valida tracking de coerência cognitiva."""
        tracker = IntentTracker()

        # Captura intenção
        intent_id = tracker.capture_intent(
            description="Create user",
            expected_outcome="User created successfully"
        )

        # Executa
        result = usecase.execute(input_dto)

        # Registra execução
        tracker.record_execution(
            intent_id=intent_id,
            actual_outcome=result.message,
            success=True
        )

        # Valida coerência
        report = tracker.validate_coherence(intent_id)

        # Assertções cognitivas
        self.assertIn(report.coherence_level, [
            CoherenceLevel.PERFECT,
            CoherenceLevel.HIGH
        ])
        self.assertGreaterEqual(report.similarity_score, 0.8)
        self.assertEqual(len(report.divergences), 0)
```

## Consequences

### Positivas

✅ **Validação Holística**
- Não apenas "funciona", mas "funciona como pretendido"
- Detecta drift entre intenção e implementação
- Garante observabilidade está ativa

✅ **Debugging Melhorado**
```python
# Quando teste falha, temos contexto rico:
AssertionError: Intent match failed
Expected: "Create user with email alice@example.com"
Actual: "User created with ID 123"
Similarity: 0.42 (below threshold 0.80)
Recommendation: Include email in success message for better coherence
```

✅ **Documentação Viva**
- Testes documentam intenção
- ForgeTestCase mostra padrões de uso
- Assertions explicam contratos cognitivos

✅ **Regressão Cognitiva**
- Detecta quando código "funciona mas não como antes"
- Previne degradação de coerência ao longo do tempo
- Mantém alinhamento com ForgeProcess

✅ **Confiança em Refatorings**
- Refatorar sem medo de quebrar coerência
- Validação automática de intenção
- Safety net cognitivo

### Negativas

⚠️ **Complexidade Adicional**
- Testes mais verbosos
- Curva de aprendizado
- Mais código de teste

⚠️ **Overhead de Manutenção**
- Atualizar testes quando intenção muda
- Manter thresholds calibrados
- Revisar assertions cognitivas

⚠️ **Potencial para Flakiness**
- Similarity thresholds podem ser sensíveis
- Performance tests podem falhar em CI lento
- Context-dependent validations

### Mitigações

1. **Tooling**
   - Generators de testes cognitivos
   - Templates para casos comuns
   - Linters para validar padrões

2. **Defaults Sensatos**
   - Thresholds calibrados por uso real
   - Timeouts ajustados para CI
   - Fakes otimizados

3. **Documentação**
   - Cookbook de testes cognitivos
   - Exemplos para cada padrão
   - ADR explicando filosofia

4. **Pragmatismo**
   - Nem todo teste precisa ser cognitivo
   - Cognitive tests para UseCases críticos
   - Unit tests tradicionais para utilities

## Alternatives Considered

### 1. Testes Tradicionais Apenas

**Rejeitado porque:**
- Não valida intenção
- Não detecta drift
- Não verifica observabilidade
- Miss oportunidade de validar coerência

### 2. Property-Based Testing (Hypothesis)

```python
@given(st.text(), st.emails())
def test_create_user(name, email):
    user = create_user(name, email)
    assert user.name == name
```

**Não rejeitado, mas complementar:**
- Property-based tests são úteis para edge cases
- Cognitive tests validam intenção específica
- Ambos podem coexistir

### 3. Snapshot Testing

```python
def test_create_user():
    result = usecase.execute(input_dto)
    assert_snapshot_matches(result, "create_user_snapshot.json")
```

**Não rejeitado, mas limitado:**
- Snapshots validam estrutura, não intenção
- Útil para regressão de formato
- Cognitive tests validam semântica

### 4. Contract Testing (Pact)

**Não rejeitado, mas diferente escopo:**
- Pact valida contratos entre serviços
- Cognitive tests validam intenção dentro de um serviço
- Complementares, não excludentes

## Implementation Guidelines

### Quando Usar Cognitive Tests

**Use para:**
- ✅ UseCases críticos de negócio
- ✅ Código que muda frequentemente
- ✅ Integração ForgeProcess ↔ ForgeBase
- ✅ Validação de observabilidade
- ✅ Performance-critical paths

**Não use para:**
- ❌ Utilities simples (use unit tests tradicionais)
- ❌ Third-party libraries
- ❌ One-off scripts
- ❌ Código puramente técnico sem intent

### Estrutura Recomendada

```
tests/
├── unit/                       # Testes unitários tradicionais
│   ├── test_entity_base.py
│   └── test_value_object.py
├── integration/                # Testes de integração
│   └── test_repository_sql.py
└── cognitive/                  # Testes cognitivos
    ├── test_create_user_cognitive.py
    ├── test_yaml_sync_coherence.py
    └── test_intent_tracking.py
```

## References

- **Growing Object-Oriented Software, Guided by Tests** by Freeman & Pryce
- **Test-Driven Development** by Kent Beck
- **Property-Based Testing** by David MacIver
- ForgeBase testing examples: `tests/unit/testing/`

## Related ADRs

- [ADR-003: Observability First](003-observability-first.md)
- [ADR-006: ForgeProcess Integration](006-forgeprocess-integration.md)

---

**Author:** ForgeBase Development Team
**Date:** 2025-11-03
**Version:** 1.0
