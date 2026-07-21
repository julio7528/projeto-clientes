import logging

from django.conf import settings


class SecretRedactionFilter(logging.Filter):
    """Redacts configured secret values before they reach handlers."""

    def filter(self, record):
        secrets = getattr(settings, "LOG_REDACTED_SECRETS", ())
        message = record.getMessage()

        for secret in secrets:
            if secret:
                message = message.replace(secret, "[REDACTED]")

        record.msg = message
        record.args = ()
        return True
