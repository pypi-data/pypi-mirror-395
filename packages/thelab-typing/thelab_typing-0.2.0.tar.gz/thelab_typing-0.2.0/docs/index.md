# thelab-typing

**Type-safe Django APIs with zero runtime overhead**

## The Problem

Django's flexibility comes at a cost—runtime errors from invalid data, brittle APIs that break silently, and endless boilerplate for request validation:

```py
# Traditional Django - runtime disasters waiting to happen
def create_user(request):
    name = request.POST.get("name")        # Could be None
    age = int(request.POST.get("age"))     # Could raise ValueError
    email = request.POST.get("email")      # No validation whatsoever
    # Ship it and hope for the best 🤞
```

## The Solution

thelab-typing brings **compile-time safety** to Django APIs using modern Python typing and Pydantic validation. Catch errors before they reach production:

```py
# Type-safe approach - errors caught by mypy at build time
class CreateUser(pydantic.BaseModel):
    name: str
    age: int
    email: str

@validate()
def create_user(request: TypedRequestBody[CreateUser]) -> HttpResponse:
    # request.validated_body is guaranteed to be valid CreateUser
    user_data = request.validated_body  # Full IDE support and type safety
```

## Core Philosophy

**Type Safety First**: Every function parameter, return value, and data structure is precisely typed. No `Any`, no guessing, no runtime surprises.

**Functional Error Handling**: Replace exception-driven code with `Result[T, E]` types that make error cases explicit and composable.

**Zero Boilerplate**: Automatic request validation, response serialization, and error formatting. Write business logic, not plumbing code.

**Modern Python**: Built for Python 3.13+ with cutting-edge type system features like generic type parameters and `TypeIs`.

## What You Get

- **🔒 Compile-time safety**: mypy catches API contract violations before deployment
- **📝 Self-documenting**: Function signatures become living API documentation
- **🚀 Developer experience**: Full IDE autocomplete, refactoring support, and instant error feedback
- **🛡️ Bulletproof APIs**: Automatic validation, structured error responses, and consistent behavior
- **⚡ Zero overhead**: Pure typing constructs with no runtime performance impact

## Installation

Install via pip:

```sh
pip install thelab-typing
```

### Optional Dependencies

The library provides optional integrations:

```sh
# For Django integration
pip install thelab-typing[django]

# For Django REST Framework integration
pip install thelab-typing[drf]

# For all features
pip install thelab-typing[django,drf]
```

## Quick Start

### Core Result Types

```py
from thelabtyping.result import Result, Ok, Err, as_result

@as_result(ValueError, TypeError)
def parse_data(data: str) -> dict:
    if not data:
        raise ValueError("Empty data")
    return {"parsed": data}

result = parse_data("hello")
if result.is_ok:
    print(result.unwrap())  # {"parsed": "hello"}
```

### Django API Validation

```py
from django.http import HttpResponse
from thelabtyping.api import validate, TypedRequestQuery
import pydantic

class QueryModel(pydantic.BaseModel):
    search: str

@validate()
def my_view(request: TypedRequestQuery[QueryModel]) -> HttpResponse:
    # request.validated_querystring is automatically validated QueryModel instance
    return HttpResponse(f"Searching for: {request.validated_querystring.search}")
```

## Next Steps

{nav}

<style type="text/css">
.autodoc { display: none; }
</style>
