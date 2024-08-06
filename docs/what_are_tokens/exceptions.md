When a token is canceled, you can call the `check()` method from it and an exception will be raised:

```python
from cantok import TimeoutToken

token = TimeoutToken(1)
token.wait()
token.check()
#> ...
#> cantok.errors.TimeoutCancellationError: The timeout of 1 seconds has expired.
```

Each type of token (except [`DefaultToken`](../types_of_tokens/DefaultToken.md)) has a corresponding type of exception that can be raised in this case:

- [`SimpleToken`](../types_of_tokens/SimpleToken.md) -> `CancellationError`
- [`ConditionToken`](../types_of_tokens/ConditionToken.md) -> `ConditionCancellationError`
- [`TimeoutToken`](../types_of_tokens/TimeoutToken.md) -> `TimeoutCancellationError`
- [`CounterToken`](../types_of_tokens/CounterToken.md) -> `CounterCancellationError`

When you call the `check()` method on any token, one of two things will happen. If it (or any of the tokens nested in it) was canceled by calling the `cancel()` method, `CancellationError` will always be raised. But if the cancellation occurred as a result of the unique ability of the token, such as for `TimeoutToken` - timeout expiration, then an exception specific to this type of token will be raised.

`ConditionCancellationError`, `TimeoutCancellationError` and `CounterCancellationError` are inherited from `CancellationError`, so if you're not sure which exception specifically you're catching, catch `CancellationError`. But also all the listed exceptions can always be imported separately:

```python
from cantok import CancellationError, ConditionCancellationError, TimeoutCancellationError, CounterCancellationError
```

You can also choose not to import these exceptions at all. For each token class, the corresponding exception class is located in the `exception` attribute:

```python
from cantok import TimeoutToken, CancellationError

token = TimeoutToken(0)

try:
    token.check()
except CancellationError as e:
    print(type(e) is TimeoutToken.exception)  #> True
```

And each exception object has a `token` attribute indicating the specific token that was canceled. This can be useful in situations where several tokens are nested in one another and you want to find out which one has been canceled:

```python
from cantok import SimpleToken, TimeoutToken, CancellationError

nested_token = TimeoutToken(0)
token = SimpleToken(nested_token)

try:
    token.check()
except CancellationError as e:
    print(e.token is nested_token)  #> True
```
