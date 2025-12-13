"""
Component Discovery API for AI Agents.

Scans codebase and catalogs ForgeBase components for programmatic analysis.

Usage:
    from forgebase.dev.api import ComponentDiscovery

    discovery = ComponentDiscovery()
    result = discovery.scan_project()

    # AI can analyze architecture
    print(f"Found {len(result.usecases)} use cases")
    print(f"Found {len(result.entities)} entities")

    # Check for orphaned components
    if result.repositories and not result.usecases:
        suggest_creating_usecases()

Author: ForgeBase Development Team
Created: 2025-11-04
"""

import ast
import importlib
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ComponentInfo:
    """Information about a discovered component."""

    name: str
    type: str  # 'entity', 'usecase', 'port', 'repository', etc.
    file_path: str
    line_number: int = 0
    base_class: str = ""
    imports: list[str] = field(default_factory=list)
    docstring: str = ""


@dataclass
class DiscoveryResult:
    """
    Result from component discovery.

    Attributes:
        entities: List of discovered entities
        usecases: List of discovered use cases
        repositories: List of discovered repositories
        ports: List of discovered ports
        value_objects: List of discovered value objects
        adapters: List of discovered adapters
        total_files_scanned: Number of files scanned
        scan_duration: Time taken for scan in seconds
    """

    entities: list[ComponentInfo] = field(default_factory=list)
    usecases: list[ComponentInfo] = field(default_factory=list)
    repositories: list[ComponentInfo] = field(default_factory=list)
    ports: list[ComponentInfo] = field(default_factory=list)
    value_objects: list[ComponentInfo] = field(default_factory=list)
    adapters: list[ComponentInfo] = field(default_factory=list)
    total_files_scanned: int = 0
    scan_duration: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "entities": [c.__dict__ for c in self.entities],
            "usecases": [c.__dict__ for c in self.usecases],
            "repositories": [c.__dict__ for c in self.repositories],
            "ports": [c.__dict__ for c in self.ports],
            "value_objects": [c.__dict__ for c in self.value_objects],
            "adapters": [c.__dict__ for c in self.adapters],
            "total_files_scanned": self.total_files_scanned,
            "scan_duration": self.scan_duration,
        }

    @property
    def total_components(self) -> int:
        """Total number of components found."""
        return (
            len(self.entities)
            + len(self.usecases)
            + len(self.repositories)
            + len(self.ports)
            + len(self.value_objects)
            + len(self.adapters)
        )


class ComponentDiscovery:
    """
    Component discovery API for AI agents.

    Scans ForgeBase projects and catalogs components with:
    - Type detection (Entity, UseCase, Repository, etc.)
    - Base class information
    - Location (file, line number)
    - Dependencies
    - Docstrings

    Example:
        discovery = ComponentDiscovery()
        result = discovery.scan_project()

        # AI analyzes architecture
        if len(result.usecases) < len(result.entities):
            print("Consider creating more UseCases")

        # Find unused components
        for entity in result.entities:
            if not any(entity.name in uc.imports for uc in result.usecases):
                print(f"Entity {entity.name} not used in any UseCase")
    """

    def __init__(
        self,
        project_root: Path | None = None,
        src_dir: Path | None = None,
        package_name: str | None = None,
    ) -> None:
        """
        Initialize component discovery.

        Args:
            project_root: Project root directory. Defaults to current directory.
                Used when scanning a source tree (e.g. a cloned repo).
            src_dir: Optional explicit source directory to scan. If not
                provided, defaults to ``project_root / "src" / "forgebase"``
                when ``package_name`` is not set.
            package_name: Optional installed package name to scan. When
                provided, the discovery will resolve the package location via
                ``importlib`` and scan only that package directory. This is
                the recommended mode for apps that depend on ForgeBase and
                want to expose their own discovery API for agents.
        """
        if package_name is not None:
            pkg = importlib.import_module(package_name)
            package_path = Path(pkg.__file__).resolve().parent
            self.project_root = package_path
            self.src_dir = src_dir or package_path
        else:
            self.project_root = project_root or Path.cwd()
            self.src_dir = src_dir or (self.project_root / "src" / "forgebase")

    def scan_project(self) -> DiscoveryResult:
        """
        Scan project for ForgeBase components.

        Returns:
            DiscoveryResult with all discovered components

        Example:
            result = discovery.scan_project()
            for usecase in result.usecases:
                print(f"{usecase.name} in {usecase.file_path}")
        """
        import time

        start_time = time.time()

        result = DiscoveryResult()

        # Scan Python files
        if self.src_dir.exists():
            python_files = list(self.src_dir.rglob("*.py"))
            result.total_files_scanned = len(python_files)

            for py_file in python_files:
                self._scan_file(py_file, result)

        result.scan_duration = time.time() - start_time

        return result

    def run_legacy_discover(self, args: list[str] | None = None) -> dict[str, Any]:
        """
        Run legacy discover.py script.

        For backwards compatibility.

        Args:
            args: Command line arguments

        Returns:
            Dictionary with execution result
        """
        try:
            result = subprocess.run(
                [sys.executable, "scripts/discover.py"] + (args or []),
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        except FileNotFoundError:
            return {"success": False, "error": "discover.py not found in scripts/"}

    def _scan_file(self, file_path: Path, result: DiscoveryResult) -> None:
        """Scan a single Python file for components."""
        try:
            with open(file_path, encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    component = self._analyze_class(node, file_path)
                    if component:
                        self._categorize_component(component, result)

        except (SyntaxError, UnicodeDecodeError):
            pass  # Skip files with syntax errors

    def _analyze_class(self, node: ast.ClassDef, file_path: Path) -> ComponentInfo | None:
        """Analyze a class definition."""
        # Get base classes
        base_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_classes.append(base.attr)

        if not base_classes:
            return None

        # Get docstring
        docstring = ast.get_docstring(node) or ""

        # Determine relative path
        try:
            rel_path = file_path.relative_to(self.project_root)
        except ValueError:
            rel_path = file_path

        return ComponentInfo(
            name=node.name,
            type="unknown",
            file_path=str(rel_path),
            line_number=node.lineno,
            base_class=base_classes[0] if base_classes else "",
            docstring=docstring.split("\n")[0] if docstring else "",
        )

    def _categorize_component(self, component: ComponentInfo, result: DiscoveryResult) -> None:
        """Categorize component by base class."""
        base = component.base_class

        if base == "EntityBase" or "Entity" in component.name:
            component.type = "entity"
            result.entities.append(component)
        elif base == "UseCaseBase" or "UseCase" in component.name:
            component.type = "usecase"
            result.usecases.append(component)
        elif base == "RepositoryBase" or "Repository" in component.name:
            component.type = "repository"
            result.repositories.append(component)
        elif base == "PortBase" or "Port" in component.name:
            component.type = "port"
            result.ports.append(component)
        elif base == "ValueObjectBase" or "ValueObject" in component.name:
            component.type = "value_object"
            result.value_objects.append(component)
        elif "Adapter" in component.name:
            component.type = "adapter"
            result.adapters.append(component)
