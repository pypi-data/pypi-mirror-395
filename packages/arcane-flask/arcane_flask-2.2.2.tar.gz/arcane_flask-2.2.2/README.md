# Arcane flask

This package help us authenticate users

## Get Started

```sh
pip install arcane-flask
```

## Example Usage

```python
from arcane.flask import check_access_rights
from arcane.core import RightsLevelEnum, UserRightsEnum
from arcane.datastore import Client as DatastoreClient
from arcane.pubsub import Client as PubSubClient

datastore_client = DatastoreClient()
pubsub_client = PubSubClient()

@check_access_rights(
    service='my-service',
    required_rights=RightsLevelEnum.VIEWER,
    service_user_right=UserRightsEnum.MY_SERVICE,
    datastore_client=datastore_client,
    pubsub_client=pubsub_client,
    receive_rights_per_client=True,
    project='my-project',
    timeout=30  # Timeout in seconds
)
def function(params):
    pass
```

## Timeout Configuration

The `check_access_rights` decorator includes a built-in `timeout` parameter that allows you to set a maximum execution time for the decorated function. If the function exceeds this timeout, the decorator will automatically return a timeout response.

```python
import time

@check_access_rights(
    service='my-service',
    required_rights=RightsLevelEnum.VIEWER,
    service_user_right=UserRightsEnum.MY_SERVICE,
    datastore_client=datastore_client,
    pubsub_client=pubsub_client,
    project='my-project',
    timeout=2  # 2 seconds timeout
)
def slow_function():
    time.sleep(5)  # This will exceed the timeout
    return {'result': 'success'}
```

If the function exceeds the timeout, the decorator will return:

```python
({'detail': 'Request Timeout'}, 504)
```

**Note:** Set the `timeout` parameter to a value a few seconds less than your Cloud Run or server timeout configuration to ensure proper error handling.

## Structured logging labels

The `arcane.flask.logs` module lets you add structured labels to every log
entry in a request. This is useful for attaching metadata such as
`component`, `module`, `function`, or IDs like `optimization_id`.

First, set up logging once at application startup:

```python
from arcane.flask import logs

logs.setup_logging(gcp_project="my-gcp-project-id")
```

Then, register a teardown handler to clear labels at the end of each request:

```python
from arcane.flask import logs

@app.teardown_request
def clear_logging_labels(exc):
    logs.clear_labels()
```

Inside your handlers you can either attach labels imperatively:

```python
from arcane.flask import logs

def validate_model_parallelism_post(optimization_id: str, job_prefix: str, ...):
    logs.attach_labels(
        component="feed-boost",
        module="api",
        function="validate_model_parallelism_post",
        optimization_id=optimization_id,
        job_prefix=job_prefix,
    )
    ...
```

or use the `with_log_labels` decorator for static labels and still add dynamic
labels as needed:

```python
from arcane.flask import logs

@logs.with_log_labels(
    component="feed-boost",
    module="api",
    function="validate_model_parallelism_post",
)
def validate_model_parallelism_post(optimization_id: str, job_prefix: str, ...):
    logs.attach_labels(
        optimization_id=optimization_id,
        job_prefix=job_prefix,
    )
    ...
```

All log records emitted during the request will then include a
`logging.googleapis.com/labels` field with the JSON-encoded labels.
