"""
Comprehensive data validation system for UCUP Framework.

This module provides validation logic, type checking, and data normalization
across all UCUP components to ensure data integrity and prevent runtime errors.
"""

import inspect
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, Callable, Set
from enum import Enum
import re
from pathlib import Path
import json

from .errors import ValidationError, UCUPError, ErrorSeverity

T = TypeVar('T')
ValidationResult = Union[T, ValidationError]

class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    field: str
    message: str
    severity: ValidationSeverity
    value: Any = None
    expected_type: Optional[Type] = None
    suggested_fix: Optional[str] = None

@dataclass
class ValidationReport:
    """Comprehensive validation report."""
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)
    errors: List[ValidationIssue] = field(default_factory=list)
    validated_data: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class DataValidator(ABC):
    """Abstract base class for data validators."""

    def __init__(self, strict: bool = True, logger: Optional[logging.Logger] = None):
        self.strict = strict
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def validate(self, data: Any, context: Optional[Dict[str, Any]] = None) -> ValidationReport:
        """Validate data and return a comprehensive report."""
        pass

    def validate_field(self, field_name: str, value: Any,
                      constraints: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate a single field against constraints."""
        issues = []

        # Type validation
        if 'type' in constraints:
            expected_type = constraints['type']
            if not self._check_type(value, expected_type):
                issues.append(ValidationIssue(
                    field=field_name,
                    message=f"Field '{field_name}' must be of type {expected_type.__name__}",
                    severity=ValidationSeverity.ERROR,
                    value=value,
                    expected_type=expected_type,
                    suggested_fix=f"Convert to {expected_type.__name__}"
                ))

        # Range validation for numeric types
        if isinstance(value, (int, float)):
            if 'min' in constraints and value < constraints['min']:
                issues.append(ValidationIssue(
                    field=field_name,
                    message=f"Field '{field_name}' must be >= {constraints['min']}",
                    severity=ValidationSeverity.ERROR,
                    value=value,
                    suggested_fix=f"Increase value to at least {constraints['min']}"
                ))
            if 'max' in constraints and value > constraints['max']:
                issues.append(ValidationIssue(
                    field=field_name,
                    message=f"Field '{field_name}' must be <= {constraints['max']}",
                    severity=ValidationSeverity.ERROR,
                    value=value,
                    suggested_fix=f"Decrease value to at most {constraints['max']}"
                ))

        # String validation
        if isinstance(value, str):
            if 'min_length' in constraints and len(value) < constraints['min_length']:
                issues.append(ValidationIssue(
                    field=field_name,
                    message=f"Field '{field_name}' must be at least {constraints['min_length']} characters",
                    severity=ValidationSeverity.ERROR,
                    value=value,
                    suggested_fix=f"Add more characters to reach minimum length"
                ))
            if 'max_length' in constraints and len(value) > constraints['max_length']:
                issues.append(ValidationIssue(
                    field=field_name,
                    message=f"Field '{field_name}' must be at most {constraints['max_length']} characters",
                    severity=ValidationSeverity.ERROR,
                    value=value,
                    suggested_fix=f"Truncate or shorten the value"
                ))
            if 'pattern' in constraints and not re.match(constraints['pattern'], value):
                issues.append(ValidationIssue(
                    field=field_name,
                    message=f"Field '{field_name}' does not match required pattern",
                    severity=ValidationSeverity.ERROR,
                    value=value,
                    suggested_fix=f"Ensure value matches pattern: {constraints['pattern']}"
                ))

        # Collection validation
        if isinstance(value, (list, set, tuple)):
            if 'min_items' in constraints and len(value) < constraints['min_items']:
                issues.append(ValidationIssue(
                    field=field_name,
                    message=f"Field '{field_name}' must have at least {constraints['min_items']} items",
                    severity=ValidationSeverity.ERROR,
                    value=value,
                    suggested_fix=f"Add more items to meet minimum requirement"
                ))
            if 'max_items' in constraints and len(value) > constraints['max_items']:
                issues.append(ValidationIssue(
                    field=field_name,
                    message=f"Field '{field_name}' must have at most {constraints['max_items']} items",
                    severity=ValidationSeverity.ERROR,
                    value=value,
                    suggested_fix=f"Remove items to meet maximum limit"
                ))
            if 'item_type' in constraints:
                item_issues = []
                for i, item in enumerate(value):
                    if not self._check_type(item, constraints['item_type']):
                        item_issues.append(ValidationIssue(
                            field=f"{field_name}[{i}]",
                            message=f"Item at index {i} must be of type {constraints['item_type'].__name__}",
                            severity=ValidationSeverity.ERROR,
                            value=item,
                            expected_type=constraints['item_type']
                        ))
                issues.extend(item_issues)

        # Custom validation
        if 'custom_validator' in constraints:
            custom_issues = constraints['custom_validator'](field_name, value)
            if custom_issues:
                issues.extend(custom_issues)

        return issues

    def _check_type(self, value: Any, expected_type: Type) -> bool:
        """Check if value matches expected type."""
        try:
            if inspect.isclass(expected_type):
                return isinstance(value, expected_type)
            elif hasattr(expected_type, '__origin__'):
                # Handle generic types like List[str], Optional[str], etc.
                return self._check_generic_type(value, expected_type)
            else:
                return isinstance(value, expected_type)
        except Exception:
            return False

    def _check_generic_type(self, value: Any, generic_type: Any) -> bool:
        """Check generic types like List[str], Dict[str, int], etc."""
        try:
            origin = getattr(generic_type, '__origin__', None)
            if origin is None:
                return isinstance(value, generic_type)

            args = getattr(generic_type, '__args__', ())

            if origin is Union:
                # Handle Optional[T] which is Union[T, None]
                return any(self._check_type(value, arg) for arg in args)
            elif origin is list:
                if not isinstance(value, list):
                    return False
                if args:
                    return all(self._check_type(item, args[0]) for item in value)
                return True
            elif origin is dict:
                if not isinstance(value, dict):
                    return False
                if len(args) >= 2:
                    return all(
                        self._check_type(k, args[0]) and self._check_type(v, args[1])
                        for k, v in value.items()
                    )
                return True
            elif origin is tuple:
                if not isinstance(value, tuple):
                    return False
                if args and len(value) == len(args):
                    return all(self._check_type(v, arg) for v, arg in zip(value, args))
                return True
            else:
                # Default fallback
                return isinstance(value, origin)
        except Exception:
            return False


class ProbabilisticResultValidator(DataValidator):
    """Validator for ProbabilisticResult objects."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, data: Any, context: Optional[Dict[str, Any]] = None) -> ValidationReport:
        """Validate a ProbabilisticResult or similar structure."""
        issues = []
        warnings = []
        is_valid = True

        if not isinstance(data, dict):
            # Try to extract attributes if it's an object
            try:
                data_dict = {
                    'value': getattr(data, 'value', None),
                    'confidence': getattr(data, 'confidence', None),
                    'alternatives': getattr(data, 'alternatives', []),
                    'metadata': getattr(data, 'metadata', {}),
                    'timestamp': getattr(data, 'timestamp', None)
                }
            except AttributeError:
                issues.append(ValidationIssue(
                    field="root",
                    message="Data must be a dictionary or ProbabilisticResult-like object",
                    severity=ValidationSeverity.CRITICAL,
                    value=data
                ))
                is_valid = False
        else:
            data_dict = data

        # Validate confidence
        confidence = data_dict.get('confidence')
        conf_issues = self.validate_field('confidence', confidence, {
            'type': (int, float),
            'min': 0.0,
            'max': 1.0
        })
        issues.extend(conf_issues)

        # Validate alternatives if present
        alternatives = data_dict.get('alternatives', [])
        if alternatives:
            alt_issues = self.validate_field('alternatives', alternatives, {
                'item_type': dict
            })
            issues.extend(alt_issues)

        # Validate metadata
        metadata = data_dict.get('metadata', {})
        if not isinstance(metadata, dict):
            issues.append(ValidationIssue(
                field="metadata",
                message="Metadata must be a dictionary",
                severity=ValidationSeverity.ERROR,
                value=metadata,
                expected_type=dict
            ))

        # Check for critical issues
        critical_issues = [i for i in issues if i.severity == ValidationSeverity.CRITICAL]
        error_issues = [i for i in issues if i.severity == ValidationSeverity.ERROR]

        if critical_issues or error_issues:
            is_valid = False

        return ValidationReport(
            is_valid=is_valid,
            issues=issues,
            warnings=warnings,
            errors=error_issues,
            validated_data=data_dict if is_valid else None,
            metadata={'validator_type': 'probabilistic_result'}
        )


class AgentConfigurationValidator(DataValidator):
    """Validator for agent configuration data."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_fields = {
            'type', 'config', 'capabilities'
        }

    def validate(self, data: Any, context: Optional[Dict[str, Any]] = None) -> ValidationReport:
        """Validate agent configuration."""
        issues = []
        warnings = []
        is_valid = True

        if not isinstance(data, dict):
            issues.append(ValidationIssue(
                field="root",
                message="Agent configuration must be a dictionary",
                severity=ValidationSeverity.CRITICAL,
                value=data,
                expected_type=dict
            ))
            is_valid = False
        else:
            # Check required fields
            for required_field in self.required_fields:
                if required_field not in data:
                    issues.append(ValidationIssue(
                        field=required_field,
                        message=f"Required field '{required_field}' is missing",
                        severity=ValidationSeverity.ERROR,
                        suggested_fix=f"Add '{required_field}' field to configuration"
                    ))

            # Validate agent type
            agent_type = data.get('type')
            if agent_type:
                type_issues = self.validate_field('type', agent_type, {
                    'type': str,
                    'custom_validator': self._validate_agent_type
                })
                issues.extend(type_issues)

            # Validate configuration section
            config = data.get('config', {})
            if config:
                config_issues = self._validate_config_section(config)
                issues.extend(config_issues)

            # Validate capabilities
            capabilities = data.get('capabilities', [])
            cap_issues = self.validate_field('capabilities', capabilities, {
                'item_type': str
            })
            issues.extend(cap_issues)

        error_issues = [i for i in issues if i.severity in (ValidationSeverity.ERROR, ValidationSeverity.CRITICAL)]
        if error_issues:
            is_valid = False

        return ValidationReport(
            is_valid=is_valid,
            issues=issues,
            warnings=warnings,
            errors=error_issues,
            validated_data=data if is_valid else None,
            metadata={'validator_type': 'agent_configuration'}
        )

    def _validate_agent_type(self, field_name: str, value: str) -> List[ValidationIssue]:
        """Validate agent type string."""
        issues = []

        # Check for plugin reference
        if value.startswith('!plugin:'):
            # Plugin reference validation would be more complex
            pass
        else:
            # Built-in agent types
            valid_types = {'ProbabilisticAgent', 'BayesianAgent', 'MDPAgent', 'MCTSReasoner'}
            if value not in valid_types:
                issues.append(ValidationIssue(
                    field=field_name,
                    message=f"Unknown agent type '{value}'. Valid types: {valid_types}",
                    severity=ValidationSeverity.ERROR,
                    value=value,
                    suggested_fix=f"Use one of: {', '.join(valid_types)}"
                ))

        return issues

    def _validate_config_section(self, config: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate agent configuration section."""
        issues = []

        # Check for LLM configuration if not plugin
        if not config.get('type', '').startswith('!plugin'):
            if 'llm' not in config:
                issues.append(ValidationIssue(
                    field="config.llm",
                    message="Non-plugin agents require LLM configuration",
                    severity=ValidationSeverity.ERROR,
                    suggested_fix="Add 'llm' field to config section"
                ))

        return issues


class CoordinationConfigurationValidator(DataValidator):
    """Validator for coordination configuration."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, data: Any, context: Optional[Dict[str, Any]] = None) -> ValidationReport:
        """Validate coordination configuration."""
        issues = []
        warnings = []
        is_valid = True

        if not isinstance(data, dict):
            issues.append(ValidationIssue(
                field="root",
                message="Coordination configuration must be a dictionary",
                severity=ValidationSeverity.CRITICAL,
                value=data,
                expected_type=dict
            ))
            is_valid = False
        else:
            # Validate coordination type
            coord_type = data.get('type')
            if not coord_type:
                issues.append(ValidationIssue(
                    field="type",
                    message="Coordination type is required",
                    severity=ValidationSeverity.ERROR,
                    suggested_fix="Add 'type' field (hierarchical, debate, market, swarm)"
                ))
            else:
                type_issues = self._validate_coordination_type(coord_type, data)
                issues.extend(type_issues)

            # Validate agents references
            if 'agents' in data:
                agent_issues = self.validate_field('agents', data['agents'], {
                    'item_type': str,
                    'custom_validator': self._validate_agent_references
                })
                issues.extend(agent_issues)

        error_issues = [i for i in issues if i.severity in (ValidationSeverity.ERROR, ValidationSeverity.CRITICAL)]
        if error_issues:
            is_valid = False

        return ValidationReport(
            is_valid=is_valid,
            issues=issues,
            warnings=warnings,
            errors=error_issues,
            validated_data=data if is_valid else None,
            metadata={'validator_type': 'coordination_configuration'}
        )

    def _validate_coordination_type(self, coord_type: str, config: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate coordination type and required fields."""
        issues = []
        valid_types = {'hierarchical', 'debate', 'market', 'swarm'}

        if coord_type not in valid_types:
            issues.append(ValidationIssue(
                field="type",
                message=f"Unknown coordination type '{coord_type}'. Valid types: {valid_types}",
                severity=ValidationSeverity.ERROR,
                value=coord_type,
                suggested_fix=f"Use one of: {', '.join(valid_types)}"
            ))
            return issues

        # Type-specific validation
        if coord_type == 'hierarchical':
            required_fields = ['manager', 'workers']
            for field in required_fields:
                if field not in config:
                    issues.append(ValidationIssue(
                        field=field,
                        message=f"Hierarchical coordination requires '{field}' field",
                        severity=ValidationSeverity.ERROR,
                        suggested_fix=f"Add '{field}' field to configuration"
                    ))

        elif coord_type == 'debate':
            if 'agents' not in config:
                issues.append(ValidationIssue(
                    field="agents",
                    message="Debate coordination requires 'agents' field",
                    severity=ValidationSeverity.ERROR,
                    suggested_fix="Add 'agents' field with list of agent references"
                ))

        return issues

    def _validate_agent_references(self, field_name: str, agents: List[str]) -> List[ValidationIssue]:
        """Validate agent references."""
        issues = []

        for i, agent_ref in enumerate(agents):
            if not isinstance(agent_ref, str):
                issues.append(ValidationIssue(
                    field=f"{field_name}[{i}]",
                    message="Agent references must be strings",
                    severity=ValidationSeverity.ERROR,
                    value=agent_ref,
                    expected_type=str
                ))
            elif not agent_ref.startswith('!ref:agents.'):
                issues.append(ValidationIssue(
                    field=f"{field_name}[{i}]",
                    message="Agent references should be in format '!ref:agents.<agent_name>'",
                    severity=ValidationSeverity.WARNING,
                    value=agent_ref,
                    suggested_fix="Use proper agent reference format"
                ))

        return issues


class PluginConfigurationValidator(DataValidator):
    """Validator for plugin configuration."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, data: Any, context: Optional[Dict[str, Any]] = None) -> ValidationReport:
        """Validate plugin configuration."""
        issues = []
        warnings = []
        is_valid = True

        if not isinstance(data, dict):
            issues.append(ValidationIssue(
                field="root",
                message="Plugin configuration must be a dictionary",
                severity=ValidationSeverity.CRITICAL,
                value=data,
                expected_type=dict
            ))
            is_valid = False
        else:
            # Validate plugin metadata if present
            if 'metadata' in data:
                metadata_issues = self._validate_plugin_metadata(data['metadata'])
                issues.extend(metadata_issues)

            # Validate plugin-specific config
            config = data.get('config', {})
            config_issues = self._validate_plugin_config(config)
            issues.extend(config_issues)

        error_issues = [i for i in issues if i.severity in (ValidationSeverity.ERROR, ValidationSeverity.CRITICAL)]
        if error_issues:
            is_valid = False

        return ValidationReport(
            is_valid=is_valid,
            issues=issues,
            warnings=warnings,
            errors=error_issues,
            validated_data=data if is_valid else None,
            metadata={'validator_type': 'plugin_configuration'}
        )

    def _validate_plugin_metadata(self, metadata: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate plugin metadata."""
        issues = []

        required_fields = ['name', 'version']
        for field in required_fields:
            if field not in metadata:
                issues.append(ValidationIssue(
                    field=f"metadata.{field}",
                    message=f"Plugin metadata missing required field '{field}'",
                    severity=ValidationSeverity.ERROR,
                    suggested_fix=f"Add '{field}' field to plugin metadata"
                ))

        # Validate version format
        if 'version' in metadata:
            version = metadata['version']
            if not isinstance(version, str) or not re.match(r'^\d+\.\d+\.\d+$', version):
                issues.append(ValidationIssue(
                    field="metadata.version",
                    message="Plugin version must be in semantic versioning format (x.y.z)",
                    severity=ValidationSeverity.ERROR,
                    value=version,
                    suggested_fix="Use semantic versioning format like '1.0.0'"
                ))

        return issues

    def _validate_plugin_config(self, config: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate plugin-specific configuration."""
        # For now, just ensure it's a dictionary
        issues = []

        if not isinstance(config, dict):
            issues.append(ValidationIssue(
                field="config",
                message="Plugin config must be a dictionary",
                severity=ValidationSeverity.ERROR,
                value=config,
                expected_type=dict
            ))

        return issues


class UCUPValidator:
    """Main validation orchestrator for UCUP components."""

    def __init__(self, strict: bool = True):
        self.strict = strict
        self.logger = logging.getLogger(__name__)
        self.validators = {
            'probabilistic_result': ProbabilisticResultValidator(strict=strict),
            'agent_config': AgentConfigurationValidator(strict=strict),
            'coordination_config': CoordinationConfigurationValidator(strict=strict),
            'plugin_config': PluginConfigurationValidator(strict=strict)
        }

    def validate(self, data_type: str, data: Any,
                context: Optional[Dict[str, Any]] = None) -> ValidationReport:
        """Validate data of a specific type."""
        validator = self.validators.get(data_type)
        if not validator:
            return ValidationReport(
                is_valid=False,
                issues=[ValidationIssue(
                    field="data_type",
                    message=f"Unknown validation type '{data_type}'",
                    severity=ValidationSeverity.CRITICAL,
                    value=data_type
                )]
            )

        return validator.validate(data, context)

    def validate_config(self, config: Dict[str, Any]) -> ValidationReport:
        """Validate complete UCUP configuration."""
        issues = []
        warnings = []
        is_valid = True

        # Validate version
        if 'version' not in config:
            issues.append(ValidationIssue(
                field="version",
                message="Configuration missing required 'version' field",
                severity=ValidationSeverity.ERROR,
                suggested_fix="Add 'version' field to configuration"
            ))

        # Validate agents section
        if 'agents' in config:
            agents_config = config['agents']
            for agent_name, agent_data in agents_config.items():
                agent_report = self.validate('agent_config', agent_data)
                if not agent_report.is_valid:
                    issues.extend([
                        ValidationIssue(
                            field=f"agents.{agent_name}.{issue.field}",
                            message=issue.message,
                            severity=issue.severity,
                            value=issue.value,
                            suggested_fix=issue.suggested_fix
                        ) for issue in agent_report.issues
                    ])

        # Validate coordination section
        if 'coordination' in config:
            coord_report = self.validate('coordination_config', config['coordination'])
            if not coord_report.is_valid:
                issues.extend([
                    ValidationIssue(
                        field=f"coordination.{issue.field}",
                        message=issue.message,
                        severity=issue.severity,
                        value=issue.value,
                        suggested_fix=issue.suggested_fix
                    ) for issue in coord_report.issues
                ])

        # Validate plugins section
        if 'plugins' in config:
            plugins_config = config['plugins']
            for plugin_name, plugin_data in plugins_config.items():
                plugin_report = self.validate('plugin_config', plugin_data)
                if not plugin_report.is_valid:
                    issues.extend([
                        ValidationIssue(
                            field=f"plugins.{plugin_name}.{issue.field}",
                            message=issue.message,
                            severity=issue.severity,
                            value=issue.value,
                            suggested_fix=issue.suggested_fix
                        ) for issue in plugin_report.issues
                    ])

        error_issues = [i for i in issues if i.severity in (ValidationSeverity.ERROR, ValidationSeverity.CRITICAL)]
        if error_issues:
            is_valid = False

        return ValidationReport(
            is_valid=is_valid,
            issues=issues,
            warnings=warnings,
            errors=error_issues,
            validated_data=config if is_valid else None,
            metadata={'validator_type': 'ucup_configuration'}
        )


# Global validator instance
_ucup_validator = None

def get_ucup_validator() -> UCUPValidator:
    """Get the global UCUP validator instance."""
    global _ucup_validator
    if _ucup_validator is None:
        _ucup_validator = UCUPValidator()
    return _ucup_validator

def validate_data(data_type: str, data: Any, context: Optional[Dict[str, Any]] = None) -> ValidationReport:
    """Convenience function to validate data."""
    return get_ucup_validator().validate(data_type, data, context)
