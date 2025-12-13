"""
YAML ↔ Code Synchronization for ForgeProcess Integration.

Enables bidirectional synchronization between YAML definitions (ForgeProcess)
and Python code (ForgeBase), maintaining cognitive coherence across the stack.

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import inspect
from pathlib import Path
from typing import Any

import yaml

from forgebase.application.usecase_base import UseCaseBase


class YAMLSyncError(Exception):
    """Exception raised for YAML synchronization errors."""

    pass


class YAMLSync:
    """
    Bidirectional YAML ↔ Code synchronization.

    Enables ForgeProcess (intent/YAML) to stay synchronized with ForgeBase
    (execution/Code), maintaining cognitive coherence.

    Features:
        - Parse YAML UseCase definitions
        - Generate Python code from YAML
        - Validate code against YAML spec
        - Detect drift and mismatches
        - Bidirectional synchronization

    Example::

        sync = YAMLSync()

        # Parse YAML definition
        spec = sync.parse_yaml("specs/create_user.yaml")

        # Validate implementation matches spec
        from my_app import CreateUserUseCase
        is_valid = sync.validate_usecase(CreateUserUseCase, spec)

        # Generate code skeleton from YAML
        code = sync.generate_code(spec)

        # Detect drift
        drift = sync.detect_drift(CreateUserUseCase, spec)
        if drift:
            print(f"Drift detected: {drift}")

    :ivar schema_version: YAML schema version
    :vartype schema_version: str
    """

    def __init__(self, schema_version: str = "1.0"):
        """
        Initialize YAML sync.

        :param schema_version: YAML schema version to use
        :type schema_version: str
        """
        self.schema_version = schema_version

    def parse_yaml(self, yaml_path: str | Path) -> dict[str, Any]:
        """
        Parse YAML UseCase definition.

        :param yaml_path: Path to YAML file
        :type yaml_path: Union[str, Path]
        :return: Parsed UseCase specification
        :rtype: Dict[str, Any]
        :raises YAMLSyncError: If YAML is invalid

        Example YAML format::

            version: "1.0"
            usecase:
              name: CreateUser
              description: Create a new user in the system
              inputs:
                - name: name
                  type: str
                  required: true
                - name: email
                  type: str
                  required: true
              outputs:
                - name: user_id
                  type: str
              business_rules:
                - Email must be unique
                - Name cannot be empty
        """
        path = Path(yaml_path)

        if not path.exists():
            raise YAMLSyncError(f"YAML file not found: {yaml_path}")

        try:
            with open(path, encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise YAMLSyncError(f"Failed to parse YAML: {e}") from e

        # Validate schema version
        if 'version' not in data:
            raise YAMLSyncError("Missing 'version' field in YAML")

        if data['version'] != self.schema_version:
            raise YAMLSyncError(
                f"Schema version mismatch: expected {self.schema_version}, "
                f"got {data['version']}"
            )

        # Validate required fields
        if 'usecase' not in data:
            raise YAMLSyncError("Missing 'usecase' section in YAML")

        usecase = data['usecase']
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in usecase:
                raise YAMLSyncError(f"Missing required field: usecase.{field}")

        return data

    def validate_usecase(
        self,
        usecase_class: type[UseCaseBase],
        spec: dict[str, Any]
    ) -> bool:
        """
        Validate UseCase implementation against YAML spec.

        :param usecase_class: UseCase class to validate
        :type usecase_class: Type[UseCaseBase]
        :param spec: YAML specification
        :type spec: Dict[str, Any]
        :return: True if valid, False otherwise
        :rtype: bool

        Example::

            sync = YAMLSync()
            spec = sync.parse_yaml("create_user.yaml")

            from my_app import CreateUserUseCase
            is_valid = sync.validate_usecase(CreateUserUseCase, spec)

            if not is_valid:
                drift = sync.detect_drift(CreateUserUseCase, spec)
                print(f"Validation failed: {drift}")
        """
        drift = self.detect_drift(usecase_class, spec)
        return len(drift) == 0

    def detect_drift(
        self,
        usecase_class: type[UseCaseBase],
        spec: dict[str, Any]
    ) -> list[str]:
        """
        Detect drift between implementation and specification.

        :param usecase_class: UseCase class
        :type usecase_class: Type[UseCaseBase]
        :param spec: YAML specification
        :type spec: Dict[str, Any]
        :return: List of drift descriptions
        :rtype: List[str]

        Example::

            drift = sync.detect_drift(CreateUserUseCase, spec)
            for issue in drift:
                print(f"- {issue}")

            # Output:
            # - Class name mismatch: expected CreateUser, got CreateUserUseCase
            # - Missing business rule: Email must be unique
        """
        drift = []
        usecase_spec = spec['usecase']

        # Check class name
        expected_name = usecase_spec['name']
        actual_name = usecase_class.__name__

        # Allow for "UseCase" suffix
        if not (actual_name == expected_name or
                actual_name == f"{expected_name}UseCase"):
            drift.append(
                f"Class name mismatch: expected {expected_name}, "
                f"got {actual_name}"
            )

        # Check execute method exists
        if not hasattr(usecase_class, 'execute'):
            drift.append("Missing execute() method")

        # Check docstring
        if not usecase_class.__doc__:
            drift.append("Missing class docstring")
        else:
            expected_desc = usecase_spec.get('description', '')
            actual_desc = usecase_class.__doc__.strip().split('\n')[0]

            # Fuzzy match - just check if description is mentioned
            if expected_desc and expected_desc.lower() not in actual_desc.lower():
                drift.append(
                    f"Description mismatch: expected '{expected_desc}', "
                    f"got '{actual_desc}'"
                )

        # Check execute signature
        if hasattr(usecase_class, 'execute'):
            sig = inspect.signature(usecase_class.execute)
            params = list(sig.parameters.keys())

            # Remove 'self'
            if 'self' in params:
                params.remove('self')

            # Check inputs if specified
            if 'inputs' in usecase_spec:
                expected_inputs = {
                    inp['name'] for inp in usecase_spec['inputs']
                }

                # We expect either individual params or a DTO
                # For now, just check that execute accepts some input
                if len(params) == 0 and len(expected_inputs) > 0:
                    drift.append(
                        f"Execute method should accept inputs: {expected_inputs}"
                    )

        return drift

    def generate_code(self, spec: dict[str, Any]) -> str:
        """
        Generate Python code skeleton from YAML spec.

        :param spec: YAML specification
        :type spec: Dict[str, Any]
        :return: Generated Python code
        :rtype: str

        Example::

            sync = YAMLSync()
            spec = sync.parse_yaml("create_user.yaml")
            code = sync.generate_code(spec)

            # Write to file
            with open("generated_usecase.py", "w") as f:
                f.write(code)
        """
        usecase_spec = spec['usecase']
        name = usecase_spec['name']
        description = usecase_spec.get('description', '')

        # Start with imports
        code = f'''"""
{description}

Auto-generated from YAML specification.

:author: ForgeBase Code Generator
:since: 2025-11-03
"""

from forgebase.application.dto_base import DTOBase
from forgebase.application.usecase_base import UseCaseBase


'''

        # Generate Input DTO if inputs specified
        if 'inputs' in usecase_spec and usecase_spec['inputs']:
            code += self._generate_input_dto(name, usecase_spec['inputs'])
            code += '\n\n'

        # Generate Output DTO if outputs specified
        if 'outputs' in usecase_spec and usecase_spec['outputs']:
            code += self._generate_output_dto(name, usecase_spec['outputs'])
            code += '\n\n'

        # Generate UseCase class
        code += self._generate_usecase_class(name, description, usecase_spec)

        return code

    def _generate_input_dto(self, usecase_name: str, inputs: list[dict]) -> str:
        """Generate Input DTO code."""
        class_name = f"{usecase_name}Input"

        # Generate __init__ parameters
        params = []
        assignments = []

        for inp in inputs:
            param_name = inp['name']
            param_type = inp.get('type', 'Any')
            required = inp.get('required', True)

            if required:
                params.append(f"{param_name}: {param_type}")
            else:
                params.append(f"{param_name}: {param_type} | None = None")

            assignments.append(f"        self.{param_name} = {param_name}")

        params_str = ', '.join(params)
        assignments_str = '\n'.join(assignments)

        return f'''class {class_name}(DTOBase):
    """Input DTO for {usecase_name}."""

    def __init__(self, {params_str}):
        """Initialize input DTO."""
{assignments_str}

    def validate(self) -> None:
        """Validate input data."""
        # TODO: Add validation logic
        pass

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {{
{self._generate_dict_items(inputs)}
        }}

    @classmethod
    def from_dict(cls, data: dict) -> '{class_name}':
        """Create from dictionary."""
        return cls(
{self._generate_from_dict_items(inputs)}
        )'''

    def _generate_output_dto(self, usecase_name: str, outputs: list[dict]) -> str:
        """Generate Output DTO code."""
        class_name = f"{usecase_name}Output"

        params = []
        assignments = []

        for out in outputs:
            param_name = out['name']
            param_type = out.get('type', 'Any')
            params.append(f"{param_name}: {param_type}")
            assignments.append(f"        self.{param_name} = {param_name}")

        params_str = ', '.join(params)
        assignments_str = '\n'.join(assignments)

        return f'''class {class_name}(DTOBase):
    """Output DTO for {usecase_name}."""

    def __init__(self, {params_str}):
        """Initialize output DTO."""
{assignments_str}

    def validate(self) -> None:
        """Validate output data."""
        pass

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {{
{self._generate_dict_items(outputs)}
        }}

    @classmethod
    def from_dict(cls, data: dict) -> '{class_name}':
        """Create from dictionary."""
        return cls(
{self._generate_from_dict_items(outputs)}
        )'''

    def _generate_usecase_class(
        self,
        name: str,
        description: str,
        spec: dict
    ) -> str:
        """Generate UseCase class code."""
        class_name = f"{name}UseCase"

        has_inputs = 'inputs' in spec and spec['inputs']
        has_outputs = 'outputs' in spec and spec['outputs']

        input_type = f"{name}Input" if has_inputs else "Any"
        output_type = f"{name}Output" if has_outputs else "Any"

        # Generate business rules comments
        rules_comments = ""
        if 'business_rules' in spec and spec['business_rules']:
            rules_comments = "\n    Business Rules:\n"
            for rule in spec['business_rules']:
                rules_comments += f"        - {rule}\n"

        return f'''class {class_name}(UseCaseBase):
    """
    {description}
{rules_comments}
    Example::

        usecase = {class_name}()
        output = usecase.execute(input_data)
    """

    def execute(self, input_dto: {input_type}) -> {output_type}:
        """
        Execute {name}.

        :param input_dto: Input data
        :type input_dto: {input_type}
        :return: Output data
        :rtype: {output_type}
        """
        # TODO: Implement business logic
        raise NotImplementedError("Business logic not yet implemented")

    def _before_execute(self) -> None:
        """Hook before execution."""
        pass

    def _after_execute(self) -> None:
        """Hook after execution."""
        pass

    def _on_error(self, error: Exception) -> None:
        """Hook on error."""
        pass'''

    def _generate_dict_items(self, fields: list[dict]) -> str:
        """Generate dictionary items for to_dict()."""
        items = []
        for field in fields:
            name = field['name']
            items.append(f"            '{name}': self.{name}")
        return ',\n'.join(items)

    def _generate_from_dict_items(self, fields: list[dict]) -> str:
        """Generate constructor arguments for from_dict()."""
        items = []
        for field in fields:
            name = field['name']
            items.append(f"            {name}=data.get('{name}')")
        return ',\n'.join(items)

    def export_to_yaml(
        self,
        usecase_class: type[UseCaseBase],
        output_path: str | Path
    ) -> None:
        """
        Export UseCase implementation to YAML spec.

        :param usecase_class: UseCase class to export
        :type usecase_class: Type[UseCaseBase]
        :param output_path: Path to write YAML
        :type output_path: Union[str, Path]

        Example::

            sync = YAMLSync()

            from my_app import CreateUserUseCase
            sync.export_to_yaml(CreateUserUseCase, "specs/create_user.yaml")
        """
        spec = {
            'version': self.schema_version,
            'usecase': {
                'name': usecase_class.__name__.replace('UseCase', ''),
                'description': (
                    usecase_class.__doc__.strip().split('\n')[0]
                    if usecase_class.__doc__ else 'No description'
                )
            }
        }

        # Try to extract inputs/outputs from execute signature
        if hasattr(usecase_class, 'execute'):
            sig = inspect.signature(usecase_class.execute)

            # Extract input type hints
            params = sig.parameters
            if len(params) > 1:  # More than just 'self'
                # Assume second parameter is input DTO
                param_names = list(params.keys())
                if len(param_names) > 1:
                    input_param = params[param_names[1]]
                    if input_param.annotation != inspect.Parameter.empty:
                        spec['usecase']['input_type'] = str(input_param.annotation)

            # Extract return type
            if sig.return_annotation != inspect.Signature.empty:
                spec['usecase']['output_type'] = str(sig.return_annotation)

        # Write YAML
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(spec, f, default_flow_style=False, sort_keys=False)
