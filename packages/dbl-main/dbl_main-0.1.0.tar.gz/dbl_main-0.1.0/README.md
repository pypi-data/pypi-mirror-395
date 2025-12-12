# DBL Main

Deterministic Boundary Layer - policies, pipelines, bindings on `dbl-core`.

DBL Main configures and orchestrates boundary evaluation for real applications. `dbl-core` stays the minimal deterministic engine.

## Architecture

```
┌──────────────────────────────────────────────┐
│ Application / Product / Gateway             │
│ (HTTP API, CLI, Service, Agent, ...)        │
├──────────────────────────────────────────────┤
│ DBL Main (this repo)                        │
│ - Policy registry                            │
│ - Pipelines                                  │
│ - Bindings / adapters                        │
│ - Config, tenants, audit                     │
├──────────────────────────────────────────────┤
│ dbl-core                                     │
│ - deterministic boundary engine              │
├──────────────────────────────────────────────┤
│ kl-kernel-logic                              │
│ - execution substrate (Δ, V, t)              │
└──────────────────────────────────────────────┘
```

- [`kl-kernel-logic`](https://github.com/lukaspfisterch/kl-kernel-logic) - deterministic execution substrate
- [`dbl-core`](https://github.com/lukaspfisterch/dbl-core) - minimal boundary evaluation engine
- `dbl-main` (this repo) - policies, pipelines, bindings

This structure follows [KL Execution Theory](https://github.com/lukaspfisterch/kl-execution-theory).

Pipelines in DBL Main orchestrate policies and produce a `BoundaryResult` (from `dbl-core`) used to decide whether the kernel is called.

## Install

```bash
pip install dbl-main
```

Requires `dbl-core>=0.2.0`, `kl-kernel-logic>=0.4.0`, Python 3.11+.

## Configuration

DBL Main loads policies and pipelines from external configuration.

```
config/
  pipelines.yaml
  policies.yaml
  tenants/
    tenant-1.yaml
    tenant-2.yaml
```

Example:

```yaml
# config/pipelines.yaml
pipelines:
  default:
    policies:
      - rate-limit
      - content-safety

# config/policies.yaml
policies:
  rate-limit:
    max_requests: 100
  content-safety:
    blocked_patterns:
      - "forbidden"
```

Loading:

```python
from dbl_main.config import load_config, build_pipeline_for

cfg = load_config("config")
pipeline = build_pipeline_for(cfg, tenant_id="tenant-1", use_case="llm-generate")
result = pipeline.evaluate(ctx)
```

Configuration is external, versionable, and auditable.

## Usage

```python
from kl_kernel_logic import PsiDefinition, Kernel
from dbl_core import BoundaryContext
from dbl_main import Pipeline
from dbl_main.policies import RateLimitPolicy, ContentSafetyPolicy

# Build context
psi = PsiDefinition(psi_type="llm", name="generate")
ctx = BoundaryContext(
    psi=psi,
    caller_id="user-1",
    tenant_id="tenant-1",
    metadata={"prompt": "Hello world"},
)

# Build pipeline
pipeline = Pipeline(
    name="default",
    policies=[
        RateLimitPolicy(max_requests=100),
        ContentSafetyPolicy(blocked_patterns=["forbidden"]),
    ],
)

# Evaluate boundaries
result = pipeline.evaluate(ctx)

if result.is_allowed():
    # Proceed with kernel execution
    kernel = Kernel()
    trace = kernel.execute(
        psi=result.effective_psi,
        task=my_task_fn,
        **result.effective_metadata,
    )
else:
    print(result.final_outcome, result.decisions[-1].reason)
```

Note: The `Kernel.execute()` call above is illustrative. See `kl-kernel-logic` for the actual API.

## Components

### Pipeline

Ordered sequence of policies. Evaluates each policy, aggregates decisions, stops on block. Returns a `BoundaryResult` from `dbl-core`.

### Policies

- `RateLimitPolicy` - request rate limiting
- `ContentSafetyPolicy` - content pattern blocking

Implement `Policy` base class for custom policies:

```python
from dbl_main.policies.base import Policy
from dbl_core import BoundaryContext, PolicyDecision

class MyPolicy(Policy):
    @property
    def name(self) -> str:
        return "my-policy"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(outcome="allow", reason="passed")
```

### Registries

- `PolicyRegistry` - register policy classes by name
- `PipelineRegistry` - register pipelines by tenant/channel

### Audit

- `AuditLogger` - log boundary evaluation results

## Design

- Pipelines are deterministic for the same config and input
- Policies are side-effect free with respect to `BoundaryContext`
- Registries and loaders are pure configuration, no hardcoded rules
- External config enables versioning and audit trails

## Guarantees

- No mutation of `BoundaryContext` by policies
- All decisions flow through `PolicyDecision` and `BoundaryResult`
- Configuration is file-based, versionable, and auditable
- Pipeline evaluation is deterministic

These guarantees are enforced by executable tests. See [docs/testing.md](docs/testing.md) for details.

## Testing

```bash
# Install with test dependencies
pip install -e .[test]

# Run tests
pytest

# With property-based tests (hypothesis)
pip install -e .[test-fuzz]
pytest
```

## License

[MIT](LICENSE)
