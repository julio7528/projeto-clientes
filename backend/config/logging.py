import logging
import re

from django.conf import settings


class SecretRedactionFilter(logging.Filter):
    """Redacts configured secret values before they reach handlers."""

    def filter(self, record):
        secrets = getattr(settings, "LOG_REDACTED_SECRETS", ())
        message = record.getMessage()

        for secret in secrets:
            if secret:
                message = message.replace(secret, "[REDACTED]")

        message = re.sub(
            r"(?i)(authorization|apikey)\s*[:=]\s*(?:bearer\s+)?[^\s,;]+",
            r"\1=[REDACTED]",
            message,
        )
        message = re.sub(
            r"(?i)postgres(?:ql)?://[^\s]+",
            "[REDACTED_DATABASE_URL]",
            message,
        )
        message = re.sub(
            r"https?://[^\s]+/storage/v1/object/sign/[^\s]+",
            "[REDACTED_SIGNED_URL]",
            message,
        )

        record.msg = message
        record.args = ()
        return True

