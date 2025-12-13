# Apps derivados de ForgeBase e agentes de IA

> Como criar apps que expõem uma experiência padrão para agentes de código, reaproveitando o ecossistema do ForgeBase.

Este guia é para quem **constrói um novo aplicativo usando ForgeBase como base** e quer que:

- agentes de IA consigam descobrir as APIs do app de forma padronizada;
- clientes que instalam o app via `pip install meu_app` tenham a mesma experiência de discovery que já existe no ForgeBase.

---

## Objetivo de design

Para cada app derivado de ForgeBase, queremos:

- um módulo `meu_app.dev` dedicado a agentes de IA;
- um guia rápido embutido (`get_agent_quickstart()`), igual ao do ForgeBase;
- uma API de discovery que escaneia **somente o pacote do app**, não o código interno do ForgeBase;
- um trecho padrão no `README.md` explicando isso para agentes.

Assim, qualquer agente que aprendeu a usar ForgeBase também sabe usar o seu app.

---

## Estrutura recomendada de projeto

Suponha um app chamado `meu_app`:

```text
src/
  meu_app/
    __init__.py
    domain/
    application/
    adapters/
    infrastructure/
    _docs/
      AI_AGENT_QUICK_START.md
    dev/
      __init__.py
      api/
        __init__.py
        discovery.py
```

- `meu_app._docs/AI_AGENT_QUICK_START.md`: guia rápido para agentes de IA (do seu app).
- `meu_app.dev`: ponto de entrada para agentes (`get_agent_quickstart`, `get_documentation_path`, etc.).
- `meu_app.dev.api`: aqui você reexpõe discovery, quality checks, testes, etc.

---

## Passo 1 — `meu_app.dev` com `get_agent_quickstart`

Implemente em `src/meu_app/dev/__init__.py` algo inspirado no ForgeBase:

```python
# src/meu_app/dev/__init__.py
import importlib.resources as resources
from pathlib import Path


def get_agent_quickstart() -> str:
    """Retorna o guia rápido para agentes de IA do seu app."""
    try:
        if hasattr(resources, "files"):
            doc_file = resources.files("meu_app._docs") / "AI_AGENT_QUICK_START.md"
            return doc_file.read_text(encoding="utf-8")
    except (FileNotFoundError, ModuleNotFoundError, AttributeError):
        pass

    # Fallback de desenvolvimento (opcional)
    project_root = Path(__file__).parent.parent.parent
    quickstart_path = project_root / "docs" / "usuarios" / "meu_app_quickstart.md"
    if quickstart_path.exists():
        return quickstart_path.read_text(encoding="utf-8")

    return "# Quickstart para agentes\n\nDocumentação não encontrada."
```

No seu `AI_AGENT_QUICK_START.md`, documente claramente:

- principais APIs do app;
- como rodar discovery;
- como rodar testes e quality checks do próprio app.

---

## Passo 2 — API de discovery específica do app

Em vez de cada projeto reinventar discovery, reutilize o mecanismo do ForgeBase via `ComponentDiscovery`, agora com suporte a `package_name`.

Crie `src/meu_app/dev/api/discovery.py`:

```python
# src/meu_app/dev/api/discovery.py
from forgebase.dev.api import ComponentDiscovery as BaseComponentDiscovery


class ComponentDiscovery(BaseComponentDiscovery):
    """Discovery dos componentes do pacote meu_app.

    Escaneia apenas o código do app, mesmo quando instalado via pip.
    """

    def __init__(self) -> None:
        # package_name → resolve caminho do pacote instalado (site-packages ou src/)
        super().__init__(package_name="meu_app")
```

Depois, em `src/meu_app/dev/api/__init__.py`, reexporte essa classe:

```python
# src/meu_app/dev/api/__init__.py
from .discovery import ComponentDiscovery

__all__ = ["ComponentDiscovery"]
```

Uso dentro do app ou por agentes de clientes:

```python
from meu_app.dev.api import ComponentDiscovery

discovery = ComponentDiscovery()
result = discovery.scan_project()

for usecase in result.usecases:
    print(usecase.name, usecase.file_path)
```

Isso garante que:

- apenas `meu_app` é escaneado (não o código interno do ForgeBase);
- funciona igual em desenvolvimento e em produção (instalado via `pip`).

---

## Passo 3 — Reusar outras APIs do ForgeBase (opcional)

Se fizer sentido para o seu app, você pode reexportar também:

- `QualityChecker` (para checks específicos do seu repo),
- `TestRunner` (para rodada de testes do projeto),
- `ScaffoldGenerator` (se você tiver scaffolds próprios).

Exemplo simples:

```python
# src/meu_app/dev/api/__init__.py
from forgebase.dev.api import QualityChecker, TestRunner
from .discovery import ComponentDiscovery

__all__ = [
    "ComponentDiscovery",
    "QualityChecker",
    "TestRunner",
]
```

Documente no seu `AI_AGENT_QUICK_START.md` como essas APIs se aplicam ao seu projeto.

---

## Passo 4 — Seção padrão no README do seu app

Adicione no `README.md` do app uma seção explícita para agentes, seguindo o padrão do ForgeBase:

```markdown
## Para Agentes de Código de IA

```python
from meu_app.dev import get_agent_quickstart

guide = get_agent_quickstart()  # Markdown completo com APIs do app
print(guide)
```

### Descoberta de componentes do app

```python
from meu_app.dev.api import ComponentDiscovery

discovery = ComponentDiscovery()
result = discovery.scan_project()
print(f"UseCases encontrados: {len(result.usecases)}")
```
```

Isso garante que:

- agentes que leem apenas o `README.md` saibam como começar;
- a experiência é consistente com a do ForgeBase.

---

## Passo 5 — Como agentes dos seus clientes irão usar

Uma vez que seu app está publicado e instalado via `pip`, o fluxo típico para um agente é:

```python
from meu_app.dev import get_agent_quickstart
from meu_app.dev.api import ComponentDiscovery

# 1. Ler guia rápido do app
guide = get_agent_quickstart()

# 2. Fazer discovery de componentes específicos do app
discovery = ComponentDiscovery()
components = discovery.scan_project()

print("Entidades:", [e.name for e in components.entities])
print("UseCases:", [u.name for u in components.usecases])
```

Nenhum agente precisa conhecer detalhes de layout de pastas do seu repo — tudo é exposto via APIs estáveis.

---

## Exemplo completo: `orders_app`

Para tornar tudo mais concreto, abaixo um exemplo mínimo de app derivado chamado `orders_app`.

### Estrutura de pastas

```text
src/
  orders_app/
    __init__.py
    domain/
      order.py
    application/
      create_order_usecase.py
    _docs/
      AI_AGENT_QUICK_START.md
    dev/
      __init__.py
      api/
        __init__.py
        discovery.py
```

### `orders_app/domain/order.py`

```python
from forgebase.domain import EntityBase


class Order(EntityBase):
    """Entidade de domínio Order."""

    def __init__(self, id: str | None, customer_id: str, total: float) -> None:
        super().__init__(id)
        self.customer_id = customer_id
        self.total = total

    def validate(self) -> None:
        if not self.customer_id:
            raise ValueError("customer_id é obrigatório")
        if self.total < 0:
            raise ValueError("total não pode ser negativo")
```

### `orders_app/application/create_order_usecase.py`

```python
from forgebase.application import UseCaseBase


class CreateOrderInput:
    def __init__(self, customer_id: str, total: float) -> None:
        self.customer_id = customer_id
        self.total = total


class CreateOrderOutput:
    def __init__(self, order_id: str) -> None:
        self.order_id = order_id


class CreateOrderUseCase(UseCaseBase[CreateOrderInput, CreateOrderOutput]):
    """UseCase de criação de pedido."""

    def _before_execute(self) -> None:
        pass

    def _after_execute(self) -> None:
        pass

    def _on_error(self, error: Exception) -> None:
        raise error

    def execute(self, input_dto: CreateOrderInput) -> CreateOrderOutput:
        # Aqui você usaria um repositório real; para exemplo, gera ID fixo
        if input_dto.total <= 0:
            raise ValueError("total deve ser maior que zero")
        order_id = "order-123"
        return CreateOrderOutput(order_id=order_id)
```

### `orders_app/dev/__init__.py`

```python
import importlib.resources as resources
from pathlib import Path


def get_agent_quickstart() -> str:
    """Guia rápido para agentes de IA do orders_app."""
    try:
        if hasattr(resources, "files"):
            doc_file = resources.files("orders_app._docs") / "AI_AGENT_QUICK_START.md"
            return doc_file.read_text(encoding="utf-8")
    except (FileNotFoundError, ModuleNotFoundError, AttributeError):
        pass

    project_root = Path(__file__).parent.parent.parent
    quickstart_path = project_root / "docs" / "usuarios" / "orders_app_quickstart.md"
    if quickstart_path.exists():
        return quickstart_path.read_text(encoding="utf-8")

    return "# Quickstart orders_app\n\nDocumentação não encontrada."
```

### `orders_app/dev/api/discovery.py`

```python
from forgebase.dev.api import ComponentDiscovery as BaseComponentDiscovery


class ComponentDiscovery(BaseComponentDiscovery):
    """Discovery dos componentes do pacote orders_app."""

    def __init__(self) -> None:
        super().__init__(package_name="orders_app")
```

### `orders_app/dev/api/__init__.py`

```python
from .discovery import ComponentDiscovery

__all__ = ["ComponentDiscovery"]
```

### `orders_app/_docs/AI_AGENT_QUICK_START.md`

```markdown
# orders_app - Guia Rápido para Agentes de IA

```python
from orders_app.dev import get_agent_quickstart
from orders_app.dev.api import ComponentDiscovery

guide = get_agent_quickstart()
discovery = ComponentDiscovery()
result = discovery.scan_project()

print("Entidades:", [e.name for e in result.entities])
print("UseCases:", [u.name for u in result.usecases])
```
```

Com essa estrutura, qualquer agente consegue:

- descobrir a documentação do app via `get_agent_quickstart()`;
- fazer discovery dos componentes específicos do `orders_app` via `orders_app.dev.api.ComponentDiscovery`;
- aplicar os mesmos padrões que já usa com o ForgeBase.

---

## Resumo

- Use `forgebase.dev.api.ComponentDiscovery(package_name="meu_app")` como base para o discovery do seu app.
- Sempre exponha um módulo `meu_app.dev` com `get_agent_quickstart()`.
- Replique o padrão do README do ForgeBase para explicar isso aos agentes.
- Assim, qualquer app derivado de ForgeBase oferece uma experiência consistente e previsível para agentes de IA, tanto em desenvolvimento quanto em produção.
