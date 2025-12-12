# Result Types

## Why Use Result Types?

Traditional Python error handling relies on exceptions, which have several drawbacks:

- **Hidden control flow**: Exceptions don't appear in function signatures
- **Easy to ignore**: Uncaught exceptions cause crashes
- **Type checker limitations**: `mypy` can't track which exceptions a function might raise
- **Performance overhead**: Exception handling is expensive

Result types make error handling explicit and type-safe:

```py
# Traditional approach - hidden failure modes
def parse_user_id(data: str) -> int:
    return int(data)  # ValueError not visible in signature

# Result approach - explicit error handling
@as_result(ValueError)
def parse_user_id(data: str) -> int:
    return int(data)

# Return type is now Result[int, ValueError]
```

## Basic Usage

### Creating Results

```py
from thelabtyping.result import Ok, Err

# Success case
success = Ok(42)
print(success.is_ok)  # True
print(success.unwrap())  # 42

# Error case
failure = Err("Something went wrong")
print(failure.is_err)  # True
print(failure.unwrap_err())  # "Something went wrong"
```

### The @as_result Decorator

Convert exception-throwing functions to return Results:

```py
from thelabtyping.result import as_result

@as_result(ValueError, TypeError)
def safe_parse(data: str) -> dict:
    if not data:
        raise ValueError("Empty data")
    return {"value": int(data)}

result = safe_parse("42")
if result.is_ok:
    print(result.unwrap())  # {"value": 42}
else:
    print(f"Error: {result.unwrap_err()}")
```

## Chaining Operations

### Using and_then()

Chain operations that might fail:

```py
@as_result(ValueError)
def parse_int(s: str) -> int:
    return int(s)

@as_result(ValueError)
def validate_positive(n: int) -> int:
    if n <= 0:
        raise ValueError("Must be positive")
    return n

result = (
    parse_int("42")
    .and_then(validate_positive)
)
# Result[int, ValueError]
```

### Using do() Notation

For more complex chains, use `do()` notation:

```py
from thelabtyping.result import do

def process_data(raw: str) -> Result[dict, ValueError]:
    def _process():
        # Each yield must be a Result
        # If any Result is Err, the entire function returns that Err
        parsed = yield parse_int(raw)
        validated = yield validate_positive(parsed)
        return {"processed": validated}

    return do(_process())
```

## Working with Collections

Use `partition_results()` to handle collections of Results:

```py
from thelabtyping.result import partition_results

# Process a list of items
results = [parse_int(s) for s in ["1", "2", "invalid", "4"]]

# Separate successful and failed results
successes, errors = partition_results(results)
print(successes)  # [1, 2, 4]
print(len(errors))  # 1
```
