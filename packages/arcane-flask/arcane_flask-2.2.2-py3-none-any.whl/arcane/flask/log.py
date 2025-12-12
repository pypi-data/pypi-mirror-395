import json
import logging
import sys
from functools import wraps
from typing import Any, Callable, Literal, Optional

from flask import g, has_request_context, request
from flask_log_request_id import current_request_id

STANDARD_FORMAT = '{"severity": "%(levelname)s", "logging.googleapis.com/trace": "%(cloud_trace)s", "logging.googleapis.com/spanId": "%(span_id)s", "component": "arbitrary", "message": %(message)s, "logging.googleapis.com/labels": %(labels)s}'


class LabelFilter(logging.Filter):
    """
    Logging filter that injects structured labels into each log record.

    Labels are stored per-request on ``flask.g.logging_labels`` (a simple
    dictionary) and JSON-encoded into the ``labels`` attribute of the
    record. When there is no active request context, ``labels`` defaults
    to the empty JSON object (``{}``).
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "labels"):
            record.labels = "{}"
        if has_request_context():
            labels = getattr(g, "logging_labels", {})
            record.labels = json.dumps(labels)
        return True


def attach_labels(**labels: Any) -> None:
    """
    Attach or update structured logging labels for the current request.

    This stores key/value pairs on ``flask.g.logging_labels`` which are
    then picked up by ``LabelFilter`` and emitted in every log record
    for the remainder of the request.

    Example
    -------
    >>> attach_labels(component="feed-boost", module="api")

    Notes
    -----
    This function must be called inside an active Flask request (or
    application) context; otherwise Flask will raise a
    ``RuntimeError`` about working outside of the application context.
    """
    if not hasattr(g, "logging_labels"):
        g.logging_labels = {}
    g.logging_labels.update(labels)


def clear_labels() -> None:
    """
    Clear all structured logging labels for the current request.

    In a typical Flask application you should call this from a
    ``teardown_request`` handler to ensure labels do not leak between
    re-used contexts in tests or background processing:

        @app.teardown_request
        def _clear_labels(exc):
            logs.clear_labels()
    """
    if hasattr(g, "logging_labels"):
        g.logging_labels = {}


def with_log_labels(**static_labels: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator that automatically attaches static logging labels
    at the beginning of a request handler.

    This is a convenience wrapper around :func:`attach_labels` for
    common, mostly-static metadata such as ``component``, ``module``
    or ``function``.

    Example
    -------
    >>> @with_log_labels(component="feed-boost", module="api", function="validate_model_parallelism_post")
    ... def validate_model_parallelism_post(...):
    ...     attach_labels(optimization_id=optimization_id, job_prefix=job_prefix)
    ...     ...
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # This will be a no-op outside a request context, but will
            # raise the standard Flask RuntimeError if misused.
            attach_labels(**static_labels)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def adscale_log(
    service: str,  # should be ValueOf ServiceEnum
    msg: str
    ):
    """Deprecated, should not be used anymore
    """
    request_id = None
    try:
        request_id = current_request_id()
    except KeyError:
        pass

    logging.info("[%s][%s] %s", service, request_id, msg)


class RequestFormatter(logging.Formatter):
    """Logging Formatter to add request id and trace id to log records
    """
    def __init__(self,
            fmt: Optional[str] = STANDARD_FORMAT,
            datefmt: Optional[str] = None,
            style: Literal["%", "{", "$"] = "%",
            validate: bool = True,
            gcp_project: Optional[str] = None,
            span_id_header: str = "X-Span-Id"):

        super().__init__(fmt, datefmt, style, validate)
        self.gcp_project = gcp_project
        self.span_id_header = span_id_header

    def format(self, record):
        if has_request_context():
            trace_header: str = request.headers.get("X-Cloud-Trace-Context")
            span_id : str = request.headers.get(self.span_id_header)
            if trace_header:
                trace = trace_header.split("/")
                record.cloud_trace = f"projects/{self.gcp_project}/traces/{trace[0]}"
            else:
                record.cloud_trace = None

            if span_id:
                record.span_id = f"projects/{self.gcp_project}/spanId/{span_id}"
            else:
                record.span_id = None
        else:
            record.cloud_trace = None
            record.span_id = None


        # Handle exception information properly
        if record.exc_info:
            # Format the exception with stack trace as a single string
            exc_text = self.formatException(record.exc_info)
            # Combine the message with the exception info
            full_message = f"{record.getMessage()}\n{exc_text}"
        else:
            full_message = record.getMessage()

        # JSON encode the complete message to escape newlines and special characters
        record.msg = json.dumps(full_message)
        # Clear args to prevent double formatting
        record.args = None

        return super().format(record)

def setup_logging(
    fmt : Optional[str] = STANDARD_FORMAT,
    datefmt: Optional[str] = None,
    style   :  Literal["%", "{", "$"] = "%",
    validate: bool = True,
    gcp_project: Optional[str] = None,
    level = logging.INFO,
    span_id_header: str = "X-Span-Id",
    filter: Optional[logging.Filter] = None
):
    """
    Setup logging for the application
    """
    handler = logging.StreamHandler(
        sys.stdout
    )

    handler.setFormatter(
        RequestFormatter(
            fmt,
            datefmt,
            style,
            validate,
            gcp_project,
            span_id_header
        )
    )

    logging.basicConfig(
        level=level,
        handlers=[handler]
    )

    root = logging.getLogger()

    if not filter:
        filter = LabelFilter()


    root.addFilter(filter)
    for handler in root.handlers:
            handler.addFilter(filter)

    return root
