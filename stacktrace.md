We recorded this error when trying to run our app:

```
INFO:     127.0.0.1:59476 - "GET / HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py", line 407, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 69, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1054, in __call__
    await super().__call__(scope, receive, send)
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/applications.py", line 123, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
    raise exc
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    await app(scope, receive, sender)
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/routing.py", line 756, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/routing.py", line 776, in app
    await route.handle(scope, receive, send)
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/routing.py", line 297, in handle
    await self.app(scope, receive, send)
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/routing.py", line 77, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
    raise exc
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    await app(scope, receive, sender)
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/starlette/routing.py", line 72, in app
    response = await func(request)
               ^^^^^^^^^^^^^^^^^^^
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 278, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/gautam/source/hello-fastapi/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/gautam/source/hello-fastapi/app.py", line 26, in home
    todos = db.query(models.Todo).all()
            ^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'query'

```

Please create a test that reproduces the issue, and then resolve the issue.
