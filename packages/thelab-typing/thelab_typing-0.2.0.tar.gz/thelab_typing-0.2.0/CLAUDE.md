# thelab-typing Development Style Guide

## Overview

This guide defines the coding standards, practices, and philosophies used by the thelab-typing project. Follow these guidelines to maintain consistency with the existing codebase.

## Core Philosophy

### Type Safety First

- **Strict typing is non-negotiable**. Every function, method, and variable must be properly typed
- Use the most restrictive mypy settings possible
- Prefer explicit types over `Any` or untyped code
- Leverage advanced typing features: `TypeIs`, `TypeGuard`, generics, and type aliases

### Modern Python Only

- Target Python 3.13+ exclusively
- Use modern generic syntax (`[T]` instead of `TypeVar`)
- Adopt new language features immediately when available
- No backward compatibility concerns with older Python versions

### Quality Over Speed

- 100% test coverage is expected, not optional
- Code must pass all linting, formatting, and type checking
- Comprehensive testing including edge cases and error conditions
- Professional-grade documentation and commit messages

## Code Style

### Formatting & Structure

```python
# Use modern generic syntax
class ListOf[T](pydantic.RootModel[list[T]]):
    """
    Always include docstrings for classes and complex functions.
    """

    def method[R](self, param: T) -> R:
        # 4-space indentation always
        # Max line length: 160 characters
        return result
```

### Type Annotations

```python
# Full type annotations required
def validate[**P, R: HttpResponse, _QST: pydantic.BaseModel](
) -> Callable[[Callable[P, R]], Callable[P, R | APIResponse]]:
    """Complex generics are preferred over Any"""
    pass

# Use Result types for error handling
@as_result(ValueError, TypeError)
def risky_operation(data: str) -> ProcessedData:
    """Convert exceptions to Result types"""
    pass
```

### Import Style

```python
# Group imports: stdlib, third-party, local
from collections.abc import Callable, Iterator
from typing import TypeIs, get_args

import pydantic
import django

from ..result import Result, Ok, Err
from .serializers import Empty
```

## Architecture Patterns

### Functional Programming Influence

- Implement `Result[T, E]` types instead of raising exceptions
- Use monadic patterns with `and_then()`, `do()` notation
- Prefer immutable data structures where possible
- Type-driven design with heavy use of generics

### Django Integration

```python
# Type-safe Django views with validation
def validate[**P, R: HttpResponse]() -> Callable[...]:
    """Decorator that infers types from function signatures"""

def view_function(
    request: TypedRequest[QueryModel, BodyModel, User],
    *args,
    **kwargs
) -> HttpResponse:
    """Request type determines validation automatically"""
```

### Pydantic Integration

```python
# Extend Pydantic with typed collections
class ListOf[T](pydantic.RootModel[list[T]]):
    """Type-safe list wrapper with full sequence protocol"""

class DictOf[K, V](pydantic.RootModel[dict[K, V]]):
    """Type-safe dict wrapper with full mapping protocol"""
```

## Testing Standards

### Test Structure

```python
class TestClassName(TestCase):
    def setUp(self) -> None:
        """Type all test methods"""
        self.data = ModelClass.model_validate(test_data)

    def test_specific_behavior(self) -> None:
        """Descriptive test names, comprehensive assertions"""
        result = function_under_test(self.data)
        self.assertIsInstance(result, ExpectedType)
        self.assertEqual(result.property, expected_value)
```

### Coverage Requirements

- 100% line and branch coverage
- Test all error paths and edge cases
- Include sample applications for integration testing
- Test type validation and error handling thoroughly

## Configuration Standards

### mypy Configuration

```toml
[tool.mypy]
python_version = "3.13"
# Enable ALL strict mode flags
warn_unused_configs = true
disallow_subclassing_any = true
disallow_any_generics = true
disallow_untyped_calls = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_return_any = true
no_implicit_reexport = true
strict_equality = true
show_error_codes = true
```

### Development Tools

- **Formatter**: Ruff (not black)
- **Linter**: Ruff (not flake8)
- **Type Checker**: mypy with strict mode
- **Import Sorting**: isort with "from_first" profile
- **Pre-commit**: All quality checks must pass

### Dependencies

```toml
[project]
requires-python = ">=3.13"
dependencies = [
    "pydantic (>=2.11.3,<3.0.0)"  # Pin major versions
]

[project.optional-dependencies]
django = ["django (>=4.2,<5.3)"]  # Support multiple versions
drf = ["djangorestframework (>=3.16.0)"]
```

## Git & Release Practices

### Commit Messages

- Use conventional commits: `feat:`, `fix:`, `refactor:`
- Be descriptive but concise
- Reference issue numbers when applicable
- Use commitizen for consistency

### Branch Strategy

- Work on feature branches
- Merge to `master` via merge requests
- Automated dependency updates via Renovate
- Semantic versioning with automated changelogs

### CI/CD Requirements

- All tests must pass across supported Django versions
- Type checking with mypy must succeed
- Linting and formatting must be clean
- Coverage reports must meet 100% threshold

## Error Handling Philosophy

### Prefer Result Types Over Exceptions

```python
# Instead of raising exceptions
def parse_data(raw: str) -> ProcessedData:
    if not raw:
        raise ValueError("Empty input")
    return process(raw)

# Use Result types
@as_result(ValueError, TypeError)
def parse_data(raw: str) -> ProcessedData:
    if not raw:
        raise ValueError("Empty input")
    return process(raw)

# Handle with monadic patterns
result = parse_data(input_data)
if result.is_err:
    return APIResponse(result)
return process_further(result.unwrap())
```

### Validation Patterns

- Use Pydantic for data validation
- Convert validation errors to Result types
- Provide detailed error responses via APIResponse
- Type-safe request/response handling

## Documentation Standards

- **Docstrings**: Required for all public classes and complex functions
- **Type hints**: More important than prose documentation
- **README**: Minimal but with CI badges
- **CHANGELOG**: Automated generation via commitizen
- **Comments**: Rare - prefer self-documenting code with good types

## Anti-Patterns to Avoid

- **Any types**: Use proper generics instead
- **Untyped functions**: Every function must have complete type annotations
- **Exception-heavy code**: Prefer Result types for expected errors
- **Manual dependency management**: Use automated tools like Renovate
- **Inconsistent formatting**: All code must pass ruff formatting
- **Missing tests**: 100% coverage is mandatory, not aspirational

## Summary

Write code as if **type safety is the primary concern**, with modern Python features, functional programming influence, and zero tolerance for shortcuts in quality. Every line should be typed, tested, and maintainable for enterprise use.
