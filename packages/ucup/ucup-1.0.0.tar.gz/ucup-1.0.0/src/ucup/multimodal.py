"""
Multi-modal agent support for UCUP Framework.

This module provides agents capable of processing and reasoning about
multiple modalities including text, images, audio, and structured data.
"""

import asyncio
import base64
import io
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Protocol, Tuple
from PIL import Image
import numpy as np

from .probabilistic import ProbabilisticAgent, ProbabilisticResult, AlternativePath


class ModalityProcessor(Protocol):
    """Protocol for processing different input modalities."""

    async def process(self, input_data: Any, **kwargs) -> Dict[str, Any]:
        """Process input data for a specific modality."""
        ...


class TextProcessor(ModalityProcessor):
    """Processes text inputs."""

    async def process(self, input_data: str, **kwargs) -> Dict[str, Any]:
        """Process text input."""
        # Basic text processing - could be enhanced with NLP
        return {
            'modality': 'text',
            'content': input_data,
            'length': len(input_data),
            'tokens': input_data.split(),  # Simple tokenization
            'sentiment': self._analyze_sentiment(input_data)
        }

    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis."""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'love']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst']

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'


class ImageProcessor(ModalityProcessor):
    """Processes image inputs."""

    async def process(self, input_data: Union[str, bytes, Image.Image], **kwargs) -> Dict[str, Any]:
        """Process image input."""
        try:
            if isinstance(input_data, str):
                # Assume base64 encoded image
                image_data = base64.b64decode(input_data)
                image = Image.open(io.BytesIO(image_data))
            elif isinstance(input_data, bytes):
                image = Image.open(io.BytesIO(input_data))
            elif isinstance(input_data, Image.Image):
                image = input_data
            else:
                raise ValueError("Unsupported image input type")

            # Basic image analysis
            width, height = image.size
            mode = image.mode

            # Convert to numpy array for further processing
            image_array = np.array(image)

            return {
                'modality': 'image',
                'dimensions': (width, height),
                'mode': mode,
                'format': image.format,
                'size_bytes': len(image.tobytes()) if hasattr(image, 'tobytes') else 0,
                'dominant_colors': self._extract_dominant_colors(image_array),
                'image_array': image_array
            }
        except Exception as e:
            return {
                'modality': 'image',
                'error': str(e),
                'processed': False
            }

    def _extract_dominant_colors(self, image_array: np.ndarray, num_colors: int = 3) -> List[Tuple[int, int, int]]:
        """Extract dominant colors from image (simplified)."""
        try:
            # Flatten image and sample pixels
            pixels = image_array.reshape(-1, image_array.shape[-1])
            if pixels.shape[-1] >= 3:
                # Sample every 10th pixel for performance
                sampled_pixels = pixels[::10]

                # Simple clustering - just return most common colors
                # In practice, would use k-means clustering
                unique_colors, counts = np.unique(sampled_pixels, axis=0, return_counts=True)
                top_indices = np.argsort(counts)[-num_colors:]
                dominant_colors = unique_colors[top_indices]

                return [tuple(color[:3]) for color in dominant_colors]
            else:
                return []
        except:
            return []


class AudioProcessor(ModalityProcessor):
    """Processes audio inputs."""

    async def process(self, input_data: Union[str, bytes], **kwargs) -> Dict[str, Any]:
        """Process audio input."""
        try:
            # This is a placeholder - real audio processing would require librosa or similar
            if isinstance(input_data, str):
                # Assume base64 encoded audio
                audio_data = base64.b64decode(input_data)
            elif isinstance(input_data, bytes):
                audio_data = input_data
            else:
                raise ValueError("Unsupported audio input type")

            return {
                'modality': 'audio',
                'size_bytes': len(audio_data),
                'duration_seconds': None,  # Would need audio library to determine
                'sample_rate': None,       # Would need audio library to determine
                'channels': None,          # Would need audio library to determine
                'features': self._extract_audio_features(audio_data)
            }
        except Exception as e:
            return {
                'modality': 'audio',
                'error': str(e),
                'processed': False
            }

    def _extract_audio_features(self, audio_data: bytes) -> Dict[str, Any]:
        """Extract basic audio features (placeholder)."""
        # In practice, would extract MFCCs, spectrograms, etc.
        return {
            'energy': None,  # Would compute RMS energy
            'pitch': None,   # Would compute fundamental frequency
            'tempo': None    # Would estimate tempo
        }


class StructuredDataProcessor(ModalityProcessor):
    """Processes structured data inputs (JSON, CSV, etc.)."""

    async def process(self, input_data: Union[str, Dict, List], **kwargs) -> Dict[str, Any]:
        """Process structured data input."""
        try:
            if isinstance(input_data, str):
                # Try to parse as JSON
                import json
                try:
                    parsed_data = json.loads(input_data)
                except json.JSONDecodeError:
                    # Treat as CSV or plain text
                    parsed_data = input_data
            else:
                parsed_data = input_data

            return {
                'modality': 'structured_data',
                'data_type': type(parsed_data).__name__,
                'structure': self._analyze_structure(parsed_data),
                'summary': self._generate_summary(parsed_data),
                'parsed_data': parsed_data
            }
        except Exception as e:
            return {
                'modality': 'structured_data',
                'error': str(e),
                'processed': False
            }

    def _analyze_structure(self, data: Any) -> Dict[str, Any]:
        """Analyze the structure of the data."""
        if isinstance(data, dict):
            return {
                'type': 'object',
                'keys': list(data.keys()),
                'depth': self._calculate_depth(data)
            }
        elif isinstance(data, list):
            return {
                'type': 'array',
                'length': len(data),
                'element_types': list(set(type(item).__name__ for item in data[:10]))  # Sample first 10
            }
        else:
            return {'type': type(data).__name__}

    def _calculate_depth(self, data: Any, max_depth: int = 10) -> int:
        """Calculate nesting depth of data structure."""
        if not isinstance(data, (dict, list)) or max_depth <= 0:
            return 0

        if isinstance(data, dict):
            return 1 + max((self._calculate_depth(value, max_depth - 1) for value in data.values()), default=0)
        elif isinstance(data, list):
            return 1 + max((self._calculate_depth(item, max_depth - 1) for item in data), default=0)

        return 0

    def _generate_summary(self, data: Any) -> Dict[str, Any]:
        """Generate a summary of the data."""
        if isinstance(data, dict):
            return {
                'num_fields': len(data),
                'field_types': {k: type(v).__name__ for k, v in data.items()}
            }
        elif isinstance(data, list):
            return {
                'num_items': len(data),
                'item_types': list(set(type(item).__name__ for item in data))
            }
        else:
            return {'value_type': type(data).__name__}


@dataclass
class MultiModalInput:
    """Container for multi-modal input data."""
    modalities: Dict[str, Any] = field(default_factory=dict)  # modality_name -> data
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_modality(self, name: str, data: Any):
        """Add a modality to the input."""
        self.modalities[name] = data

    def get_modality(self, name: str) -> Any:
        """Get data for a specific modality."""
        return self.modalities.get(name)


@dataclass
class MultiModalFeatures:
    """Extracted features from multi-modal inputs."""
    text_features: Dict[str, Any] = field(default_factory=dict)
    image_features: Dict[str, Any] = field(default_factory=dict)
    audio_features: Dict[str, Any] = field(default_factory=dict)
    structured_features: Dict[str, Any] = field(default_factory=dict)
    cross_modal_features: Dict[str, Any] = field(default_factory=dict)  # Relationships between modalities


class MultiModalProcessor:
    """Processes multiple modalities and extracts cross-modal features."""

    def __init__(self):
        self.processors = {
            'text': TextProcessor(),
            'image': ImageProcessor(),
            'audio': AudioProcessor(),
            'structured_data': StructuredDataProcessor()
        }

    async def process_input(self, multimodal_input: MultiModalInput) -> MultiModalFeatures:
        """Process all modalities in the input."""
        features = MultiModalFeatures()

        # Process each modality
        processing_tasks = []
        for modality_name, data in multimodal_input.modalities.items():
            if modality_name in self.processors:
                task = self.processors[modality_name].process(data)
                processing_tasks.append((modality_name, task))

        # Execute processing tasks
        results = await asyncio.gather(*[task for _, task in processing_tasks])

        # Organize results
        for (modality_name, _), result in zip(processing_tasks, results):
            if modality_name == 'text':
                features.text_features = result
            elif modality_name == 'image':
                features.image_features = result
            elif modality_name == 'audio':
                features.audio_features = result
            elif modality_name == 'structured_data':
                features.structured_features = result

        # Extract cross-modal features
        features.cross_modal_features = self._extract_cross_modal_features(features)

        return features

    def _extract_cross_modal_features(self, features: MultiModalFeatures) -> Dict[str, Any]:
        """Extract features that relate multiple modalities."""
        cross_features = {}

        # Text-Image relationships
        if features.text_features and features.image_features:
            cross_features['text_image_alignment'] = self._analyze_text_image_alignment(
                features.text_features, features.image_features
            )

        # Text-Structured Data relationships
        if features.text_features and features.structured_features:
            cross_features['text_data_relevance'] = self._analyze_text_data_relevance(
                features.text_features, features.structured_features
            )

        # Image-Structured Data relationships
        if features.image_features and features.structured_features:
            cross_features['visual_data_correlation'] = self._analyze_visual_data_correlation(
                features.image_features, features.structured_features
            )

        return cross_features

    def _analyze_text_image_alignment(self, text_feat: Dict, image_feat: Dict) -> float:
        """Analyze how well text and image align (simplified)."""
        # This would use CLIP or similar models in practice
        # For now, return a mock alignment score
        return 0.7  # Placeholder

    def _analyze_text_data_relevance(self, text_feat: Dict, data_feat: Dict) -> float:
        """Analyze relevance between text and structured data."""
        # Simple keyword matching
        text_content = text_feat.get('content', '').lower()
        data_keys = ' '.join(data_feat.get('structure', {}).get('keys', [])).lower()

        common_words = set(text_content.split()) & set(data_keys.split())
        return len(common_words) / max(len(set(text_content.split())), 1)

    def _analyze_visual_data_correlation(self, image_feat: Dict, data_feat: Dict) -> float:
        """Analyze correlation between visual and structured data."""
        # Placeholder - would analyze if image represents the data
        return 0.5


class VisionLanguageAgent(ProbabilisticAgent):
    """
    Agent that can process both text and images for comprehensive reasoning.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.multimodal_processor = MultiModalProcessor()

    async def execute(self, task: str, **kwargs) -> ProbabilisticResult:
        """Execute task with vision-language capabilities."""
        # Extract multimodal inputs
        multimodal_input = kwargs.get('multimodal_input')
        if not multimodal_input:
            # Fallback to text-only processing
            return await super().execute(task, **kwargs)

        # Process multimodal inputs
        features = await self.multimodal_processor.process_input(multimodal_input)

        # Generate reasoning prompt incorporating all modalities
        enhanced_prompt = self._create_multimodal_prompt(task, features)

        # Use LLM with multimodal context
        result, confidence = await self.llm.generate_with_confidence(enhanced_prompt)

        # Create alternatives based on different modality combinations
        alternatives = self._generate_multimodal_alternatives(task, features)

        return ProbabilisticResult(
            value=result,
            confidence=confidence,
            alternatives=alternatives,
            metadata={
                'modalities_used': list(multimodal_input.modalities.keys()),
                'multimodal_features': features.__dict__,
                'reasoning_type': 'vision_language'
            }
        )

    def _create_multimodal_prompt(self, task: str, features: MultiModalFeatures) -> str:
        """Create a prompt that incorporates multiple modalities."""
        prompt_parts = [f"Task: {task}\n"]

        # Add text context
        if features.text_features:
            text_content = features.text_features.get('content', '')
            sentiment = features.text_features.get('sentiment', 'neutral')
            prompt_parts.append(f"Text Content: {text_content}")
            prompt_parts.append(f"Text Sentiment: {sentiment}")

        # Add image context
        if features.image_features:
            dimensions = features.image_features.get('dimensions', 'unknown')
            colors = features.image_features.get('dominant_colors', [])
            prompt_parts.append(f"Image Dimensions: {dimensions}")
            if colors:
                prompt_parts.append(f"Dominant Colors: {colors}")

        # Add structured data context
        if features.structured_features:
            data_type = features.structured_features.get('data_type', 'unknown')
            structure = features.structured_features.get('structure', {})
            prompt_parts.append(f"Data Type: {data_type}")
            prompt_parts.append(f"Data Structure: {structure}")

        # Add cross-modal insights
        if features.cross_modal_features:
            alignment = features.cross_modal_features.get('text_image_alignment', 0)
            relevance = features.cross_modal_features.get('text_data_relevance', 0)
            prompt_parts.append(f"Text-Image Alignment: {alignment:.2f}")
            prompt_parts.append(f"Text-Data Relevance: {relevance:.2f}")

        prompt_parts.append("\nProvide a comprehensive answer considering all available modalities.")

        return "\n".join(prompt_parts)

    def _generate_multimodal_alternatives(self, task: str, features: MultiModalFeatures) -> List[AlternativePath]:
        """Generate alternative interpretations based on different modality combinations."""
        alternatives = []

        # Text-only alternative
        if features.text_features:
            alternatives.append(AlternativePath(
                value="Text-only analysis",
                confidence=0.6,
                reasoning_steps=["Focused solely on textual content"]
            ))

        # Image-focused alternative
        if features.image_features:
            alternatives.append(AlternativePath(
                value="Vision-focused analysis",
                confidence=0.7,
                reasoning_steps=["Prioritized visual information"]
            ))

        # Data-driven alternative
        if features.structured_features:
            alternatives.append(AlternativePath(
                value="Data-centric analysis",
                confidence=0.8,
                reasoning_steps=["Emphasized structured data insights"]
            ))

        return alternatives


class StructuredDataAgent(ProbabilisticAgent):
    """
    Agent specialized in analyzing and reasoning about structured data.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_processor = StructuredDataProcessor()

    async def execute(self, task: str, **kwargs) -> ProbabilisticResult:
        """Execute task with structured data analysis capabilities."""
        data_input = kwargs.get('data_input')
        if not data_input:
            return await super().execute(task, **kwargs)

        # Process the structured data
        data_features = await self.data_processor.process(data_input)

        # Generate analysis prompt
        analysis_prompt = self._create_data_analysis_prompt(task, data_features)

        # Get analysis from LLM
        result, confidence = await self.llm.generate_with_confidence(analysis_prompt)

        # Generate alternative analyses
        alternatives = self._generate_data_alternatives(task, data_features)

        return ProbabilisticResult(
            value=result,
            confidence=confidence,
            alternatives=alternatives,
            metadata={
                'data_analysis': True,
                'data_features': data_features,
                'analysis_type': 'structured_data'
            }
        )

    def _create_data_analysis_prompt(self, task: str, data_features: Dict[str, Any]) -> str:
        """Create prompt for data analysis."""
        structure = data_features.get('structure', {})
        summary = data_features.get('summary', {})

        prompt = f"""
Task: {task}

Data Analysis Context:
- Data Type: {data_features.get('data_type', 'unknown')}
- Structure: {structure}
- Summary: {summary}

Please analyze this data and provide insights relevant to the task.
Consider patterns, trends, anomalies, and relationships within the data.
"""
        return prompt

    def _generate_data_alternatives(self, task: str, data_features: Dict[str, Any]) -> List[AlternativePath]:
        """Generate alternative data analysis approaches."""
        return [
            AlternativePath(
                value="Statistical summary approach",
                confidence=0.7,
                reasoning_steps=["Focused on descriptive statistics and distributions"]
            ),
            AlternativePath(
                value="Pattern recognition approach",
                confidence=0.6,
                reasoning_steps=["Looked for patterns and correlations in the data"]
            ),
            AlternativePath(
                value="Anomaly detection approach",
                confidence=0.5,
                reasoning_steps=["Identified outliers and unusual data points"]
            )
        ]


class AudioAnalysisAgent(ProbabilisticAgent):
    """
    Agent capable of processing and analyzing audio inputs.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio_processor = AudioProcessor()

    async def execute(self, task: str, **kwargs) -> ProbabilisticResult:
        """Execute task with audio analysis capabilities."""
        audio_input = kwargs.get('audio_input')
        if not audio_input:
            return await super().execute(task, **kwargs)

        # Process audio
        audio_features = await self.audio_processor.process(audio_input)

        # Create audio analysis prompt
        analysis_prompt = self._create_audio_analysis_prompt(task, audio_features)

        # Get analysis
        result, confidence = await self.llm.generate_with_confidence(analysis_prompt)

        return ProbabilisticResult(
            value=result,
            confidence=confidence,
            metadata={
                'audio_analysis': True,
                'audio_features': audio_features,
                'analysis_type': 'audio'
            }
        )

    def _create_audio_analysis_prompt(self, task: str, audio_features: Dict[str, Any]) -> str:
        """Create prompt for audio analysis."""
        return f"""
Task: {task}

Audio Context:
- Duration: {audio_features.get('duration_seconds', 'unknown')} seconds
- Sample Rate: {audio_features.get('sample_rate', 'unknown')} Hz
- Channels: {audio_features.get('channels', 'unknown')}
- Size: {audio_features.get('size_bytes', 0)} bytes

Please analyze this audio and provide insights relevant to the task.
Consider content, quality, patterns, and any notable characteristics.
"""
