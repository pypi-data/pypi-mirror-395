"""
Multimodal processing components for UCUP framework.

This module provides advanced multimodal fusion and real-time streaming capabilities.
"""

from .fusion_engine import (
    MultimodalInputs,
    MultimodalFusionEngine,
    FusedAnalysis,
    fuse_multimodal,
    create_fusion_engine
)

from .streaming_processor import (
    RealTimeStreamingProcessor,
    StreamChunk,
    StreamingAnalysis
)

__all__ = [
    'MultimodalInputs',
    'MultimodalFusionEngine',
    'FusedAnalysis',
    'fuse_multimodal',
    'create_fusion_engine',
    'RealTimeStreamingProcessor',
    'StreamChunk',
    'StreamingAnalysis'
]
