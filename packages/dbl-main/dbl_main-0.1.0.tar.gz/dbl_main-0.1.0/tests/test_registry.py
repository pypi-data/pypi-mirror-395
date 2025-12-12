# test_registry.py

from dbl_core import BoundaryContext, PolicyDecision
from kl_kernel_logic import PsiDefinition

from dbl_main.core.registry import PolicyRegistry, PipelineRegistry
from dbl_main.core.pipeline import Pipeline
from dbl_main.policies.base import Policy


class DummyPolicy(Policy):
    @property
    def name(self) -> str:
        return "dummy"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(outcome="allow", reason="dummy")


def test_policy_registry_register_and_get():
    registry = PolicyRegistry()
    registry.register("dummy", DummyPolicy)
    
    cls = registry.get("dummy")
    assert cls is DummyPolicy


def test_policy_registry_create_instance():
    registry = PolicyRegistry()
    registry.register("dummy", DummyPolicy)
    
    policy = registry.create("dummy")
    
    assert policy is not None
    assert isinstance(policy, DummyPolicy)


def test_policy_registry_list_policies():
    registry = PolicyRegistry()
    registry.register("a", DummyPolicy)
    registry.register("b", DummyPolicy)
    
    names = registry.list_policies()
    
    assert "a" in names
    assert "b" in names


def test_pipeline_registry_register_and_get():
    registry = PipelineRegistry()
    pipeline = Pipeline(name="test", policies=[])
    
    registry.register("tenant-1:api", pipeline)
    
    result = registry.get("tenant-1:api")
    assert result is pipeline


def test_pipeline_registry_for_context_tenant_channel():
    registry = PipelineRegistry()
    pipeline = Pipeline(name="specific", policies=[])
    
    registry.register("tenant-1:api", pipeline)
    
    result = registry.for_context(tenant_id="tenant-1", channel="api")
    assert result is pipeline


def test_pipeline_registry_for_context_fallback_default():
    registry = PipelineRegistry()
    default_pipeline = Pipeline(name="default", policies=[])
    
    registry.register("default", default_pipeline)
    
    result = registry.for_context(tenant_id="unknown", channel="api")
    assert result is default_pipeline


def test_pipeline_registry_for_context_tenant_default():
    registry = PipelineRegistry()
    tenant_default = Pipeline(name="tenant-default", policies=[])
    
    registry.register("tenant-1:default", tenant_default)
    
    result = registry.for_context(tenant_id="tenant-1", channel="unknown")
    assert result is tenant_default

