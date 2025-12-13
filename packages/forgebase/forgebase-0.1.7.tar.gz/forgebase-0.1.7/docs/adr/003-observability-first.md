# ADR-003: Observability First

## Status

**Aceita** (2025-11-03)

## Context

ForgeBase foi projetado para ser um framework **cognitivo** — não apenas executa código, mas **entende, mede e explica** seu próprio comportamento. Para isso, observabilidade não pode ser um "add-on" posterior, mas sim uma **característica nativa** da arquitetura.

### Desafios de Sistemas Tradicionais

Em sistemas tradicionais, observabilidade é frequentemente:
- **Adicionada depois**: "Vamos adicionar logs quando der problema"
- **Inconsistente**: Alguns módulos logam, outros não
- **Superficial**: Logs sem contexto, métricas sem significado
- **Cara**: Overhead de instrumentação manual
- **Fragmentada**: Logs aqui, métricas ali, traces em outro lugar

### Necessidades do ForgeBase

Como framework cognitivo, ForgeBase precisa:

1. **Auto-Reflexão**: Capacidade de introspectar seu próprio comportamento
2. **Rastreabilidade**: Entender a jornada de cada execução
3. **Medição Contínua**: Métricas de performance, sucesso, coerência
4. **Debugging Cognitivo**: Não apenas "onde falhou", mas "por que falhou"
5. **Feedback Loops**: Dados para aprendizado contínuo
6. **Transparência**: Explicar decisões e execuções

### Forças em Jogo

**Necessidades:**
- Debugging eficiente em produção
- Monitoramento de performance
- Validação de coerência cognitiva (intent vs execution)
- Feedback para ForgeProcess
- Auditoria de decisões

**Riscos:**
- Overhead de performance
- Custo de storage (logs, métricas)
- Complexidade de configuração
- Excesso de informação (signal vs noise)

## Decision

**Adotamos "Observability First" como princípio fundamental: observabilidade é nativa, não opcional.**

### Pilares de Observabilidade

#### 1. Logging Estruturado (LogService)

**Decisão**: Todos os logs são estruturados (JSON), não strings.

```python
# ❌ Tradicional (não estruturado)
logger.info("User created: Alice")

# ✅ ForgeBase (estruturado)
logger.info(
    "User created",
    user_id="123",
    user_name="Alice",
    email="alice@example.com",
    duration_ms=42.5,
    correlation_id="abc-def"
)
```

**Benefícios:**
- Queryable: Buscar por `user_id=123` facilmente
- Context propagation automático
- Correlation IDs rastreiam requests
- Machine-readable para análise

**Implementação**:
- `src/forgebase/observability/log_service.py` (~489 LOC)
- Handlers: stdout, file, remote (Elasticsearch, CloudWatch)
- Níveis: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Sampling para high-volume scenarios

#### 2. Métricas Ativas (TrackMetrics)

**Decisão**: UseCases e Ports são automaticamente instrumentados.

**Tipos de Métricas:**

```python
# Counters: Contagem de eventos
track_metrics.increment("usecase.execution.count", usecase="CreateUser")
track_metrics.increment("usecase.execution.errors", usecase="CreateUser")

# Gauges: Valores instantâneos
track_metrics.gauge("system.memory.usage", value=512.5, unit="MB")

# Histograms: Distribuições de valores
track_metrics.histogram("usecase.execution.duration", value=42.5, usecase="CreateUser")
```

**Métricas Padrão (Auto-coletadas):**
- `usecase.execution.duration` — Tempo de execução
- `usecase.execution.count` — Quantidade de execuções
- `usecase.execution.errors` — Quantidade de erros
- `usecase.execution.success_rate` — Taxa de sucesso
- `port.call.duration` — Tempo de chamadas a ports
- `adapter.request.count` — Requests por adapter

**Implementação**:
- `src/forgebase/observability/track_metrics.py` (~447 LOC)
- Export formats: Prometheus, JSON, StatsD
- Aggregation em memória
- Overhead < 1ms per metric

#### 3. Distributed Tracing (TracerPort)

**Decisão**: Suporte nativo para distributed tracing (OpenTelemetry-compatible).

**Conceito**: Cada execução cria uma **trace** com múltiplos **spans**:

```
Trace: CreateUser (correlation_id: abc-123)
├─ Span: usecase.execute [42ms]
│  ├─ Span: domain.validate [2ms]
│  ├─ Span: repository.save [35ms]
│  └─ Span: logger.info [1ms]
└─ Span: adapter.respond [3ms]
```

**Implementação**:
- `src/forgebase/observability/tracer_port.py` (~504 LOC)
- OpenTelemetry-compatible interface
- Context propagation automática
- Adapters: Jaeger, Zipkin, DataDog

#### 4. Cognitive Coherence (FeedbackManager + IntentTracker)

**Decisão**: Rastrear coerência entre intenção e execução.

**Fluxo:**
1. **Capture Intent** (antes da execução)
   ```python
   intent_id = tracker.capture_intent(
       description="Create user with valid email",
       expected_outcome="User created successfully"
   )
   ```

2. **Execute**
   ```python
   result = usecase.execute(input_dto)
   ```

3. **Record Execution** (após execução)
   ```python
   tracker.record_execution(
       intent_id=intent_id,
       actual_outcome=result.message,
       success=True,
       duration_ms=42.5
   )
   ```

4. **Validate Coherence**
   ```python
   report = tracker.validate_coherence(intent_id)
   # report.coherence_level: PERFECT, HIGH, MEDIUM, LOW, DIVERGENT
   # report.similarity_score: 0.0 - 1.0
   # report.recommendations: ["Improve error message clarity"]
   ```

**Implementação**:
- `src/forgebase/observability/feedback_manager.py` (~455 LOC)
- `src/forgebase/integration/intent_tracker.py` (~450 LOC)
- Similarity analysis usando difflib
- Learning data export para ML

### Instrumentação Automática

#### Decorator @track_metrics

**Decisão**: UseCases podem ser instrumentados com um decorator.

```python
from forgebase.application.decorators import track_metrics

class CreateUserUseCase(UseCaseBase):
    @track_metrics(
        metric_name="create_user",
        track_duration=True,
        track_errors=True
    )
    def execute(self, input_dto: CreateUserInput) -> CreateUserOutput:
        # Métricas coletadas automaticamente:
        # - create_user.duration
        # - create_user.count
        # - create_user.errors (se exception)
        ...
```

**Implementação**:
- `src/forgebase/application/decorators/track_metrics.py` (~283 LOC)
- Zero overhead quando desabilitado
- Async-compatible
- Context propagation

### Níveis de Observabilidade

ForgeBase suporta 3 níveis configuráveis:

**1. MINIMAL (Produção)**
- Logs: ERROR, CRITICAL
- Métricas: Aggregated (1min resolution)
- Traces: Sampling 1% (para performance)

**2. STANDARD (Staging)**
- Logs: INFO, WARNING, ERROR, CRITICAL
- Métricas: All
- Traces: Sampling 10%

**3. DEBUG (Desenvolvimento)**
- Logs: ALL (DEBUG included)
- Métricas: All (real-time)
- Traces: 100% (todas requests)

### Configuration

```yaml
# config.yaml
observability:
  level: standard  # minimal | standard | debug

  logging:
    handlers:
      - stdout
      - file: /var/log/forgebase.log
    format: json
    correlation_id: true

  metrics:
    enabled: true
    export:
      - prometheus: http://localhost:9090
      - json: /var/metrics/forgebase.json
    collection_interval: 60  # seconds

  tracing:
    enabled: true
    provider: jaeger
    endpoint: http://localhost:14268
    sampling_rate: 0.1  # 10%

  cognitive:
    intent_tracking: true
    coherence_validation: true
    learning_export: /var/learning/data.jsonl
```

## Consequences

### Positivas

✅ **Debugging Eficiente**
```python
# Encontrar execução específica por correlation_id
logs = log_service.query(correlation_id="abc-123")

# Ver timeline completa de uma execução
trace = tracer.get_trace("abc-123")

# Analisar coerência de uma operação
report = intent_tracker.validate_coherence(intent_id)
```

✅ **Visibilidade Completa**
- Saber exatamente o que está acontecendo em produção
- Detectar degradação de performance antes de virar problema
- Entender padrões de uso

✅ **Feedback Loop Cognitivo**
- Dados de coerência alimentam ForgeProcess
- Aprendizado contínuo sobre qualidade de execução
- Melhoria iterativa baseada em dados reais

✅ **Auditoria & Compliance**
- Trail completo de operações
- Rastreabilidade de decisões
- Conformidade com regulações

✅ **Performance Tuning**
- Identificar bottlenecks facilmente
- Comparar performance de diferentes implementações
- A/B testing de otimizações

### Negativas

⚠️ **Overhead de Performance**
- Logging: ~0.1-0.5ms por log
- Métricas: ~0.1ms por metric
- Tracing: ~1-5ms por span
- **Mitigation**: Sampling, async logging, níveis configuráveis

⚠️ **Storage Costs**
- Logs podem crescer rapidamente
- Métricas históricas requerem espaço
- Traces podem ser volumosos
- **Mitigation**: Retention policies, compression, aggregation

⚠️ **Complexidade Operacional**
- Infraestrutura de observabilidade (Elasticsearch, Prometheus, Jaeger)
- Dashboards e alerting
- Conhecimento técnico necessário
- **Mitigation**: Defaults sensatos, self-hosted options, docs claras

⚠️ **Signal vs Noise**
- Excesso de logs pode dificultar debugging
- Métricas demais podem confundir
- Traces detalhados podem ser overwhelming
- **Mitigation**: Níveis configuráveis, sampling inteligente, filtering

### Mitigações Implementadas

1. **Performance**
   - Logging assíncrono (não bloqueia execução)
   - Metrics aggregation em memória
   - Sampling configurável para traces
   - Lazy evaluation de contexto

2. **Storage**
   - Retention policies configuráveis
   - Log rotation automático
   - Metrics downsampling (ex: 1min → 1hour → 1day)
   - Compression de logs

3. **Usabilidade**
   - Defaults funcionam out-of-the-box
   - Pode desabilitar completamente se necessário
   - Fakes para testes (zero overhead)
   - Documentation clara

## Alternatives Considered

### 1. Observabilidade Opcional (Add-on)

```python
# Observabilidade como "extra"
class CreateUserUseCase:
    def execute(self, input_dto):
        # Lógica pura, sem instrumentação
        ...

# Usuário adiciona observabilidade manualmente
```

**Rejeitado porque:**
- Inconsistência: Alguns UseCases instrumentados, outros não
- Esquecimento: Fácil esquecer de adicionar
- Overhead: Instrumentação manual é verbosa
- Fragmentação: Cada dev faz de um jeito

### 2. Logging Tradicional (Strings)

```python
logger.info(f"User {user_id} created at {timestamp}")
```

**Rejeitado porque:**
- Não queryable
- Parsing complexo
- Sem contexto estruturado
- Difícil análise automatizada

### 3. Métricas Apenas em Pontos Críticos

**Rejeitado porque:**
- Linha tênue entre "crítico" e "não crítico"
- Tendência a sub-instrumentar
- Debugging fica mais difícil
- Melhor ter tudo e filtrar do que não ter

### 4. APM Comercial Obrigatório (DataDog, NewRelic)

**Rejeitado porque:**
- Vendor lock-in
- Custo alto
- Dependência externa obrigatória
- Preferimos open standards (OpenTelemetry)
- Solução: Suportar APMs como *opção*, não requirement

## Implementation Notes

### Para Desenvolvedores de UseCases

**Observabilidade é automática:**
```python
class MyUseCase(UseCaseBase):
    def execute(self, input_dto):
        # Logging e métricas já estão ativos
        # Apenas foque na lógica de negócio
        ...
```

**Para adicionar contexto específico:**
```python
def execute(self, input_dto):
    self.logger.info(
        "Processing order",
        order_id=input_dto.order_id,
        customer_id=input_dto.customer_id
    )
    ...
```

### Para Operadores

**Configuração mínima:**
```yaml
observability:
  level: standard
```

**Produção otimizada:**
```yaml
observability:
  level: minimal
  logging:
    handlers: [file]
  metrics:
    collection_interval: 300
  tracing:
    sampling_rate: 0.01  # 1%
```

## References

- **The Three Pillars of Observability** (Logs, Metrics, Traces)
- **OpenTelemetry Specification**
- **Site Reliability Engineering** by Google
- **Distributed Tracing in Practice** by Austin Parker et al.

## Related ADRs

- [ADR-001: Clean Architecture Choice](001-clean-architecture-choice.md)
- [ADR-004: Cognitive Testing](004-cognitive-testing.md)
- [ADR-006: ForgeProcess Integration](006-forgeprocess-integration.md)

---

**Author:** ForgeBase Development Team
**Date:** 2025-11-03
**Version:** 1.0
