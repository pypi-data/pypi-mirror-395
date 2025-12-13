"""
Slack notification for TaskQueue.
"""
import json
import logging

import requests

logger = logging.getLogger(__name__)


class SlackbotManager:

    @classmethod
    def send_message(cls, message: str) -> None:
        try:
            from django.conf import settings
        except ImportError:
            return

        if not getattr(settings, 'TASKQUEUE_SLACK_ENABLED', False):
            return

        hook_url = getattr(settings, 'TASKQUEUE_SLACK_HOOK_URL', None)
        if not hook_url:
            return

        channel = getattr(
            settings, 'TASKQUEUE_SLACK_CHANNEL_NAME', '#tech-automation')
        username = getattr(
            settings, 'TASKQUEUE_SLACK_USERNAME', 'TaskQueueBot')
        icon_emoji = getattr(
            settings, 'TASKQUEUE_SLACK_ICON_EMOJI', ':robot_face:')

        is_staging = getattr(settings, 'IS_RUN_IN_STAGING_ENV', False)
        if is_staging:
            message = '[STAGING] ' + message

        try:
            requests.post(
                hook_url,
                data=json.dumps({
                    'channel': channel,
                    'username': username,
                    'text': message,
                    'icon_emoji': icon_emoji,
                }),
                headers={"Content-Type": "application/json"}
            )
        except Exception as e:
            logger.exception('[TaskQueue Slack] Error: %s', str(e))
