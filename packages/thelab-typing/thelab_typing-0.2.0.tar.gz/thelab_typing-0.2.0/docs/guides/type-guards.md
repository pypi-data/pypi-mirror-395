# Type Guards

## Literal Type Guards

The `is_literal_factory` function creates type guards for Literal types:

```py
from typing import Literal
from thelabtyping.guards import is_literal_factory

type Status = Literal["pending", "complete", "failed"]

is_status = is_literal_factory(Status)

def process_status(value: str) -> None:
    if is_status(value):
        # value is now typed as Status
        match value:
            case "pending":
                print("Still processing...")
            case "complete":
                print("Done!")
            case "failed":
                print("Error occurred")
```

## Container Type Guards

Use `ListOf` and `DictOf` for type-safe Pydantic containers:

```py
from thelabtyping.abc import ListOf, DictOf
import pydantic

class User(pydantic.BaseModel):
    name: str
    age: int

class UserList(ListOf[User]):
    pass

class UserMap(DictOf[str, User]):
    pass

# Type-safe operations
users = UserList([
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
])

for user in users:  # user is typed as User
    print(user.name)

user_map = UserMap({
    "alice": {"name": "Alice", "age": 30}
})
alice = user_map["alice"]  # alice is typed as User
```
