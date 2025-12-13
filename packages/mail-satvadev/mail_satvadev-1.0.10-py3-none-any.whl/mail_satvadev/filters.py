import logging
import pprint

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

logger = logging.getLogger(__name__)


class RecipientFilter:
    """Фильтр email на основании их валидности"""

    def __init__(self):
        self.validator = EmailValidator()

    def filter_emails(self, recipients: list) -> list:
        """Возвращает список валидных email, невалидные исключаются"""
        valid_list = []
        for recipient in recipients:
            try:
                self.validator(recipient.strip())
            except (ValidationError, UnicodeError) as ex:
                logger.exception(
                    f'Can`t send email message to {recipient}.'
                    f' {pprint.saferepr(ex)}')
                continue
            valid_list.append(recipient)
        return valid_list
