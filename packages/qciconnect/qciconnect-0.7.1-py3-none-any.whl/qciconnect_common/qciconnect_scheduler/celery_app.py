"""Module that provides celery instances and configs."""

from celery import Celery
from qciconnect_settings.environment_config import get_settings

# Fetch settings
settings = get_settings()
_db = settings.db
_redis = settings.redis


def _get_redis_url_template() -> str:
    """Return redis url template.

    Returns:
        redis url template string.
    """
    return "redis://:{password}@{host}:{port}/{db}"


def _get_postgres_url_template() -> str:
    """Return postgres url template.

    Returns:
        postres url template string.
    """
    return "db+{drivername}://{user}:{password}@{host}/{database_name}"


# default redis and postgres url for celery
redis_url = _get_redis_url_template().format(
    password=_redis.password, host=_redis.host, port=_redis.port, db=_redis.queue_db
)
postgres_url = _get_postgres_url_template().format(
    drivername=_db.drivername,
    user=_db.user,
    password=_db.password,
    host=_db.host,
    database_name=_db.database,
)


def get_celery_app(
    name: str,
    broker_url: str = redis_url,
    backend_url: str = postgres_url,
    task_routes: dict | None = None,
    registered_task_modules: list[str] | None = None,
    task_acks_late=False,
    worker_prefetch_multiplier=1,
    task_track_started=True,
) -> Celery:
    """Create a new Celery application.

    Args:
        name (str): The name of the celery application.
        broker_url (str): The URL of the message broker to use for task distribution.
        backend_url (str): The URL of the backend to use for storing task results.
        task_routes (dict): Dict with task queue routing information. Defaults to empty dict.
        registered_task_modules (list[str], optional): A list of Python modules that
            register tasks to be used by the Celery application. Defaults to None.
        task_acks_late (bool, optional): Configuration option to acknowledge tasks after they have
            been successfully processed by the worker instead of immediately after receipt.
            Defaults to False.
        worker_prefetch_multiplier (int, optional): The number of tasks a worker will prefetch
            from the task queue. Defaults to 1.
        task_track_started (bool, optional): If True, a 'STARTED' state is sent when
            the worker starts processing the task. Defaults to True.

    Returns:
        celery.Celery: Configured Celery application instance.
    """
    if task_routes is None:
        task_routes = {}

    app = Celery(
        name,
        backend=backend_url,
        broker=broker_url,
        task_routes=task_routes,
        imports=registered_task_modules,
        task_acks_late=task_acks_late,
        worker_prefetch_multiplier=worker_prefetch_multiplier,
        task_track_started=task_track_started,
    )
    app.conf.update(worker_hijack_root_logger=False)
    return app
