# Django REST Framework Integration

Building on the Django integration concepts, thelab-typing extends support to Django REST Framework with Pydantic-aware renderers that eliminate manual serialization.

## Why Enhanced DRF Integration?

Standard DRF requires manual conversion between Pydantic models and JSON:

```py
# Standard DRF approach - manual serialization
from rest_framework.views import APIView
from rest_framework.response import Response

class UserView(APIView):
    def get(self, request):
        user_data = UserResponse(id=1, name="Alice", email="alice@example.com")
        return Response(user_data.model_dump())  # Manual conversion required
```

Enhanced renderers handle this automatically:

```py
# thelab-typing approach - automatic serialization
class UserView(APIView):
    def get(self, request):
        user_data = UserResponse(id=1, name="Alice", email="alice@example.com")
        return Response(user_data)  # Pydantic model serialized automatically
```

## Installation

Install with DRF support:

```sh
pip install thelab-typing[drf]
```

Add to Django settings:

```py
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "thelabtyping",
    # ...
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "thelabtyping.drf.renderers.JSONRenderer",
        "thelabtyping.drf.renderers.BrowsableAPIRenderer",
    ],
}
```

## Enhanced Renderers

### JSON Renderer

The enhanced `JSONRenderer` automatically handles Pydantic models:

```py
from rest_framework.views import APIView
from rest_framework.response import Response
import pydantic

class UserResponse(pydantic.BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

class UserView(APIView):
    def get(self, request):
        user_data = UserResponse(
            id=1,
            name="Alice",
            email="alice@example.com",
            is_active=True
        )
        # Automatic Pydantic serialization with proper JSON formatting
        return Response(user_data)
```

### Browsable API Renderer

The enhanced `BrowsableAPIRenderer` displays Pydantic models in DRF's web interface:

```py
# With enhanced renderer, Pydantic models display correctly in:
# - DRF's browsable API interface
# - API documentation
# - Debug responses
```

## Combining with Type-Safe Django Views

The most powerful approach combines DRF renderers with thelab-typing's validation system:

### DRF Views with Validation

```py
# views.py
from rest_framework.decorators import api_view
from django.http import HttpResponse
from thelabtyping.api import validate, TypedRequestQuery, APIResponse
import pydantic

class SearchQuery(pydantic.BaseModel):
    q: str
    limit: int = 10
    category: str | None = None

class SearchResult(pydantic.BaseModel):
    query: str
    results: list[str]
    total: int
    category: str | None

@api_view(["GET"])
@validate()
def search_api(request: TypedRequestQuery[SearchQuery]) -> HttpResponse:
    query_params = request.validated_querystring

    # Perform search logic
    results = SearchResult(
        query=query_params.q,
        results=["result1", "result2"],
        total=2,
        category=query_params.category
    )

    # APIResponse + enhanced DRF renderer = automatic serialization
    return APIResponse(results)
```

### Router Integration

Use the routing system with DRF decorators:

```py
# urls.py
from thelabtyping.api import Router
from rest_framework.decorators import api_view
from . import views

api_router = Router(basename="api", enable_index=True)

# Combine DRF decorators with router registration
api_router.route("search", name="search", get=views.search_api)

urlpatterns = api_router.urls
```

### Class-Based Views

Enhanced renderers work with DRF class-based views:

```py
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from thelabtyping.api import validate, TypedRequestBody
from thelabtyping.result import Result, as_result

class CreateUser(pydantic.BaseModel):
    name: str
    email: str
    age: int

class UserResponse(pydantic.BaseModel):
    id: int
    name: str
    email: str
    created_at: str

class UserCreateView(APIView):
    @validate()
    def post(self, request: TypedRequestBody[CreateUser]) -> Response:
        user_data = request.validated_body

        # Business logic with Result types
        creation_result = self.create_user_logic(user_data)

        # Enhanced renderer handles both Pydantic models and Results
        if creation_result.is_ok:
            return Response(creation_result.unwrap(), status=201)
        else:
            return Response({"error": str(creation_result.unwrap_err())}, status=400)

    @as_result(ValueError, KeyError)
    def create_user_logic(self, user_data: CreateUser) -> UserResponse:
        # Your business logic here
        return UserResponse(
            id=123,
            name=user_data.name,
            email=user_data.email,
            created_at="2024-01-01T00:00:00Z"
        )
```

## Migration from Standard DRF

### Before: Manual Serialization

```py
# Standard DRF approach
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()

class UserView(APIView):
    def get(self, request):
        # Manual data preparation
        data = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        serializer = UserSerializer(data)
        return Response(serializer.data)
```

### After: Automatic with Type Safety

```py
# thelab-typing approach
from rest_framework.views import APIView
from rest_framework.response import Response
import pydantic

class UserResponse(pydantic.BaseModel):
    id: int
    name: str
    email: str

class UserView(APIView):
    def get(self, request):
        # Type-safe model with automatic serialization
        user_data = UserResponse(id=1, name="Alice", email="alice@example.com")
        return Response(user_data)  # Enhanced renderer handles conversion
```

## Best Practices

### Consistent Response Types

Use the same Pydantic models across Django and DRF views:

```py
# Shared models in models.py
class UserResponse(pydantic.BaseModel):
    id: int
    name: str
    email: str

# Django view
@validate()
def django_user_view(request: EmptyTypedRequest) -> HttpResponse:
    user = UserResponse(id=1, name="Alice", email="alice@example.com")
    return APIResponse(user)

# DRF view
class DRFUserView(APIView):
    def get(self, request):
        user = UserResponse(id=1, name="Alice", email="alice@example.com")
        return Response(user)  # Same model, same result
```

### Error Handling Consistency

Both Django and DRF views benefit from the same error handling patterns:

```py
from thelabtyping.result import Result, Err
from thelabtyping.api import Status

class DRFUserView(APIView):
    def get(self, request):
        user_result = self.fetch_user()

        if user_result.is_err:
            error = user_result.unwrap_err()
            return Response(
                {"error": str(error)},
                status=Status.HTTP_404_NOT_FOUND
            )

        return Response(user_result.unwrap())
```
