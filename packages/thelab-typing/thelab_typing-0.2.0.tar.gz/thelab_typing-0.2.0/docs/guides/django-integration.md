# Django Integration

## Why Type-Safe API Views?

Traditional Django views lack compile-time guarantees about request data:

```py
# Traditional approach - runtime errors waiting to happen
def create_user(request):
    name = request.POST.get("name")  # Could be None
    age = int(request.POST.get("age"))  # Could raise ValueError
    # No validation, no type safety
```

Type-safe views catch errors at development time:

```py
# Type-safe approach - errors caught by mypy
class CreateUser(pydantic.BaseModel):
    name: str
    age: int

@validate()
def create_user(request: TypedRequest[None, CreateUser, None]) -> HttpResponse:
    # request.validated_body is guaranteed to be validated CreateUser
    name = request.validated_body.name  # Always str
    age = request.validated_body.age    # Always int
```

Benefits:

- **Compile-time validation**: `mypy` catches type errors
- **Automatic request validation**: Pydantic handles data parsing
- **Self-documenting**: Function signatures show expected data structure
- **IDE support**: Full autocomplete and type checking

## Installation

Install with Django support:

```sh
pip install thelab-typing[django]
```

Add to `INSTALLED_APPS` if using model integration:

```py
INSTALLED_APPS = [
    # ...
    "thelabtyping",
    # ...
]
```

## Request Validation

### Query Parameters Only

```py
class SearchQuery(pydantic.BaseModel):
    q: str
    limit: int = 10

@validate()
def search_view(request: TypedRequestQuery[SearchQuery]) -> HttpResponse:
    query = request.validated_querystring.q
    limit = request.validated_querystring.limit
    return HttpResponse(f"Searching '{query}' with limit {limit}")
```

### Request Body Only

```py
class CreateUser(pydantic.BaseModel):
    name: str
    email: str
    age: int

@validate()
def create_user(request: TypedRequestBody[CreateUser]) -> HttpResponse:
    user_data = request.validated_body
    return HttpResponse(f"Creating user: {user_data.name}")
```

### Both Query and Body

```py
class UserQuery(pydantic.BaseModel):
    include_deleted: bool = False

class UpdateUser(pydantic.BaseModel):
    name: str | None = None
    email: str | None = None

@validate()
def update_user(
    request: TypedRequest[UserQuery, UpdateUser, None],
    user_id: int
) -> HttpResponse:
    include_deleted = request.validated_querystring.include_deleted
    updates = request.validated_body
    return HttpResponse("User updated")
```

### Authentication

Use authenticated request types to require login:

```py
from django.contrib.auth.models import User

@validate()
def protected_view(request: AuthdEmptyTypedRequest) -> HttpResponse:
    # request.user is guaranteed to be authenticated User
    username = request.user.username
    return HttpResponse(f"Hello, {username}")
```

### Error Handling

Validation errors become structured JSON responses:

```py
# Invalid request data automatically returns:
{
  "errors": {
    "age": {
      "type": "int_parsing",
      "msg": "Input should be a valid integer"
    }
  }
}
```

#### Custom Errors

```py
from thelabtyping.api import APIResponse
from thelabtyping.result import Err
import pydantic

class QueryModel(pydantic.BaseModel):
    search: str

@validate()
def my_view(request: TypedRequest[QueryModel, None, None]) -> HttpResponse:
    if request.validated_querystring.search == "forbidden":
        error = Err(ValueError("Search term not allowed"))
        return APIResponse(error)

    return HttpResponse("Success")
```

## Response Handling

The `APIResponse` class is designed to work seamlessly with both Result types and regular Pydantic models, providing a unified way to handle API responses.

### Direct Model Usage

```py
from django.http import HttpRequest, HttpResponse
from thelabtyping.api import APIResponse, EmptyTypedRequest, validate
import pydantic

class UserResponse(pydantic.BaseModel):
    id: int
    username: str
    email: str

@validate()
def get_user(request: EmptyTypedRequest) -> HttpResponse:
    user_data = UserResponse(id=1, username="alice", email="alice@example.com")
    return APIResponse(user_data)  # Automatically serializes to JSON
```

### Integration with Result Types

`APIResponse` seamlessly handles Result types, making error handling elegant:

```py
from django.http import HttpRequest, HttpResponse
from thelabtyping.api import validate, TypedRequestQuery
from thelabtyping.result import as_result, Result, Ok, Err
import pydantic

@as_result(ValueError, KeyError)
def fetch_user_data(user_id: int) -> UserResponse:
    # Might raise exceptions
    if user_id < 1:
        raise ValueError("Invalid user ID")
    return UserResponse(id=user_id, username="alice", email="alice@example.com")

class UserQuery(pydantic.BaseModel):
    user_id: int

@validate()
def get_user_api(request: TypedRequestQuery[UserQuery]) -> HttpResponse:
    user_id = request.validated_querystring.user_id

    # fetch_user_data returns Result[UserResponse, ValueError | KeyError]
    result = fetch_user_data(user_id)

    # APIResponse handles both success and error cases automatically
    return APIResponse(result)
    # ✅ Success: Returns JSON with 200 status
    # ❌ Error: Returns structured error JSON with 400 status
```

### Error Response Format

When `APIResponse` receives an `Err[ValidationError]`, it automatically formats errors:

```py
# Input: Err(ValidationError(...))
# Output:
{
  "errors": {
    "user_id": {
      "type": "int_parsing",
      "msg": "Input should be a valid integer"
    },
    "email": {
      "type": "value_error",
      "msg": "invalid email format"
    }
  }
}
```

### Combining with @validate Decorator

The `@validate` decorator and `APIResponse` work together to provide comprehensive error handling:

```py
class QueryModel(pydantic.BaseModel):
    search: str

class BodyModel(pydantic.BaseModel):
    data: str

@validate()
def complex_operation(request: TypedRequest[QueryModel, BodyModel, None]) -> HttpResponse:
    # Step 1: Request validation (handled by @validate)
    # If validation fails, @validate returns APIResponse with 400 error

    # Step 2: Business logic with Result types
    processing_result = process_business_logic(
        request.validated_querystring,
        request.validated_body
    )

    # Step 3: Response handling (handled by APIResponse)
    return APIResponse(processing_result)
    # Automatically handles Ok[Model] -> JSON or Err[Exception] -> error JSON
```

### Status Code Handling

The library provides comprehensive HTTP status code support through `Status` and `StatusType` enums:

```py
from thelabtyping.api import Status, StatusType

# Success cases: 200 OK (default)
return APIResponse(Ok(user_model))

# Validation errors: 400 Bad Request (automatic)
return APIResponse(Err(validation_error))

# Custom status codes using Status enum
return APIResponse(user_model, status=Status.HTTP_201_CREATED)
return APIResponse(user_model, status=Status.HTTP_202_ACCEPTED)

# Non-validation errors: Re-raised as exceptions
return APIResponse(Err(RuntimeError("Database down")))  # Raises exception
```

#### Status Categories

Use `StatusType` to check status code categories:

```py
@validate()
def status_info(request: EmptyTypedRequest) -> HttpResponse:
    status = Status.HTTP_404_NOT_FOUND

    # Check status categories
    if status.is_client_error:
        return HttpResponse("This is a 4xx error")
    elif status.is_server_error:
        return HttpResponse("This is a 5xx error")
    elif status.is_success:
        return HttpResponse("This is a 2xx success")

    return APIResponse({"status": status}, status=status)
```

#### Custom Error Responses

```py
@validate()
def api_view_with_custom_errors(request: EmptyTypedRequest) -> HttpResponse:
    # Business logic here...
    if some_condition:
        return APIResponse(
            {"error": "Resource not found"},
            status=Status.HTTP_404_NOT_FOUND
        )

    if another_condition:
        return APIResponse(
            {"error": "Forbidden action"},
            status=Status.HTTP_403_FORBIDDEN
        )

    return APIResponse({"success": True})
```

## URL Routing

The library provides a type-safe routing system that organizes your API endpoints and automatically generates index views.

### Basic Router Setup

Create your view functions in `views.py`:

```py
# views.py
from thelabtyping.api import validate, TypedRequestQuery, EmptyTypedRequest
from django.http import HttpResponse
import pydantic

class SearchQuery(pydantic.BaseModel):
    q: str
    limit: int = 10

@validate()
def search_users(request: TypedRequestQuery[SearchQuery]) -> HttpResponse:
    query = request.validated_querystring.q
    limit = request.validated_querystring.limit
    return HttpResponse(f"Search results for '{query}'")

@validate()
def get_user(request: EmptyTypedRequest, user_id: int) -> HttpResponse:
    return HttpResponse(f"User {user_id}")
```

Then register routes in `urls.py`:

```py
# urls.py
from thelabtyping.api import Router
from . import views

# Create router and register routes
api_router = Router(basename="api", enable_index=True)

# Register routes with view functions
api_router.route("search", name="search", get=views.search_users)
api_router.route("users/<int:user_id>", name="user-detail", get=views.get_user)

urlpatterns = api_router.urls
```

### Multiple HTTP Methods

Define view functions in `views.py`:

```py
# views.py
from thelabtyping.api import validate, TypedRequestQuery, TypedRequestBody
from django.http import HttpResponse
import pydantic

class UserQuery(pydantic.BaseModel):
    include_deleted: bool = False

class CreateUser(pydantic.BaseModel):
    name: str
    email: str

class UpdateUser(pydantic.BaseModel):
    name: str | None = None
    email: str | None = None

@validate()
def list_users(request: TypedRequestQuery[UserQuery]) -> HttpResponse:
    return HttpResponse("User list")

@validate()
def create_user(request: TypedRequestBody[CreateUser]) -> HttpResponse:
    return HttpResponse("User created")

@validate()
def update_user(request: TypedRequestBody[UpdateUser]) -> HttpResponse:
    return HttpResponse("User updated")
```

Register multiple methods in `urls.py`:

```py
# urls.py
from thelabtyping.api import Router
from . import views

api_router = Router(basename="api", enable_index=True)

# Register multiple HTTP methods on the same route
api_router.route("users", name="users",
    get=views.list_users,
    post=views.create_user,
    put=views.update_user
)

urlpatterns = api_router.urls
```

### Including in Main URLs

Include your API router in your main `urls.py`:

```py
# main_project/urls.py
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("myapp.urls")),  # Include your app's API routes
]
```

### Auto-Generated Index

When `enable_index=True`, the router automatically creates an index view at the root URL that lists all available endpoints:

```py
# GET /api/ returns:
{
  "api:search": "http://localhost:8000/api/search",
  "api:user-detail": "http://localhost:8000/api/users/1",  # Skipped (requires params)
  "api:users": "http://localhost:8000/api/users"
}
```

## Working with Collections

When dealing with collections of Django models, `partition_results` helps separate successful conversions from validation errors.

### Basic Collection Handling

```py
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User as DjangoUser
from thelabtyping.result import partition_results, as_result
from thelabtyping.api import APIObj, APIResponse, validate, EmptyTypedRequest
from typing import Self
import pydantic_core

class User(APIObj[DjangoUser]):
    id: int
    username: str
    email: str

    @classmethod
    @as_result(pydantic_core.ValidationError)
    def from_django(cls, request: HttpRequest, obj: DjangoUser) -> Self:
        return cls.model_validate({
            "id": obj.id,
            "username": obj.username,
            "email": obj.email,
        })

@validate()
def list_users(request: EmptyTypedRequest) -> HttpResponse:
    django_users = DjangoUser.objects.all()

    # Convert each Django user to API model, collecting Results
    user_results = [User.from_django(request, user) for user in django_users]

    # Separate successful conversions from validation errors
    valid_users, validation_errors = partition_results(user_results)

    if validation_errors:
        # Log errors or handle them as needed
        print(f"Skipped {len(validation_errors)} invalid users")

    # Create typed list and return
    user_list = User.get_list_model()(valid_users)
    return APIResponse(user_list)
```

### Automatic Collection Handling

The `APIObj.list_from_django()` method combines this pattern:

```py
@validate()
def list_users_simplified(request: EmptyTypedRequest) -> HttpResponse:
    django_users = DjangoUser.objects.all()

    # This automatically calls partition_results internally
    user_list, errors = User.list_from_django(request, django_users)

    # Errors are logged automatically, valid users returned
    return APIResponse(user_list)
```

### Error Handling Strategies

```py
from thelabtyping.result import Err

@validate()
def robust_user_list(request: EmptyTypedRequest) -> HttpResponse:
    django_users = DjangoUser.objects.all()
    user_results = [User.from_django(request, user) for user in django_users]

    valid_users, validation_errors = partition_results(user_results)

    if len(validation_errors) > len(valid_users):
        # Too many errors - something's wrong
        return APIResponse(
            Err(ValueError("Too many validation errors in user data"))
        )

    # Acceptable error rate - proceed with valid users
    user_list = User.get_list_model()(valid_users)
    return APIResponse(user_list)
```

## Model Serialization

Create API serializers with `APIObj`:

```py
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User as DjangoUser
from thelabtyping.api import APIObj, APIResponse, validate, TypedRequestQuery
from thelabtyping.result import Result, as_result
import pydantic_core

class User(APIObj[DjangoUser]):
    id: int
    username: str
    email: str

    @classmethod
    @as_result(pydantic_core.ValidationError)
    def from_django(
        cls,
        request: HttpRequest,
        obj: DjangoUser
    ) -> Self:
        return cls.model_validate({
            "id": obj.id,
            "username": obj.username,
            "email": obj.email,
        })

class UserQuery(pydantic.BaseModel):
    user_id: int

@validate()
def get_user(request: TypedRequestQuery[UserQuery]) -> HttpResponse:
    django_user = DjangoUser.objects.get(id=request.validated_querystring.user_id)

    # from_django returns Result[User, ValidationError]
    user_result = User.from_django(request, django_user)

    # APIResponse handles the Result automatically
    return APIResponse(user_result)
```
