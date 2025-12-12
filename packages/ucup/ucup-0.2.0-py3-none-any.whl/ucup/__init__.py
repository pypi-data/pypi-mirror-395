"""
UCUP: Unified Cognitive Uncertainty Processing Framework for Agentic AI

This package provides comprehensive tools for building reliable, observable,
and well-tested agentic AI systems.
"""

from .probabilistic import (
    ProbabilisticAgent, ProbabilisticResult, AlternativePath, AgentState,
    BayesianNetwork, MarkovDecisionProcess, MonteCarloTreeSearch,
    BayesianAgent, MDPAgent, MCTSReasoner
)
from .multimodal import (
    MultiModalProcessor, MultiModalInput, MultiModalFeatures,
    VisionLanguageAgent, StructuredDataAgent, AudioAnalysisAgent
)
from .observability import DecisionTracer, DecisionExplorer, ReasoningVisualizer, LiveAgentMonitor
from .testing import AgentTestSuite, AdversarialTestGenerator, ProbabilisticAssert, AgentEvalPipeline
from .coordination import (
    HierarchicalCoordination, DebateCoordination, MarketBasedCoordination, SwarmCoordination,
    AdaptiveOrchestrator, AgentMessageBus, SmartAgentRouter, EnhancedAdaptiveOrchestrator,
    LearningStrategySelector, ContextAwareStrategySelector
)
from .reliability import FailureDetector, AutomatedRecoveryPipeline, StateCheckpointer, GracefulDegradationManager

# Plugin system (commented out - not yet implemented)
# from . import plugins
# from .plugins import (
#     PluginManager, PluginInterface, AgentPlugin, StrategyPlugin, MonitorPlugin, SerializerPlugin,
#     PluginMetadata, PluginHook, get_plugin_manager, initialize_plugin_system
# )

# Configuration DSL
from . import config
from .config import (
    ConfigLoader, ConfigValidator, ConfigResolver, ConfigContext, ConfigReference,
    load_ucup_config, create_ucup_system
)

# Deployment and monitoring
from . import deployment
from .deployment import (
    DeploymentManager, DeploymentProvider, DockerDeploymentProvider, KubernetesDeploymentProvider,
    HealthMonitor, AutoScaler, MetricsCollector, get_deployment_manager,
    DeploymentState, ScalingStrategy, HealthCheck, ScalingConfig, ContainerConfig, DeploymentSpec
)

__version__ = "0.1.0"
__all__ = [
    # Probabilistic Core
    "ProbabilisticAgent",
    "ProbabilisticResult",
    "AlternativePath",
    "AgentState",

    # Advanced Probabilistic Models
    "BayesianNetwork",
    "MarkovDecisionProcess",
    "MonteCarloTreeSearch",
    "BayesianAgent",
    "MDPAgent",
    "MCTSReasoner",

    # Multi-modal Support
    "MultiModalProcessor",
    "MultiModalInput",
    "MultiModalFeatures",
    "VisionLanguageAgent",
    "StructuredDataAgent",
    "AudioAnalysisAgent",

    # Observability
    "DecisionTracer",
    "DecisionExplorer",
    "ReasoningVisualizer",
    "LiveAgentMonitor",

    # Testing & Evaluation
    "AgentTestSuite",
    "AdversarialTestGenerator",
    "ProbabilisticAssert",
    "AgentEvalPipeline",

    # Coordination
    "HierarchicalCoordination",
    "DebateCoordination",
    "MarketBasedCoordination",
    "SwarmCoordination",
    "AdaptiveOrchestrator",
    "AgentMessageBus",
    "SmartAgentRouter",
    "EnhancedAdaptiveOrchestrator",
    "LearningStrategySelector",
    "ContextAwareStrategySelector",

    # Reliability
    "FailureDetector",
    "AutomatedRecoveryPipeline",
    "StateCheckpointer",
    "GracefulDegradationManager",

    # Plugin System
    "plugins",
    "PluginManager",
    "PluginInterface",
    "AgentPlugin",
    "StrategyPlugin",
    "MonitorPlugin",
    "SerializerPlugin",
    "PluginMetadata",
    "PluginHook",
    "get_plugin_manager",
    "initialize_plugin_system",

    # Configuration DSL
    "config",
    "ConfigLoader",
    "ConfigValidator",
    "ConfigResolver",
    "ConfigContext",
    "ConfigReference",
    "load_ucup_config",
    "create_ucup_system",

    # Deployment and monitoring
    "deployment",
    "DeploymentManager",
    "DeploymentProvider",
    "DockerDeploymentProvider",
    "KubernetesDeploymentProvider",
    "HealthMonitor",
    "AutoScaler",
    "MetricsCollector",
    "get_deployment_manager",
    "DeploymentState",
    "ScalingStrategy",
    "HealthCheck",
    "ScalingConfig",
    "ContainerConfig",
    "DeploymentSpec"
]
