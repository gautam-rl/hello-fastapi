I tried to run `pytest .` but got this error. Please make changes to the repo to fix
this issue.

```
__________________________________________ ERROR collecting test_app.py __________________________________________
.venv/lib/python3.12/site-packages/starlette/testclient.py:33: in <module>
    import httpx
E   ModuleNotFoundError: No module named 'httpx'

During handling of the above exception, another exception occurred:
test_app.py:1: in <module>
    from fastapi.testclient import TestClient
.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: in <module>
    from starlette.testclient import TestClient as TestClient  # noqa
.venv/lib/python3.12/site-packages/starlette/testclient.py:35: in <module>
    raise RuntimeError(
E   RuntimeError: The starlette.testclient module requires the httpx package to be installed.
E   You can install this with:
E       $ pip install httpx
============================================ short test summary info =============================================
ERROR test_app.py - RuntimeError: The starlette.testclient module requires the httpx package to be installed.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
================================================ 1 error in 0.22s ======================================== [0.72s]
```
