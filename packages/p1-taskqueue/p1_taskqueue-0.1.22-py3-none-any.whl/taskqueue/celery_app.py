"""
Celery application setup for TaskQueue.
Reads configuration from Django settings and auto-configures queues with DLQ.
"""
import logging

from amqp.exceptions import PreconditionFailed
from celery import Celery
from kombu import Exchange
from kombu import Queue

logger = logging.getLogger(__name__)


def get_django_settings():
    """Get Django settings, fail fast if not properly configured."""
    try:
        from django.conf import settings
        return settings
    except ImportError:
        raise ImportError("[TaskQueue] Django settings not found.")


def create_celery_app():
    """Create and configure the Celery application."""
    settings = get_django_settings()

    app_name = getattr(settings, 'TASKQUEUE_APP_NAME', 'taskqueue')
    app = Celery(app_name)

    # https://docs.celeryq.dev/en/latest/userguide/configuration.html
    celery_config = {
        'broker_url': getattr(settings, 'CELERY_BROKER_URL', 'amqp://localhost:5672//'),
        'result_backend': getattr(settings, 'CELERY_RESULT_BACKEND', 'rpc://localhost:5672//'),
        'task_serializer': getattr(settings, 'CELERY_TASK_SERIALIZER', 'pickle'),
        'result_serializer': getattr(settings, 'CELERY_RESULT_SERIALIZER', 'pickle'),
        'accept_content': getattr(settings, 'CELERY_ACCEPT_CONTENT', ['pickle']),
        'timezone': getattr(settings, 'CELERY_TIMEZONE', 'UTC+7'),
        'task_time_limit': getattr(settings, 'CELERY_TASK_TIME_LIMIT', 30 * 60),
        'task_soft_time_limit': getattr(settings, 'CELERY_TASK_SOFT_TIME_LIMIT', 25 * 60),
        # 14 days
        'result_expires': getattr(settings, 'CELERY_RESULT_EXPIRES', 14 * 24 * 60 * 60),
        'task_track_started': True,
        'task_always_eager': False,
        'task_eager_propagates': True,
        'task_acks_late': True,
        'result_extended': True,
        'task_ignore_result': False,
        'task_send_sent_event': True,
        'worker_send_task_events': True,
        'task_reject_on_worker_lost': True,
        'worker_prefetch_multiplier': 1,
        'worker_max_tasks_per_child': 1000,
    }

    setup_queues(app, settings, celery_config)
    app.conf.update(celery_config)
    app.autodiscover_tasks(['taskqueue'])

    return app


def setup_queues(app, settings, celery_config):
    app_name = getattr(settings, 'TASKQUEUE_APP_NAME', 'taskqueue')
    queue_names = getattr(settings, 'TASKQUEUE_QUEUES',
                          ['default', 'high', 'low'])
    if queue_names is None:
        queue_names = ['default', 'high', 'low']
    dlq_name_prefix = getattr(settings, 'TASKQUEUE_DLQ_NAME_PREFIX', 'dlq')

    logger.info(
        f"[TaskQueue] Configuring app: {app_name}, queues: {queue_names}")

    main_exchange = Exchange(app_name, type='direct')
    dlx_exchange = Exchange(f'{app_name}.dlx', type='direct')

    queues = []

    for queue_name in queue_names:
        dlq_name = f'{dlq_name_prefix}.{queue_name}'
        dlx_name = f'{app_name}.dlx'

        queue_args = {
            'x-dead-letter-exchange': dlx_name,
            'x-dead-letter-routing-key': dlq_name
        }

        queue = Queue(
            queue_name,
            main_exchange,
            routing_key=queue_name,
            queue_arguments=queue_args
        )
        queues.append(queue)
        logger.info(
            f"[TaskQueue] Queue '{queue_name}' configured with DLX: {dlx_name}, DLQ routing key: {dlq_name}")

    for queue_name in queue_names:
        dlq_name = f'{dlq_name_prefix}.{queue_name}'
        dlq = Queue(dlq_name, dlx_exchange, routing_key=dlq_name)
        queues.append(dlq)
        logger.info(f"[TaskQueue] DLQ '{dlq_name}' configured")

    celery_config.update({
        'task_default_queue': 'default',
        'task_default_exchange': app_name,
        'task_default_exchange_type': 'direct',
        'task_queues': tuple(queues),
    })

    try:
        with app.connection_or_acquire() as conn:
            channel = conn.default_channel

            try:
                main_exchange.declare(channel=channel)
                logger.info(f"[TaskQueue] Exchange declared: {app_name}")
            except PreconditionFailed:
                logger.info(f"[TaskQueue] Exchange already exists: {app_name}")

            try:
                dlx_exchange.declare(channel=channel)
                logger.info(
                    f"[TaskQueue] DLX Exchange declared: {app_name}.dlx")
            except PreconditionFailed:
                logger.info(
                    f"[TaskQueue] DLX Exchange already exists: {app_name}.dlx")

            for queue in queues:
                try:
                    queue.declare(channel=channel)
                    logger.info(f"[TaskQueue] Queue declared: {queue.name}")
                except PreconditionFailed:
                    logger.info(
                        f"[TaskQueue] Queue already exists with different config: {queue.name}. Using existing queue.")
                except Exception as e:
                    logger.warning(
                        f"[TaskQueue] Failed to declare queue {queue.name}: {e}")

    except Exception as e:
        logger.warning(
            f"[TaskQueue] Failed to setup queues: {str(e.__class__.__name__)} {e}")


celery_app = create_celery_app()
