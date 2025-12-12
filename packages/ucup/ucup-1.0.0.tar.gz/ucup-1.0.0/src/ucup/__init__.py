# UCUP/src/ucup/__init__.py
from .config import load_ucup_config, create_ucup_system
from .probabilistic import (
    ProbabilisticResult,
    AlternativePath,
    ProbabilisticAgent
)
from .metrics import (
    show_build_benefits,
    show_test_benefits,
    record_build_metrics,
    get_global_tracker,
    MetricsTracker,
    BenefitsDisplay
)
from .errors import (
    ProbabilisticError,
    ValidationError,
    ErrorHandler,
    get_error_handler
)
from .validation import (
    ValidationReport,
    validate_data
)
from .testing import (
    AgentTestSuite,
    Scenario,
    ExpectedOutcome,
    TestRun,
    ScenarioContext,
    CustomerServiceContext,
    AdversarialTestGenerator,
    ProbabilisticAssert,
    BenchmarkIntegration,
    APITestingHarness,
    DynamicScenarioGenerator,
    AgentNetworkIntegrationTester,
    PerformanceDegradationTester,
    ComparativeModelTester,
    UserSimulationTester,
    TestScenario,
    ScenarioGenerationResult,
    IntelligentTestGenerator
)

# Import from multimodal submodules
from .multimodal.fusion_engine import (
    MultimodalInputs,
    MultimodalFusionEngine,
    FusedAnalysis,
    fuse_multimodal,
    create_fusion_engine
)

from .multimodal.streaming_processor import (
    RealTimeStreamingProcessor,
    StreamChunk,
    StreamingAnalysis
)

# MultimodalAgentTester is optional - import it separately if needed
# Note: testing/ dir contains additional testing utilities but is not a package
MultimodalAgentTester = None

__version__ = "0.2.0"

__all__ = [
    'load_ucup_config',
    'create_ucup_system',
    'ProbabilisticResult',
    'AlternativePath',
    'ProbabilisticAgent',
    'show_build_benefits',
    'show_test_benefits',
    'record_build_metrics',
    'get_global_tracker',
    'MetricsTracker',
    'BenefitsDisplay',
    'ProbabilisticError',
    'ValidationError',
    'ErrorHandler',
    'get_error_handler',
    'ValidationReport',
    'validate_data',
    'AgentTestSuite',
    'Scenario',
    'ExpectedOutcome',
    'TestRun',
    'ScenarioContext',
    'CustomerServiceContext',
    'AdversarialTestGenerator',
    'ProbabilisticAssert',
    'BenchmarkIntegration',
    'APITestingHarness',
    'DynamicScenarioGenerator',
    'AgentNetworkIntegrationTester',
    'PerformanceDegradationTester',
    'ComparativeModelTester',
    'UserSimulationTester',
    'MultimodalFusionEngine',
    'MultimodalInputs',
    'FusedAnalysis',
    'fuse_multimodal',
    'create_fusion_engine',
    'RealTimeStreamingProcessor',
    'StreamChunk',
    'StreamingAnalysis',
    'MultimodalAgentTester',
    'IntelligentTestGenerator',
    'TestScenario',
    'ScenarioGenerationResult'
]
